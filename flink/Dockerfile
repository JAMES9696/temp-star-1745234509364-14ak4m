FROM flink:1.17.0-scala_2.12

USER root

# 安装Python, pip, wget
RUN apt-get update -y && \
    apt-get install -y python3 python3-pip python3-dev build-essential wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 更新pip并创建软链接
RUN pip3 install --no-cache-dir --upgrade pip
RUN ln -sf /usr/bin/python3 /usr/bin/python
RUN ln -sf /usr/bin/pip3 /usr/bin/pip

# 下载 Flink Kafka Connector JAR 及其依赖 (kafka-clients) 到 Flink 的 lib 目录
ARG KAFKA_CONNECTOR_VERSION=3.0.1-1.17
ARG KAFKA_CLIENTS_VERSION=3.3.1
ARG ES7_CONNECTOR_VERSION=3.0.1-1.17
RUN wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-kafka/${KAFKA_CONNECTOR_VERSION}/flink-connector-kafka-${KAFKA_CONNECTOR_VERSION}.jar && \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/kafka/kafka-clients/${KAFKA_CLIENTS_VERSION}/kafka-clients-${KAFKA_CLIENTS_VERSION}.jar && \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-connector-elasticsearch7/${ES7_CONNECTOR_VERSION}/flink-sql-connector-elasticsearch7-${ES7_CONNECTOR_VERSION}.jar

# 安装PyFlink和其他依赖
WORKDIR /tmp
COPY requirements.txt .
RUN pip install --no-cache-dir --default-timeout=600 -vvv -r requirements.txt

# 不再复制或克隆应用代码，代码将通过卷挂载提供
# WORKDIR /opt/flink/usrlib # 设置工作目录，但保持为空
# COPY src/ ./src/
# COPY data_cleaner.py .
# COPY document_cleaner.py .
# COPY __init__.py .
# ARG GIT_REPO_URL="..."
# ARG GIT_BRANCH="..."
# RUN git clone ...

# 设置Python环境变量 （指向将包含挂载代码的目录）
ENV PYFLINK_CLIENT_EXECUTABLE=/usr/bin/python3
ENV PYTHONPATH=/opt/flink/usrlib

# 切换回flink用户
USER flink 