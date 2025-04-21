# WorldLoRa 数据处理平台

这是一个完整的数据处理平台，包含文档清洗、索引和搜索功能。系统使用 Flink 进行流处理，Elasticsearch 进行文档存储和搜索。

## 系统架构

- **数据采集**：通过爬虫获取原始文档
- **数据清洗**：使用 Flink 进行流处理
- **数据存储**：使用 Elasticsearch 存储和索引文档
- **数据检索**：通过 Elasticsearch 提供搜索功能

## 环境要求

- Docker 和 Docker Compose
- Python 3.7+
- 至少 4GB 可用内存

## 安装

1. 克隆仓库：
```bash
git clone <repository-url>
cd worldlora
```

2. 创建虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行

1. 启动基础服务：
```bash
docker-compose up -d
```

2. 启动 Flink 清洗任务：
```bash
docker-compose exec flink-jobmanager flink run -py /opt/flink/usrlib/data_cleaner.py
```

3. 启动 Elasticsearch 索引器：
```bash
python -m elasticsearch_sink.src.es_indexer
```

## 配置说明

### Flink 配置
- 版本：1.17.0
- JobManager 端口：8081
- 任务并行度：2
- 内存配置：1GB

### Elasticsearch 配置
- 版本：8.x
- 内存：2GB
- 集群名称：worldlora-cluster
- 数据卷：es-data

### Kafka 配置
- 输入主题：worldlora.capture.raw
- 输出主题：worldlora.cleaned
- 消费者组：flink-cleaner, es-indexer

## 监控

- Flink Web UI：http://localhost:8081
- Elasticsearch：http://localhost:9200
- Kibana：http://localhost:5601

## 数据流程

1. 爬虫将原始文档发送到 Kafka 主题 `worldlora.capture.raw`
2. Flink 清洗任务读取原始文档，进行清洗和结构化
3. 清洗后的文档发送到 Kafka 主题 `worldlora.cleaned`
4. Elasticsearch 索引器读取清洗后的文档，索引到 Elasticsearch
5. 用户可以通过 Kibana 或自定义前端进行搜索

## 性能优化

- Flink 使用批量处理提高吞吐量
- Elasticsearch 配置了合理的分片和副本
- 使用 Docker 卷持久化数据
- 优化了内存配置

## 错误处理

- Flink 任务包含完善的错误处理
- Elasticsearch 索引器支持批量重试
- 所有组件都有详细的日志记录

## 扩展建议

- 添加更多的文档处理功能
- 实现文档分类和标签
- 添加用户认证和授权
- 集成监控和告警系统 