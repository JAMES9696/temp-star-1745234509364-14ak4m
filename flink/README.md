# WorldLoRa Flink 文档清洗框架

这是一个基于 Apache Flink 的文档清洗框架，用于处理从 Kafka 接收的原始文档数据，进行清洗和结构化处理后输出到新的 Kafka 主题。

## 功能特点

- 从 Kafka 主题 `worldlora.capture.raw` 读取原始文档
- 对文档进行深度清洗，包括：
  - HTML 标签清理
  - 文本标准化
  - 时间戳规范化
  - 内容哈希计算
  - 文档结构特征提取
- 过滤不合格的文档
- 将清洗后的文档发送到 Kafka 主题 `worldlora.cleaned`

## 环境要求

- Python 3.7+
- Apache Flink 1.16.0
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

1. 确保 Kafka 服务已启动
2. 运行 Flink 清洗任务：
```bash
python -m flink.data_cleaner
```

## 配置说明

- Kafka 配置：
  - 输入主题：`worldlora.capture.raw`
  - 输出主题：`worldlora.cleaned`
  - 消费者组：`flink-cleaner`
  - 服务器：`localhost:9092`

- Flink 配置：
  - 并行度：2
  - 任务管理器内存：1GB

## 文档处理流程

1. 从 Kafka 读取原始文档
2. 解析 JSON 数据
3. 清洗文档内容：
   - 移除 HTML 标签
   - 清理控制字符
   - 标准化空白字符
4. 提取文档特征：
   - 生成唯一 ID
   - 计算内容哈希
   - 评估来源可靠性
5. 过滤不合格文档
6. 发送清洗后的文档到 Kafka

## 错误处理

- 清洗过程中的错误会被捕获并记录
- 错误文档会被标记为 `status: 'error'`
- 原始内容会被保留在 `raw_content` 字段中

## 监控

- 使用 Python 的 logging 模块记录处理状态
- 可以通过 Kafka UI 监控消息流
- 清洗后的文档包含处理状态和元数据信息 