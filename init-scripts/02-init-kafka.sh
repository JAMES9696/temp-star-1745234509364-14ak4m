#!/bin/bash
set -e

# 等待Kafka启动
sleep 20

# 创建主题
echo "Creating Kafka topics..."

# 数据采集主题
kafka-topics --create --if-not-exists --topic worldlora.capture.raw --bootstrap-server kafka:29092 --partitions 3 --replication-factor 1

# 处理主题
kafka-topics --create --if-not-exists --topic worldlora.processing.clean --bootstrap-server kafka:29092 --partitions 3 --replication-factor 1
kafka-topics --create --if-not-exists --topic worldlora.processing.entity --bootstrap-server kafka:29092 --partitions 3 --replication-factor 1
kafka-topics --create --if-not-exists --topic worldlora.processing.embedding --bootstrap-server kafka:29092 --partitions 3 --replication-factor 1

# 存储主题
kafka-topics --create --if-not-exists --topic worldlora.storage.document --bootstrap-server kafka:29092 --partitions 3 --replication-factor 1

# 错误主题
kafka-topics --create --if-not-exists --topic worldlora.dlq --bootstrap-server kafka:29092 --partitions 1 --replication-factor 1

# 日志主题
kafka-topics --create --if-not-exists --topic worldlora.logs --bootstrap-server kafka:29092 --partitions 1 --replication-factor 1

# Kafka Connect 内部主题
echo "Creating Kafka Connect internal topics..."
kafka-topics --create --if-not-exists --topic docker-connect-configs --bootstrap-server kafka:29092 --partitions 1 --replication-factor 1 --config cleanup.policy=compact
kafka-topics --create --if-not-exists --topic docker-connect-offsets --bootstrap-server kafka:29092 --partitions 25 --replication-factor 1 --config cleanup.policy=compact
kafka-topics --create --if-not-exists --topic docker-connect-status --bootstrap-server kafka:29092 --partitions 5 --replication-factor 1 --config cleanup.policy=compact

echo "Kafka topics created successfully!" 