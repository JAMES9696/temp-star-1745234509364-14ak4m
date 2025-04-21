#!/usr/bin/env python3
import json
import uuid
import hashlib
from datetime import datetime
from confluent_kafka import Producer

# 配置Kafka生产者
producer = Producer({
    'bootstrap.servers': 'localhost:9092'
})

# 模拟捕获到的文档
test_document = {
    "source_id": str(uuid.uuid4()),
    "url": "https://example.com/test-article",
    "title": "测试文章：星际罗盘系统架构",
    "original_content": """
    这是一篇测试文章，用于验证星际罗盘·WorldLoRa Nebula系统的基本功能。
    
    星际罗盘是一个知识管理系统，旨在捕获、处理、存储和可视化各种信息源的数据。
    
    该系统使用Kafka进行事件流处理，PostgreSQL进行关系数据存储，以及其他技术组件。
    """,
    "content_hash": "",
    "capture_timestamp": datetime.now().isoformat(),
    "metadata": {
        "type": "article",
        "language": "zh-CN",
        "estimated_reading_time": 1
    }
}

# 计算内容哈希
content_hash = hashlib.sha256(test_document["original_content"].encode('utf-8')).hexdigest()
test_document["content_hash"] = content_hash

# 发送回调函数
def delivery_report(err, msg):
    if err is not None:
        print(f'消息发送失败: {err}')
    else:
        print(f'消息发送成功! Topic: {msg.topic()}, Partition: {msg.partition()}, Offset: {msg.offset()}')

# 发送到Kafka
producer.produce(
    'worldlora.capture.raw',
    json.dumps(test_document).encode('utf-8'),
    callback=delivery_report
)

# 等待所有消息发送完成
producer.flush() 