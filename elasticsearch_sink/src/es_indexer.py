from elasticsearch import Elasticsearch, helpers
from kafka import KafkaConsumer
import json
import logging
from datetime import datetime
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ESIndexer")

class ElasticsearchIndexer:
    """Elasticsearch 索引器：将清洗后的文档索引到ES"""
    
    def __init__(self, es_host='http://localhost:9200', kafka_topic='worldlora.cleaned'):
        self.es = Elasticsearch([es_host])
        self.kafka_topic = kafka_topic
        self.index_name = 'worldlora_docs'
        
        # 确保索引存在
        self._ensure_index()
        
    def _ensure_index(self):
        """确保ES索引存在并配置正确"""
        if not self.es.indices.exists(index=self.index_name):
            # 创建索引映射
            mapping = {
                "settings": {
                    "number_of_shards": 3,
                    "number_of_replicas": 1,
                    "analysis": {
                        "analyzer": {
                            "content_analyzer": {
                                "type": "standard",
                                "stopwords": "_english_"
                            }
                        }
                    }
                },
                "mappings": {
                    "properties": {
                        "doc_id": {"type": "keyword"},
                        "source_id": {"type": "keyword"},
                        "source_type": {"type": "keyword"},
                        "url": {"type": "keyword"},
                        "title": {
                            "type": "text",
                            "analyzer": "content_analyzer",
                            "fields": {
                                "keyword": {"type": "keyword", "ignore_above": 256}
                            }
                        },
                        "clean_content": {
                            "type": "text",
                            "analyzer": "content_analyzer"
                        },
                        "capture_timestamp": {"type": "date"},
                        "content_hash": {"type": "keyword"},
                        "meta_extracted": {
                            "properties": {
                                "content_length": {"type": "integer"},
                                "has_title": {"type": "boolean"},
                                "source_reliability": {"type": "float"},
                                "extraction_confidence": {"type": "float"}
                            }
                        }
                    }
                }
            }
            
            self.es.indices.create(index=self.index_name, body=mapping)
            logger.info(f"索引 {self.index_name} 创建成功")
        else:
            logger.info(f"索引 {self.index_name} 已存在")
    
    def run(self):
        """运行索引器"""
        consumer = KafkaConsumer(
            self.kafka_topic,
            bootstrap_servers=['localhost:9092'],
            group_id='es-indexer',
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            auto_offset_reset='latest'
        )
        
        logger.info(f"开始监听 {self.kafka_topic} 主题...")
        
        # 批量处理优化
        batch = []
        batch_size = 100
        batch_timeout = 10  # 秒
        last_batch_time = time.time()
        
        try:
            for message in consumer:
                doc = message.value
                
                # 构建ES文档
                es_doc = {
                    "_index": self.index_name,
                    "_id": doc.get('doc_id'),
                    "_source": doc
                }
                
                batch.append(es_doc)
                
                # 达到批量大小或超时时执行索引
                if len(batch) >= batch_size or (time.time() - last_batch_time) > batch_timeout:
                    self._bulk_index(batch)
                    batch = []
                    last_batch_time = time.time()
        
        except KeyboardInterrupt:
            logger.info("接收到停止信号，正在关闭...")
            if batch:
                self._bulk_index(batch)
            consumer.close()
        
        finally:
            if batch:  # 确保最后的批次被处理
                self._bulk_index(batch)
    
    def _bulk_index(self, batch):
        """批量索引文档"""
        if not batch:
            return
            
        try:
            success, failed = helpers.bulk(self.es, batch, stats_only=True)
            logger.info(f"成功索引 {success} 个文档")
            if failed:
                logger.error(f"索引失败 {failed} 个文档")
        except Exception as e:
            logger.error(f"批量索引失败: {str(e)}")

if __name__ == "__main__":
    indexer = ElasticsearchIndexer()
    indexer.run() 