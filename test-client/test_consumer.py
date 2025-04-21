#!/usr/bin/env python3
import json
from confluent_kafka import Consumer, KafkaError
import psycopg
import uuid
import time

# Kafka消费者配置
consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'worldlora-test-consumer',
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': False
})

# 订阅主题
consumer.subscribe(['worldlora.capture.raw'])

# PostgreSQL连接配置
conn = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="worldlora_nebula",
    user="worldlora",
    password="nebula_password"
)
conn.autocommit = False

# 处理消息
try:
    start_time = time.time()
    timeout = 30  # 30秒后自动退出
    
    while True:
        # 检查是否超时
        if time.time() - start_time > timeout:
            print("达到超时时间，退出消费者")
            break
            
        msg = consumer.poll(1.0)
        
        if msg is None:
            print("等待消息中...")
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                print("已到达分区末尾")
                break
            else:
                print(f"消费者错误: {msg.error()}")
                break
            
        try:
            data = json.loads(msg.value().decode('utf-8'))
            print(f"接收到消息: {msg.topic()} [{msg.partition()}] @ {msg.offset()}")
            
            # 开始事务
            with conn.cursor() as cur:
                # 检查来源是否存在
                cur.execute("SELECT source_id FROM metadata.sources WHERE source_id = %s", 
                            (data.get('source_id'),))
                source_result = cur.fetchone()
                
                # 如果来源不存在，创建一个
                if not source_result:
                    cur.execute("""
                    INSERT INTO metadata.sources (source_id, name, source_type, url_pattern, active)
                    VALUES (%s, %s, %s, %s, %s)
                    """, (
                        data.get('source_id'),
                        "Test Source",
                        "test",
                        "https://example.com/*",
                        True
                    ))
                
                # 检查文档是否已存在（通过内容哈希）
                cur.execute("SELECT doc_id FROM storage.documents WHERE content_hash = %s", 
                            (data.get('content_hash'),))
                doc_result = cur.fetchone()
                
                if doc_result:
                    print(f"文档已存在，ID: {doc_result[0]}")
                else:
                    # 插入新文档
                    doc_id = uuid.uuid4()
                    cur.execute("""
                    INSERT INTO storage.documents 
                    (doc_id, source_id, title, url, content_hash, original_content, visibility, doc_type, metadata)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, (
                        doc_id,
                        data.get('source_id'),
                        data.get('title'),
                        data.get('url'),
                        data.get('content_hash'),
                        data.get('original_content'),
                        'private',
                        'article',
                        json.dumps(data.get('metadata', {}))
                    ))
                    print(f"已插入新文档，ID: {doc_id}")
                
                # 提交事务
                conn.commit()
                
                # 提交Kafka偏移量
                consumer.commit(msg)
            
            print("消息处理完成!")
            break  # 处理完一条消息后退出
            
        except Exception as e:
            print(f"处理消息时出错: {e}")
            conn.rollback()
            
except KeyboardInterrupt:
    print("消费者停止")
finally:
    consumer.close()
    conn.close() 