from pyflink.datastream import SinkFunction
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import ConnectionError, TransportError
import json
import time
import logging
from dataclasses import dataclass
from typing import List, Dict, Optional, Any
from datetime import datetime
import backoff
import threading
from queue import Queue
import os

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ESIndexer")

# ========================================================================================
# 重要网络配置说明 (starcompass 项目):
# 1. 此 Flink Sink 组件依赖 Elasticsearch 服务，容器名为 es-worldlora
# 2. 当使用 Docker Compose (项目名 starcompass) 部署时，请确保：
#    - Elasticsearch 容器 (服务名通常映射到容器名 es-worldlora) 在 starcompass_default 网络中
#    - Flink TaskManager 容器 (例如 starcompass-flink-taskmanager-1) 也在 starcompass_default 网络中
#    - Sink 配置中的 hosts 应使用服务名，例如: ["http://es-worldlora:9200"]
# 3. 如果 ES 连接失败，请使用 `docker network inspect starcompass_default` 
#    检查网络配置和容器连接。
# ========================================================================================

@dataclass
class BatchConfig:
    """批处理配置"""
    batch_size: int = 100  # 批次大小 (可调)
    flush_interval: int = 10  # 刷新间隔（秒）(可调)
    max_retries: int = 3
    backoff_factor: float = 2.0
    max_batch_size: int = 1000
    max_queue_size: int = 10000
    retry_delay: int = 5

@dataclass
class ESConfig:
    """Elasticsearch配置"""
    hosts: List[str]
    index_name: str = "worldlora_documents"  # <--- 设置默认索引名称
    username: Optional[str] = None
    password: Optional[str] = None
    use_ssl: bool = False
    verify_certs: bool = True
    timeout: int = 30
    max_retries: int = 3

