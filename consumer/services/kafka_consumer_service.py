import json
import time
from typing import List, Dict, Any, Optional
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from ..config.consumer_settings import ConsumerSettings
from ..models.document_model import DocumentModel
from ..services.postgres_service import PostgresService

class KafkaConsumerService:
    """Kafka消费者服务 - 数据管道的核心处理器"""
    
    def __init__(self, settings: ConsumerSettings):
        self.settings = settings
        self.consumer = None
        self.postgres_service = PostgresService(settings)
        self.batch = []
        self.last_commit_time = time.time()
    
    def initialize(self):
        """初始化消费者"""
        self.consumer = KafkaConsumer(
            self.settings.KAFKA_TOPIC,
            bootstrap_servers=self.settings.KAFKA_BOOTSTRAP_SERVERS,
            group_id=self.settings.KAFKA_GROUP_ID,
            auto_offset_reset=self.settings.KAFKA_AUTO_OFFSET_RESET,
            enable_auto_commit=False,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            max_poll_records=self.settings.BATCH_SIZE,
            session_timeout_ms=30000,
            heartbeat_interval_ms=10000
        )
        print(f"[Info] 消费者已连接到主题: {self.settings.KAFKA_TOPIC}")
    
    def process_message(self, message) -> Optional[DocumentModel]:
        """处理单条消息"""
        try:
            data = message.value
            
            # 检查是否为错误消息
            if 'error' in data and 'original_content' not in data:
                print(f"[Warning] 跳过错误消息: {data['error']}")
                return None
            
            # 转换为文档模型
            doc = DocumentModel(**data)
            return doc
        except Exception as e:
            print(f"[Error] 消息处理失败: {str(e)}")
            return None
    
    def should_commit(self) -> bool:
        """判断是否应该提交"""
        return (
            len(self.batch) >= self.settings.BATCH_SIZE or
            (time.time() - self.last_commit_time) * 1000 >= self.settings.COMMIT_INTERVAL
        )
    
    def handle_batch(self):
        """处理批次"""
        if not self.batch:
            return
        
        print(f"[Info] 处理批次，包含 {len(self.batch)} 条消息")
        success, errors = self.postgres_service.batch_save_documents(self.batch)
        
        print(f"[Batch] 成功: {success}, 失败: {errors}")
        
        # 提交偏移量
        self.consumer.commit()
        self.last_commit_time = time.time()
        self.batch.clear()
    
    def run(self):
        """运行消费者服务"""
        print("[Info] Kafka消费者服务启动")
        self.initialize()
        
        try:
            while True:
                # 拉取消息
                messages = self.consumer.poll(timeout_ms=1000)
                
                for tp, msgs in messages.items():
                    for message in msgs:
                        doc = self.process_message(message)
                        if doc:
                            self.batch.append(doc)
                
                # 检查是否需要处理批次
                if self.should_commit():
                    self.handle_batch()
                
                # 即使没有新消息，也检查是否需要基于时间提交
                elif time.time() - self.last_commit_time >= self.settings.COMMIT_INTERVAL / 1000:
                    self.handle_batch()
                    
        except KeyboardInterrupt:
            print("\n[Info] 收到停止信号，准备关闭...")
        except Exception as e:
            print(f"[Critical] 消费者意外退出: {str(e)}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """清理资源"""
        try:
            # 处理剩余批次
            if self.batch:
                self.handle_batch()
            
            # 关闭消费者
            if self.consumer:
                self.consumer.close()
                print("[Info] Kafka消费者已关闭")
        except Exception as e:
            print(f"[Error] 清理过程出错: {str(e)}") 