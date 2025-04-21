@echo off
REM 这个批处理脚本用于设置和运行Flink数据处理任务

echo 设置环境...

REM 创建jars目录（如果不存在）
if not exist jars mkdir jars
echo JAR目录已创建: jars

REM 检查是否有必要的JAR文件
echo 检查必要的JAR文件...
set has_all_jars=1

if not exist jars\flink-connector-kafka*.jar (
    echo 缺少 flink-connector-kafka JAR
    echo 请从 https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-kafka_2.12-1.19.1/ 下载
    set has_all_jars=0
)

if not exist jars\flink-json*.jar (
    echo 缺少 flink-json JAR
    echo 请从 https://repo.maven.apache.org/maven2/org/apache/flink/flink-json-1.19.1/ 下载
    set has_all_jars=0
)

if not exist jars\kafka-clients*.jar (
    echo 缺少 kafka-clients JAR
    echo 请从 https://repo.maven.apache.org/maven2/org/apache/kafka/kafka-clients/3.3.1/ 下载
    set has_all_jars=0
)

REM 选择测试模式
echo.
echo 请选择要运行的测试:
echo 1. 仅测试 ElasticsearchSink（不需要JAR文件）
echo 2. 运行完整的Flink作业（需要JAR文件）
echo 3. 在Docker容器中运行（如果有Docker环境）

set /p test_mode="请输入选项 (1/2/3): "

if "%test_mode%"=="1" (
    echo 运行 ElasticsearchSink 测试...
    python test_es_sink.py
    goto end
)

if "%test_mode%"=="2" (
    if "%has_all_jars%"=="0" (
        echo 缺少必要的JAR文件，无法运行完整作业。
        echo 请先下载缺少的JAR文件到jars目录。
        goto end
    )
    echo 运行完整的Flink作业...
    python data_cleaner.py
    goto end
)

if "%test_mode%"=="3" (
    echo 检查Docker环境...
    docker --version > nul 2>&1
    if %errorlevel% neq 0 (
        echo Docker未安装或未运行。
        goto end
    )
    
    echo 查看正在运行的Docker容器...
    docker ps
    
    echo.
    echo 请确保taskmanager容器正在运行。
    echo 在容器中执行以下命令:
    echo   docker compose exec taskmanager bash
    echo   cd /opt/flink/usrlib
    echo   python data_cleaner.py
    
    set /p run_docker="是否尝试在Docker中运行? (y/n): "
    if "%run_docker%"=="y" (
        docker compose exec taskmanager python /opt/flink/usrlib/data_cleaner.py
    )
    goto end
)

echo 无效的选项!

:end
echo 完成!
pause 