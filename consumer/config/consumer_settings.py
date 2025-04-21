import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

class ConsumerSettings:
    """消费者配置 - 精密仪器的参数设定"""
    
    # Kafka 设置
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_TOPIC = os.getenv('KAFKA_TOPIC', 'worldlora.capture.raw')
    KAFKA_GROUP_ID = os.getenv('KAFKA_GROUP_ID', 'worldlora-consumer')
    KAFKA_AUTO_OFFSET_RESET = os.getenv('KAFKA_AUTO_OFFSET_RESET', 'earliest')
    
    # PostgreSQL 设置
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = int(os.getenv('DB_PORT', 5432))
    DB_NAME = os.getenv('DB_NAME', 'worldlora_nebula')
    DB_USER = os.getenv('DB_USER', 'worldlora')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'nebula_password')
    
    # 性能设置
    BATCH_SIZE = int(os.getenv('BATCH_SIZE', 50))
    COMMIT_INTERVAL = int(os.getenv('COMMIT_INTERVAL', 1000))  # 毫秒
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    RETRY_DELAY = int(os.getenv('RETRY_DELAY', 5))  # 秒
    
    @property
    def DB_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

# Kafka配置
KAFKA_CONFIG: Dict[str, Any] = {
    'bootstrap_servers': ConsumerSettings.KAFKA_BOOTSTRAP_SERVERS,
    'group_id': ConsumerSettings.KAFKA_GROUP_ID,
    'auto_offset_reset': ConsumerSettings.KAFKA_AUTO_OFFSET_RESET,
    'enable_auto_commit': True,
    'auto_commit_interval_ms': ConsumerSettings.COMMIT_INTERVAL,
    'max_poll_interval_ms': 300000,
    'session_timeout_ms': 10000,
    'heartbeat_interval_ms': 3000
}

# PostgreSQL配置
POSTGRES_CONFIG: Dict[str, Any] = {
    'host': ConsumerSettings.DB_HOST,
    'port': ConsumerSettings.DB_PORT,
    'database': ConsumerSettings.DB_NAME,
    'user': ConsumerSettings.DB_USER,
    'password': ConsumerSettings.DB_PASSWORD
}

# 消费者配置
CONSUMER_CONFIG: Dict[str, Any] = {
    'topics': [ConsumerSettings.KAFKA_TOPIC],
    'batch_size': ConsumerSettings.BATCH_SIZE,
    'max_retries': ConsumerSettings.MAX_RETRIES,
    'retry_delay': ConsumerSettings.RETRY_DELAY,
    'state_file': 'consumer_state.json'
} 