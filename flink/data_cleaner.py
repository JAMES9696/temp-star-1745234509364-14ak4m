from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.datastream.connectors.kafka import FlinkKafkaConsumer
# 导入官方 Elasticsearch Sink 相关类
from pyflink.datastream.connectors.elasticsearch import Elasticsearch7SinkBuilder, ElasticsearchEmitter, ActionRequestFailureHandler, FlushBackoffType
from pyflink.datastream.functions import RuntimeContext
from pyflink.common import Configuration, Types
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.functions import MapFunction, FilterFunction
import json
import re
import os
from datetime import datetime
from bs4 import BeautifulSoup
import logging
import hashlib
from typing import Dict, Any, Iterable
import time # 确保导入 time

# ========================================================================================
# 网络配置更新说明：
# 1. 已删除旧的 worldlora-flink-taskmanager-1 和 worldlora-flink-jobmanager-1 容器
# 2. 确保当前使用 starcompass-flink-* 容器，它们在 starcompass_worldlora-net 网络中
# 3. Elasticsearch 容器 (es-worldlora) 已连接到 starcompass_worldlora-net 网络
# 4. Kafka 连接使用 kafka:29092 (Docker 内部地址)
# 5. Elasticsearch 连接使用 es-worldlora:9200 (Docker 内部地址)
# ========================================================================================

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DocumentCleaner")

# 自动下载所需的JAR文件
def ensure_kafka_jars():
    """确保Kafka连接器的JAR文件可用"""
    jar_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jars")
    os.makedirs(jar_dir, exist_ok=True)
    
    required_jars = [
        "flink-connector-kafka",
        "flink-json",
        "kafka-clients"
    ]
    
    logger.info(f"查找JAR文件: {jar_dir}")
    if os.path.exists(jar_dir):
        jar_files = [f for f in os.listdir(jar_dir) if f.endswith('.jar')]
        logger.info(f"发现JAR文件: {jar_files}")
    
    flink_lib = "/opt/flink/lib"
    if os.path.exists(flink_lib):
        logger.info(f"检测到Flink容器环境，将使用内置JAR文件: {flink_lib}")
        return []
    
    jar_list = []
    if os.path.exists(jar_dir):
        for jar_file in os.listdir(jar_dir):
            if jar_file.endswith('.jar'):
                jar_list.append(os.path.join(jar_dir, jar_file))
    
    return jar_list