class ElasticsearchSink(SinkFunction):
    """Elasticsearch数据槽"""

    def __init__(self, 
                 es_config: ESConfig,
                 batch_config: BatchConfig = None):
        # 确保传入的 es_config 的 index_name 优先，否则使用默认值
        self.es_config = es_config
        if not self.es_config.index_name:
            self.es_config.index_name = "worldlora_documents" # 确保有索引名
            
        self.batch_config = batch_config or BatchConfig()
        self.batch: List[Dict] = []
        self.last_flush_time = time.time()
        self.es: Optional[Elasticsearch] = None
        # self.doc_queue = Queue(maxsize=self.batch_config.max_queue_size) # Queue 似乎未使用，注释掉
        self.flush_thread = None
        self.running = True
        self.lock = threading.Lock()

    def open(self, runtime_context):
        """初始化ES连接并检查索引"""
        try:
            self._init_es_connection()
            self._ensure_index() # 仅检查索引，不再尝试创建
            self._start_flush_thread()
            logger.info(f"ES连接建立成功，将写入索引: {self.es_config.index_name}, 主机: {self.es_config.hosts}")
        except Exception as e:
            logger.error(f"ES Sink 初始化失败: {str(e)}")
            logger.error("请确保 Elasticsearch 服务可用，并且索引 '{self.es_config.index_name}' 已通过 setup_es_index.py 创建。")
            raise RuntimeError(f"ES Sink 初始化失败: {e}") from e # 抛出异常，使 Flink 作业失败

    def _init_es_connection(self):
        """初始化ES连接"""
        self.es = Elasticsearch(
            hosts=self.es_config.hosts,
            http_auth=(self.es_config.username, self.es_config.password) if self.es_config.username else None,
            use_ssl=self.es_config.use_ssl,
            verify_certs=self.es_config.verify_certs,
            timeout=self.es_config.timeout,
            max_retries=self.es_config.max_retries
        )
    
    def _start_flush_thread(self):
        """启动刷新线程"""
        self.flush_thread = threading.Thread(target=self._flush_loop)
        self.flush_thread.daemon = True
        self.flush_thread.start()
    
    def _flush_loop(self):
        """定期刷新循环"""
        while self.running:
            try:
                current_time = time.time()
                # 检查是否有数据需要刷新，并且达到时间间隔
                if self.batch and (current_time - self.last_flush_time) >= self.batch_config.flush_interval:
                    self._flush_with_retry()
                # 或者检查是否需要更频繁地刷新，如果队列接近满（这里先简单用时间间隔）
                time.sleep(1) # 减少 CPU 占用
            except Exception as e:
                # 捕获可能的线程中断等异常
                if self.running:
                    logger.error(f"刷新循环异常: {str(e)}")
                else:
                    logger.info("刷新线程正常退出")
                    break # 退出循环

    @backoff.on_exception(backoff.expo, (ConnectionError, TransportError), max_tries=3)
    def _ensure_index(self):
        """确保索引存在"""
        if not self.es.indices.exists(index=self.es_config.index_name):
            # 不再尝试创建索引，而是记录错误并抛出异常
            error_msg = f"目标索引 {self.es_config.index_name} 不存在！请先运行 setup_es_index.py 创建索引和映射。"
            logger.error(error_msg)
            raise ValueError(error_msg) # 抛出异常，导致 open() 失败
        else:
            logger.info(f"确认目标索引 {self.es_config.index_name} 已存在")

    def invoke(self, value, context=None):
        """处理每个文档"""
        try:
            # 假设输入 value 是 JSON 字符串
            doc = json.loads(value) 
            es_doc_action = self._transform_to_es_doc_action(doc)
            
            if es_doc_action:
                with self.lock:
                    self.batch.append(es_doc_action)
                    # 检查是否达到批次大小
                    if len(self.batch) >= self.batch_config.batch_size:
                        self._flush_with_retry()
                
        except json.JSONDecodeError as e:
            logger.error(f"输入数据非有效JSON: {str(e)}, 数据: {value[:200]}...")
        except Exception as e:
            logger.error(f"文档处理失败: {str(e)}, 原始数据: {value[:200]}...")

    def _transform_to_es_doc_action(self, doc: Dict) -> Optional[Dict]:
        """将输入文档转换为 Elasticsearch bulk API 的 action 格式"""
        # 简单的错误检查，可以根据需要扩展
        if not doc or not isinstance(doc, dict):
             logger.warning(f"接收到无效文档: {doc}")
             return None

        # 提取需要的字段，提供默认值以增加健壮性
        doc_id = doc.get('id') # 优先使用 'id' 字段作为 ES 文档 ID
        source = doc.get('source', 'unknown')
        title = doc.get('title', '')
        content = doc.get('content', '')
        timestamp = doc.get('timestamp') # 可以是 ISO 格式字符串或毫秒时间戳
        
        # 如果没有提供 'id'，可以考虑使用其他唯一标识符，或者让 ES 自动生成
        # if not doc_id:
        #    doc_id = generate_unique_id(...) # 例如基于内容哈希
            
        # 构建 _source 部分
        source_data = {
            "id": doc_id, # 也将 id 包含在 _source 中，方便查询
            "source": source,
            "title": title,
            "content": content,
            "timestamp": timestamp
            # 可以添加其他需要索引的字段
        }
        
        # 构建完整的 bulk action
        action = {
            "_index": self.es_config.index_name,
            "_op_type": "index", # 使用 index 操作，如果文档 ID 已存在则更新
            "_source": source_data
        }
        
        # 如果 doc_id 存在，则使用它作为 ES 文档 ID
        if doc_id:
            action["_id"] = str(doc_id) # 确保 ID 是字符串
        # else: 让 ES 自动生成 ID
            
        return action

    @backoff.on_exception(backoff.expo, (ConnectionError, TransportError), max_tries=3)
    def _flush_with_retry(self):
        """带重试机制的批量刷新"""
        batch_to_flush = None
        with self.lock:
            if not self.batch:
                return # 没有数据需要刷新
            # 复制当前批次以进行刷新，并清空实例变量中的批次
            batch_to_flush = self.batch.copy()
            self.batch = [] 
            self.last_flush_time = time.time() # 更新最后刷新时间
        
        if not batch_to_flush:
             return

        try:
            success, failed_info = helpers.bulk(
                self.es,
                batch_to_flush, # 使用复制出来的批次
                chunk_size=min(500, self.batch_config.batch_size), # chunk_size 不应超过 batch_size
                max_retries=self.batch_config.max_retries, # 使用配置的重试次数
                request_timeout=self.es_config.timeout, # 使用配置的超时
                stats_only=False, # 获取详细的失败信息
                raise_on_error=False, # 不立即抛出异常，手动处理失败
                raise_on_exception=False
            )
            
            failed_count = len(failed_info)
            logger.info(f"批量索引完成：成功 {success} 个，失败 {failed_count} 个")
            
            if failed_count > 0:
                # 从 failed_info 提取失败的文档并处理
                failed_docs_to_save = []
                for item in failed_info:
                    # item 结构通常是 {'index': {'_index': '...', '_id': '...', 'status': 4xx/5xx, 'error': {...}, 'data': original_action}}
                    op_type = list(item.keys())[0]
                    original_action = item[op_type].get('data') # 尝试获取原始 action 数据
                    if original_action:
                        failed_docs_to_save.append(original_action)
                    else:
                         logger.warning(f"无法从失败信息中提取原始文档: {item}")
                if failed_docs_to_save:
                     self._handle_failed_documents(failed_docs_to_save)
            
        except (ConnectionError, TransportError) as e:
            logger.error(f"与 Elasticsearch 连接失败，无法批量索引: {str(e)}")
            # 连接错误时，整个批次都失败了
            self._save_failed_batch(batch_to_flush)
        except Exception as e:
            logger.error(f"批量索引时发生未知异常: {str(e)}")
            # 其他未知异常，也保存整个批次
            self._save_failed_batch(batch_to_flush)
    
    def _handle_failed_documents(self, failed_docs: List[Dict]):
        """处理失败的文档 (保存到文件)"""
        if not failed_docs:
            return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f") # 添加毫秒以防文件名冲突
        error_dir = "failed_documents"
        try:
            os.makedirs(error_dir, exist_ok=True)
            error_file = os.path.join(error_dir, f"failed_docs_{timestamp}.json")
            with open(error_file, "w", encoding='utf-8') as f:
                json.dump(failed_docs, f, indent=2, ensure_ascii=False)
            logger.warning(f"{len(failed_docs)} 个失败的文档已保存到: {error_file}")
        except Exception as e:
             logger.error(f"保存失败文档时出错: {e}")

    def _save_failed_batch(self, batch: List[Dict]):
        """保存整个失败的批次 (通常在连接错误时调用)"""
        if not batch:
             return
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        error_dir = "failed_batches"
        try:
            os.makedirs(error_dir, exist_ok=True)
            error_file = os.path.join(error_dir, f"failed_batch_{timestamp}.json")
            with open(error_file, "w", encoding='utf-8') as f:
                json.dump(batch, f, indent=2, ensure_ascii=False)
            logger.error(f"整个失败的批次 ({len(batch)} 个文档) 已保存到: {error_file}")
        except Exception as e:
             logger.error(f"保存失败批次时出错: {e}")

    def close(self):
        """关闭时处理剩余的批次并停止线程"""
        logger.info("关闭 Elasticsearch Sink...")
        self.running = False # 设置标志位停止刷新循环
        
        # 等待刷新线程结束
        if self.flush_thread and self.flush_thread.is_alive():
            logger.info("等待刷新线程完成...")
            self.flush_thread.join(timeout=self.batch_config.flush_interval + 5) # 等待一个刷新周期加额外时间
            if self.flush_thread.is_alive():
                 logger.warning("刷新线程未能在超时时间内结束")

        # 处理关闭前 self.batch 中剩余的文档
        if self.batch: 
            logger.info(f"关闭前刷新剩余的 {len(self.batch)} 个文档...")
            try:
                self._flush_with_retry()
            except Exception as e:
                 logger.error(f"关闭时刷新剩余文档失败: {e}")
                 self._save_failed_batch(self.batch) # 保存最后失败的批次

        # 关闭 Elasticsearch 连接
        if self.es:
            try:
                self.es.close()
                logger.info("Elasticsearch 连接已关闭")
            except Exception as e:
                 logger.error(f"关闭 Elasticsearch 连接时出错: {e}")
        logger.info("Elasticsearch Sink 关闭完成")

