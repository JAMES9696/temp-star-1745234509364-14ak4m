import json
import time
import asyncio
import hashlib
import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from kafka import KafkaProducer
from kafka.errors import KafkaError, KafkaTimeoutError
from ..config.settings import CrawlerSettings

class KafkaProducerManager:
    """
    Kafka生产者管理器 - 负责将捕获的猎物安全送达仓库
    """
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, bootstrap_servers: Optional[str] = None):
        if not hasattr(self, 'initialized'):
            self.settings = CrawlerSettings()
            self.bootstrap_servers = bootstrap_servers or self.settings.KAFKA_BOOTSTRAP_SERVERS
            self.producer = self._create_producer()
            self.initialized = True
    
    def _create_producer(self) -> KafkaProducer:
        """创建Kafka生产者实例"""
        return KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v, ensure_ascii=False).encode('utf-8'),
            retries=self.settings.MAX_RETRIES,
            acks='all',
            compression_type='gzip',  # 使用gzip压缩
            batch_size=16384,  # 16KB的批次大小
            linger_ms=100,  # 等待100ms收集更多消息
            buffer_memory=33554432,  # 32MB的缓冲区
            max_block_ms=60000  # 最大阻塞1分钟
        )
    
    def ensure_message_structure(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """确保消息结构完整性"""
        required_fields = {
            'source_id': str(uuid.uuid4()),
            'url': '',
            'title': '无标题',
            'original_content': '',
            'capture_timestamp': datetime.now().isoformat(),
            'metadata': {}
        }
        
        # 合并默认值和实际数据
        structured_message = {**required_fields, **message}
        
        # 计算内容哈希（如果还未计算）
        if 'content_hash' not in structured_message:
            content = structured_message.get('original_content', '')
            structured_message['content_hash'] = hashlib.sha256(
                content.encode('utf-8')
            ).hexdigest()
        
        return structured_message
    
    async def send_message(self, topic: str, message: Dict[str, Any], retries: int = None):
        """
        发送消息到指定主题
        
        Args:
            topic: Kafka主题
            message: 要发送的消息
            retries: 重试次数，如果为None则使用配置中的值
            
        Returns:
            bool: 发送是否成功
        """
        retries = retries if retries is not None else self.settings.MAX_RETRIES
        last_error = None
        
        for attempt in range(retries + 1):
            try:
                if attempt > 0:
                    # 使用指数退避策略
                    wait_time = self.settings.BACKOFF_FACTOR * (2 ** (attempt - 1))
                    print(f"第 {attempt} 次重试，等待 {wait_time} 秒...")
                    await asyncio.sleep(wait_time)
                
                # 确保消息结构完整
                structured_message = self.ensure_message_structure(message)
                structured_message['kafka_send_timestamp'] = int(time.time() * 1000)
                
                # 发送消息
                future = self.producer.send(topic, structured_message)
                result = future.get(timeout=10)
                
                print(f"消息发送成功! Topic: {result.topic}, Partition: {result.partition}, Offset: {result.offset}")
                return True
                
            except KafkaTimeoutError as e:
                last_error = e
                print(f"发送超时 (尝试 {attempt + 1}/{retries + 1}): {str(e)}")
                continue
                
            except KafkaError as e:
                last_error = e
                print(f"Kafka错误 (尝试 {attempt + 1}/{retries + 1}): {str(e)}")
                continue
                
            except Exception as e:
                print(f"未预期的错误: {str(e)}")
                return False
        
        if last_error:
            print(f"发送失败，重试次数耗尽: {str(last_error)}")
            return False
        return True
    
    async def close(self):
        """关闭生产者，确保所有消息都已发送"""
        if hasattr(self, 'producer'):
            try:
                # 刷新所有待发送的消息
                self.producer.flush(timeout=30)
                print("所有消息已刷新到Kafka")
            except Exception as e:
                print(f"刷新消息时出错: {str(e)}")
            finally:
                # 关闭生产者
                self.producer.close(timeout=30)
                print("Kafka生产者已关闭") 