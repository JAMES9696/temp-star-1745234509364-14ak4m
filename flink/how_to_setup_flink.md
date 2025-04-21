# 如何设置完整的Flink环境

要正确运行完整的Flink作业（包括Kafka连接器），你需要确保有必要的Java依赖。以下是详细步骤：

## 问题诊断

我们之前遇到的错误：
```
TypeError: Could not found the Java class 'org.apache.flink.streaming.connectors.kafka.FlinkKafkaConsumer'. The Java dependencies could be specified via command line argument '--jarfile' or the config option 'pipeline.jars'
```

这个错误表明缺少Flink Kafka连接器的Java JAR文件。PyFlink只是Python API，底层仍然需要Java依赖。

## 解决方案

### 方法1：下载并添加JAR文件（本地开发环境）

1. **创建一个jars目录**:
   ```powershell
   mkdir -p flink/jars
   ```

2. **下载必要的JAR文件**:
   - 访问[Maven中央仓库](https://repo.maven.apache.org/maven2/org/apache/flink/)
   - 下载以下JAR文件到`flink/jars`目录：
     - flink-connector-kafka_{scala_version}-{flink_version}.jar (例如：flink-connector-kafka_2.12-1.19.1.jar)
     - flink-json-{flink_version}.jar (例如：flink-json-1.19.1.jar)
     - kafka-clients-{version}.jar (例如：kafka-clients-3.3.1.jar)

3. **修改data_cleaner.py中的配置**:
   ```python
   # 配置Flink环境
   config = Configuration()
   config.set_string("python.client.executable", "python3")
   config.set_string("taskmanager.memory.process.size", "1g")
   
   # 添加JAR文件
   jar_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "jars")
   jars = [os.path.join(jar_path, jar_file) for jar_file in os.listdir(jar_path) if jar_file.endswith('.jar')]
   config.set_string("pipeline.jars", ";".join(jars))
   
   env = StreamExecutionEnvironment.get_execution_environment(configuration=config)
   ```

### 方法2：使用完整的Flink Docker镜像（推荐）

1. **修改docker-compose.yml**，添加或更新Flink服务：
   ```yaml
   jobmanager:
     image: apache/flink:1.19.1
     ports:
       - "8081:8081"
     volumes:
       - ./flink:/opt/flink/usrlib
     environment:
       - JOB_MANAGER_RPC_ADDRESS=jobmanager

   taskmanager:
     image: apache/flink:1.19.1
     depends_on:
       - jobmanager
     volumes:
       - ./flink:/opt/flink/usrlib
     environment:
       - JOB_MANAGER_RPC_ADDRESS=jobmanager
   ```

2. **启动Docker服务**:
   ```powershell
   docker compose up -d
   ```

3. **在容器内运行Flink作业**:
   ```powershell
   docker compose exec taskmanager bash
   cd /opt/flink/usrlib
   # 修改data_cleaner.py中的主机地址为容器名
   python data_cleaner.py
   ```

## 临时解决方案

为了测试Elasticsearch Sink功能，我已创建了一个不依赖Kafka的简化版测试程序：`flink/test_es_sink.py`

你可以使用以下命令运行它：
```powershell
python flink/test_es_sink.py
```

这将直接测试ElasticsearchSink，而不需要完整的Flink环境和Kafka依赖。

## 后续步骤

1. 运行测试程序验证ElasticsearchSink功能
2. 按照上述方法之一设置完整的Flink环境
3. 更新data_cleaner.py中的配置，根据你的运行环境选择合适的主机名 