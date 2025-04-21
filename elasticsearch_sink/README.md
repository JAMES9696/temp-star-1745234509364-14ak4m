# WorldLoRa Elasticsearch 索引器

这是一个用于将清洗后的文档从 Kafka 索引到 Elasticsearch 的服务。它作为数据管道的最后一步，确保清洗后的文档能够被高效地存储和检索。

## 功能特点

- 从 Kafka 主题 `worldlora.cleaned` 读取清洗后的文档
- 自动创建和配置 Elasticsearch 索引
- 批量索引优化，提高性能
- 完善的错误处理和日志记录
- 优雅的关闭处理

## 环境要求

- Python 3.7+
- Elasticsearch 8.x
- Kafka 集群
- 其他依赖见 requirements.txt

## 安装

1. 创建虚拟环境：
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows
```

2. 安装依赖：
```bash
pip install -r requirements.txt
```

## 运行

1. 确保 Elasticsearch 和 Kafka 服务已启动
2. 运行索引器：
```bash
python -m elasticsearch_sink.src.es_indexer
```

## 配置说明

- Elasticsearch 配置：
  - 主机：`localhost:9200`
  - 索引名：`worldlora_docs`
  - 分片数：3
  - 副本数：1

- Kafka 配置：
  - 输入主题：`worldlora.cleaned`
  - 消费者组：`es-indexer`
  - 服务器：`localhost:9092`

- 批量处理配置：
  - 批量大小：100
  - 超时时间：10秒

## 索引映射

索引使用以下映射配置：

- 文档ID：keyword类型
- 来源信息：keyword类型
- 标题：text类型，带keyword子字段
- 内容：text类型，使用标准分析器
- 时间戳：date类型
- 内容哈希：keyword类型
- 元数据：嵌套对象，包含各种统计信息

## 错误处理

- 使用 Python 的 logging 模块记录处理状态
- 批量索引失败时会记录错误信息
- 支持优雅关闭，确保所有文档都被处理

## 监控

- 可以通过 Elasticsearch 的 API 监控索引状态
- 使用 Kibana 查看索引的统计信息
- 日志记录索引成功和失败的数量

## 性能优化

- 使用批量索引提高吞吐量
- 配置合理的分片和副本数
- 使用超时机制确保及时处理 