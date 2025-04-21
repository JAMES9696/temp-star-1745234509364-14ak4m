from prometheus_client import start_http_server, Gauge
import time
import psycopg2
from dotenv import load_dotenv
import os
import requests
from kafka import KafkaAdminClient
from typing import Dict

# 加载环境变量
load_dotenv()

# 定义指标
db_connection_status = Gauge('db_connection_status', '数据库连接状态')
query_execution_time = Gauge('query_execution_time_seconds', '查询执行时间')
active_connections = Gauge('active_connections', '活动连接数')

class SystemMetricsCollector:
    """系统指标收集器 - 全知全能的数据之眼"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.metrics = {}
        self._init_metrics()
    
    def _init_metrics(self):
        """初始化Prometheus指标"""
        # Kafka指标
        self.metrics['kafka_lag'] = Gauge('worldlora_kafka_lag', 'Kafka消费延迟', ['topic', 'partition'])
        self.metrics['kafka_msg_sec'] = Gauge('worldlora_kafka_messages_per_second', 'Kafka消息/秒')
        
        # PostgreSQL指标
        self.metrics['pg_write_latency'] = Gauge('worldlora_pg_write_latency_ms', 'PostgreSQL写入延迟(ms)')
        self.metrics['document_count'] = Gauge('worldlora_document_count', '文档总数')
        self.metrics['error_count'] = Gauge('worldlora_error_count', '错误数量')
        
        # 爬虫指标
        self.metrics['crawler_success_rate'] = Gauge('worldlora_crawler_success_rate', '爬虫成功率')
        self.metrics['crawler_active_count'] = Gauge('worldlora_crawler_active_count', '活跃爬虫数量')
    
    def collect_kafka_metrics(self):
        """收集Kafka指标 - 开发阶段需要容错处理"""
        try:
            admin_client = KafkaAdminClient(
                bootstrap_servers=self.config['kafka_bootstrap_servers']
            )
            
            try:
                # 基础连接性检查
                topics = admin_client.list_topics()
                self.metrics['kafka_msg_sec'].set(len(topics))  # 开发阶段使用主题数量作为占位
                
                # 消费者组延迟检查 - 开发阶段可选
                try:
                    consumer_groups = admin_client.list_consumer_groups()
                    for group in consumer_groups:
                        group_id = group[0]  # 元组的第一个元素是group_id
                        
                        # 获取消费者组详情
                        offsets = admin_client.list_consumer_group_offsets(group_id)
                        if offsets:
                            for tp, offset in offsets.items():
                                if offset.offset > 0:  # 只记录有效的偏移量
                                    self.metrics['kafka_lag'].labels(
                                        topic=tp.topic,
                                        partition=tp.partition
                                    ).set(0)  # 开发阶段默认设置为0
                except Exception as group_err:
                    print(f"消费者组指标收集跳过（开发阶段）: {group_err}")
                    # 开发阶段：设置默认值而不是失败
                    self.metrics['kafka_lag'].labels(
                        topic='development',
                        partition=0
                    ).set(0)
            
            finally:
                try:
                    admin_client.close()
                except Exception as close_err:
                    print(f"关闭Kafka管理客户端出错（非致命）: {close_err}")
                
        except Exception as e:
            print(f"Kafka指标收集基础错误（开发阶段）: {e}")
            # 开发阶段：设置默认值以保持指标连续性
            self.metrics['kafka_msg_sec'].set(0)
            self.metrics['kafka_lag'].labels(
                topic='development',
                partition=0
            ).set(0)
    
    def collect_postgres_metrics(self):
        """收集PostgreSQL指标"""
        try:
            conn = psycopg2.connect(**self.config['postgres'])
            with conn.cursor() as cur:
                # 文档总数
                cur.execute("SELECT COUNT(*) FROM storage.documents")
                count = cur.fetchone()[0]
                self.metrics['document_count'].set(count)
                
                # 错误数量
                cur.execute("SELECT COUNT(*) FROM storage.documents WHERE metadata->>'type' = 'error'")
                error_count = cur.fetchone()[0]
                self.metrics['error_count'].set(error_count)
                
                # 写入延迟（示例）
                start_time = time.time()
                cur.execute("SELECT 1")
                latency = (time.time() - start_time) * 1000
                self.metrics['pg_write_latency'].set(latency)
        except Exception as e:
            print(f"收集PostgreSQL指标失败: {e}")
    
    def collect_crawler_metrics(self):
        """收集爬虫指标"""
        try:
            # 这里需要实现更具体的爬虫指标收集逻辑
            self.metrics['crawler_active_count'].set(0)  # 占位值
            self.metrics['crawler_success_rate'].set(0.95)  # 占位值
        except Exception as e:
            print(f"收集爬虫指标失败: {e}")
    
    def run_collector(self, port=8001, interval=15):
        """运行指标收集器
        
        Args:
            port (int): Prometheus指标服务端口
            interval (int): 指标收集间隔（秒）
        """
        start_http_server(port)  # 启动Prometheus指标服务
        print(f"指标服务器已启动在端口 {port}")
        
        while True:
            self.collect_kafka_metrics()
            self.collect_postgres_metrics()
            self.collect_crawler_metrics()
            time.sleep(interval)  # 每x秒收集一次

def check_db_connection():
    """检查数据库连接状态"""
    try:
        conn = psycopg2.connect(
            dbname=os.getenv('DB_NAME', 'worldlora_nebula'),
            user=os.getenv('DB_USER', 'worldlora'),
            password=os.getenv('DB_PASSWORD', 'nebula_password'),
            host=os.getenv('DB_HOST', 'postgres'),
            port=os.getenv('DB_PORT', '5432')
        )
        conn.close()
        db_connection_status.set(1)
    except Exception as e:
        print(f"数据库连接错误: {str(e)}")
        db_connection_status.set(0)

def collect_metrics():
    """收集指标"""
    while True:
        check_db_connection()
        time.sleep(15)  # 每15秒收集一次指标

def start_metrics_server(port=8000):
    """启动指标服务器"""
    start_http_server(port)
    print(f"指标服务器已启动在端口 {port}")
    collect_metrics() 