# 可以在这里添加一个 main 函数用于本地测试 Sink (可选)
# if __name__ == '__main__':
#     # 创建配置
#     es_conf = ESConfig(hosts=["http://localhost:9200"], index_name="worldlora_documents")
#     batch_conf = BatchConfig(batch_size=5, flush_interval=5)
#     
#     # 创建 Sink 实例
#     sink = ElasticsearchSink(es_conf, batch_conf)
#     
#     # 模拟 Flink RuntimeContext
#     class MockRuntimeContext:
#         def get_task_name(self): return "mock_task"
#         def get_number_of_parallel_subtasks(self): return 1
#         def get_index_of_this_subtask(self): return 0
#         # ... 其他可能需要的方法
#     
#     try:
#         sink.open(MockRuntimeContext()) # 手动调用 open
#         
#         # 模拟发送数据
#         for i in range(12):
#             doc = {
#                 "id": f"test_doc_{i}",
#                 "source": "test_source",
#                 "title": f"Test Document {i}",
#                 "content": f"This is the content for test document {i}.",
#                 "timestamp": datetime.now().isoformat()
#             }
#             sink.invoke(json.dumps(doc))
#             time.sleep(0.5)
#             
#         print("等待最后的刷新...")
#         time.sleep(batch_conf.flush_interval + 2) # 等待超过刷新间隔
#         
#     finally:
#         sink.close() # 手动调用 close
#         print("测试完成") 