class DocumentCleanerFunction(MapFunction):
    """文档清洗函数：将原始爬取数据转化为结构化文档"""
    
    def __init__(self):
        self.html_pattern = re.compile('<.*?>')
        self.whitespace_pattern = re.compile(r'\s+')
        self.control_chars = re.compile(r'[\x00-\x1F\x7F-\x9F]')
    
    def map(self, raw_message):
        try:
            doc = json.loads(raw_message)
            cleaned_doc = {
                'doc_id': self._generate_id(doc),
                'source_id': doc.get('source_id', 'unknown'),
                'source_type': doc.get('source_type', 'unknown'),
                'url': doc.get('url', ''),
                'capture_timestamp': self._normalize_timestamp(doc.get('capture_timestamp')),
                'metadata': doc.get('metadata', {}),
                'status': 'cleaned'
            }
            if 'content' in doc:
                cleaned_doc['raw_content'] = doc['content']
                cleaned_doc['clean_content'] = self._clean_content(doc['content'])
                cleaned_doc['content_hash'] = self._content_hash(cleaned_doc['clean_content'])
            if 'title' in doc:
                cleaned_doc['title'] = self._clean_text(doc['title'])
            cleaned_doc['meta_extracted'] = self._extract_document_structure(cleaned_doc)
            logger.info(f"成功清洗文档: {cleaned_doc['doc_id']}")
            return json.dumps(cleaned_doc)
        except Exception as e:
            logger.error(f"清洗失败: {str(e)}, 原始消息: {raw_message[:100]}...")
            error_doc = {
                'doc_id': hashlib.md5(raw_message.encode()).hexdigest(),
                'status': 'error',
                'error_message': str(e),
                'raw_content': raw_message,
                'timestamp': datetime.now().isoformat()
            }
            return json.dumps(error_doc)

    def _generate_id(self, doc):
        """生成文档唯一ID"""
        unique_key = f"{doc.get('url', '')}-{doc.get('capture_timestamp', '')}"
        return hashlib.sha256(unique_key.encode()).hexdigest()[:12]

    def _clean_content(self, content):
        """深度清洗内容"""
        if not content:
            return ""
        soup = BeautifulSoup(content, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
        text = soup.get_text()
        text = self.control_chars.sub(' ', text)
        text = self.whitespace_pattern.sub(' ', text)
        return text.strip()

    def _clean_text(self, text):
        """清理普通文本"""
        if not text:
            return ""
        text = self.control_chars.sub(' ', text)
        return self.whitespace_pattern.sub(' ', text).strip()

    def _normalize_timestamp(self, timestamp):
        """统一时间戳格式"""
        if not timestamp:
            return datetime.now().isoformat()
        if isinstance(timestamp, str):
            try:
                return datetime.fromisoformat(timestamp).isoformat()
            except ValueError:
                try:
                    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").isoformat()
                except:
                    return datetime.now().isoformat()
        return timestamp

    def _content_hash(self, content):
        """计算内容哈希，用于去重"""
        if not content:
            return None
        return hashlib.md5(content.encode()).hexdigest()

    def _extract_document_structure(self, doc):
        """提取文档结构特征"""
        structure_meta = {
            'content_length': len(doc.get('clean_content', '')),
            'has_title': bool(doc.get('title')),
            'source_reliability': self._assess_source_reliability(doc),
            'extraction_confidence': 0.95 if doc.get('status') == 'cleaned' else 0.5
        }
        return structure_meta

    def _assess_source_reliability(self, doc):
        """评估来源可靠性"""
        source_id = doc.get('source_id', '').lower()
        if 'zhihu' in source_id:
            return 0.85
        elif 'wechat' in source_id:
            return 0.75
        return 0.5

class DocumentFilterFunction(FilterFunction):
    """过滤掉不合格的文档"""
    
    def filter(self, cleaned_doc_json):
        try:
            doc = json.loads(cleaned_doc_json)
            
            # 过滤规则：必须有有效内容，且不是错误文档
            if doc.get('status') == 'error':
                return False
            
            if not doc.get('clean_content', '').strip():
                return False
            
            # 内容长度检查
            if len(doc.get('clean_content', '')) < 10:
                return False
            
            return True
            
        except:
            return False

# --- 新增 ElasticsearchEmitter 实现 ---
class DocumentElasticsearchEmitter(ElasticsearchEmitter):
    """将清洗后的文档JSON转换为Elasticsearch索引请求"""

    def open(self, runtime_context: RuntimeContext):
        # 初始化（如果需要）
        pass

    def emit(self, element: str, runtime_context: RuntimeContext, indexer):
        try:
            doc = json.loads(element)
            # 确保 status 不是 error
            if doc.get('status') == 'error':
                logger.warning(f"跳过错误文档: {doc.get('doc_id')}")
                return

            # 获取文档ID和源数据
            doc_id = doc.get('doc_id', doc.get('content_hash'))
            if not doc_id:
                logger.warning(f"文档缺少有效ID，跳过: {element[:100]}...")
                return

            # 移除可能不需要直接索引的字段
            source_doc = doc.copy()
            source_doc.pop('raw_content', None)
            source_doc.pop('status', None)
            source_doc.pop('error_message', None)
            source_doc.pop('doc_id', None) # _id 已经在外部指定
            source_doc.pop('content_hash', None)

            # 创建索引请求
            indexer.add_index_request(index="worldlora_documents",  # 目标索引
                                      id=str(doc_id),             # 文档ID
                                      source=source_doc)          # 文档内容
        except json.JSONDecodeError:
            logger.error(f"无法解析JSON文档: {element[:200]}...")
        except Exception as e:
            logger.error(f"处理文档时出错: {element[:200]}... Error: {e}")

    def close(self):
        # 清理资源（如果需要）
        pass

# --- 默认的失败处理器 (可以自定义) ---
class SimpleFailureHandler(ActionRequestFailureHandler):
    def on_failure(self, action, failure, rest_status_code, indexer):
        logger.error(f"Elasticsearch请求失败: Status={rest_status_code}, Action={action}, Failure={failure}")
        # 可以选择抛出异常停止作业，或记录后继续
        # raise failure

def create_flink_job():
    """创建并配置Flink任务"""
    
    jar_files = ensure_kafka_jars()
    
    config = Configuration()
    config.set_string("taskmanager.memory.process.size", "1g")
    
    if jar_files:
        jar_path_str = ";".join(jar_files)
        logger.info(f"设置本地JAR路径: {jar_path_str}")
        config.set_string("pipeline.jars", jar_path_str)
    
    env = StreamExecutionEnvironment.get_execution_environment(configuration=config)
    env.set_parallelism(2)
    
    is_docker = os.path.exists("/opt/flink")
    logger.info(f"检测环境 - Docker容器: {is_docker}")
    
    if is_docker:
        kafka_host = "kafka:29092"
        es_hosts_str = ["http://es-worldlora:9200"]
    else:
        kafka_host = "localhost:9092"
        es_hosts_str = ["http://localhost:9200"]
        
    logger.info(f"使用Kafka地址: {kafka_host}")
    logger.info(f"使用ES地址: {es_hosts_str}")
    
    kafka_props = {
        'bootstrap.servers': kafka_host,
        'group.id': 'flink-cleaner-v2',
        'auto.offset.reset': 'latest'
    }
    
    kafka_consumer = FlinkKafkaConsumer(
        topics='worldlora.capture.raw',
        deserialization_schema=SimpleStringSchema(),
        properties=kafka_props
    )
    
    raw_stream = env.add_source(kafka_consumer)
    
    cleaned_stream = raw_stream \
        .map(DocumentCleanerFunction(), output_type=Types.STRING()) \
        .filter(DocumentFilterFunction())
        
    es_sink = Elasticsearch7SinkBuilder() \
        .set_hosts(es_hosts_str) \
        .set_emitter(DocumentElasticsearchEmitter()) \
        .set_bulk_flush_max_actions(100) \
        .set_bulk_flush_interval(10 * 1000) \
        .set_failure_handler(SimpleFailureHandler()) \
        .set_bulk_flush_backoff_strategy(FlushBackoffType.EXPONENTIAL, 3, 1000) \
        .build()
        
    cleaned_stream.sink_to(es_sink).name("Elasticsearch Sink")
    
    env.execute("WorldLoRa Document Cleaner (Official ES Sink)")

if __name__ == "__main__":
    create_flink_job() 