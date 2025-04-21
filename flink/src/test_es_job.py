from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.functions import MapFunction, ProcessFunction
from pyflink.common import Types, Row
import json
import random
import logging
from datetime import datetime
from elasticsearch import Elasticsearch
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('test_es_job')

# 测试数据生成器
class TestDataGenerator(MapFunction):
    def __init__(self):
        self.count = 0
        self.topics = ["技术", "科学", "健康", "金融", "教育", "文化", "娱乐", "体育"]
    
    def map(self, value):
        # 忽略输入值，生成新的测试文档
        doc = {
            "id": f"doc_{self.count}",
            "source": f"test_source_{random.randint(1, 5)}",
            "title": f"测试文档 #{self.count} - {random.choice(self.topics)}",
            "content": f"这是一个测试文档的内容，包含了随机文本 {random.randint(1000, 9999)}。" * 3,
            "timestamp": datetime.now().isoformat()
        }
        
        self.count += 1
        logger.info(f"已生成第 {self.count} 个文档")
        
        # 返回文档
        return doc

# Elasticsearch 处理函数
class ESProcessor(ProcessFunction):
    def __init__(self, es_hosts, index_name):
        self.es_hosts = es_hosts
        self.index_name = index_name
        self.es = None
        self.batch_size = 10
        self.batch = []
        self.count = 0
    
    def open(self, runtime_context):
        logger.info(f"连接 Elasticsearch: {self.es_hosts}")
        self.es = Elasticsearch(self.es_hosts)
        
        if not self.es.indices.exists(index=self.index_name):
            logger.error(f"索引 {self.index_name} 不存在！请先运行 setup_es_index.py 创建索引")
            raise ValueError(f"索引 {self.index_name} 不存在！")
        else:
            logger.info(f"索引 {self.index_name} 已存在，准备写入数据")
    
    def process_element(self, doc, ctx):
        # 创建 ES 文档
        es_doc = {
            "id": doc["id"],
            "source": doc["source"],
            "title": doc["title"],
            "content": doc["content"],
            "timestamp": doc["timestamp"]
        }
        
        # 写入 ES
        try:
            result = self.es.index(
                index=self.index_name,
                id=doc["id"],
                body=es_doc
            )
            
            self.count += 1
            logger.info(f"成功写入文档 {doc['id']} 到 ES，总计: {self.count}")
            
            # 每批次后执行刷新
            if self.count % self.batch_size == 0:
                self.es.indices.refresh(index=self.index_name)
                logger.info(f"刷新索引 {self.index_name}")
                
        except Exception as e:
            logger.error(f"写入 ES 失败: {e}, 文档ID: {doc['id']}")
    
    def close(self):
        logger.info("关闭 Elasticsearch 连接")
        if self.es:
            # 最终刷新
            try:
                self.es.indices.refresh(index=self.index_name)
                logger.info(f"最终刷新索引 {self.index_name}")
            except Exception as e:
                logger.error(f"最终刷新失败: {e}")
                
            self.es.close()
        logger.info(f"共写入 {self.count} 条记录到 Elasticsearch")

def main():
    # 创建执行环境
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)  # 使用单并行度简化处理
    
    # 创建有限的数据源
    data_stream = env.from_collection(
        collection=range(20),  # 生成20条测试数据
        type_info=Types.INT()
    ).map(
        TestDataGenerator(),
        output_type=Types.PICKLED_BYTE_ARRAY()  # 返回 Python 对象
    )
    
    # 使用 process 函数处理并写入 ES
    data_stream.process(
        ESProcessor(
            es_hosts=["http://es-worldlora:9200"],
            index_name="worldlora_documents"
        ),
        output_type=Types.PICKLED_BYTE_ARRAY()
    )
    
    # 执行作业
    env.execute("ES测试作业")

if __name__ == "__main__":
    main() 