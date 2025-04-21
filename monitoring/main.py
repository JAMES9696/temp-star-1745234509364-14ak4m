import click
from .cli.query_tool import cli as query_cli
from .prometheus.metrics_collector import SystemMetricsCollector
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

@click.group()
def main():
    """星际罗盘监控系统 - 洞察一切的数据之眼"""
    pass

@main.command()
@click.option('--port', '-p', default=8001, help='Prometheus指标服务端口')
@click.option('--interval', '-i', default=15, help='指标收集间隔（秒）')
def monitor(port, interval):
    """启动Prometheus监控"""
    config = {
        'kafka_bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
        'postgres': {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': int(os.getenv('DB_PORT', '5432')),
            'database': os.getenv('DB_NAME', 'worldlora_nebula'),
            'user': os.getenv('DB_USER', 'worldlora'),
            'password': os.getenv('DB_PASSWORD', 'nebula_password')
        }
    }
    
    click.echo(f"启动监控服务在端口 {port}...")
    click.echo(f"指标收集间隔: {interval}秒")
    
    collector = SystemMetricsCollector(config)
    collector.run_collector(port=port, interval=interval)

@main.command()
def status():
    """显示系统状态概览"""
    click.echo("\n=== 系统状态概览 ===")
    
    # 检查数据库连接
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=int(os.getenv('DB_PORT', '5432')),
            database=os.getenv('DB_NAME', 'worldlora_nebula'),
            user=os.getenv('DB_USER', 'worldlora'),
            password=os.getenv('DB_PASSWORD', 'nebula_password')
        )
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM storage.documents")
            doc_count = cur.fetchone()[0]
            click.echo(f"✅ 数据库连接正常 - 文档总数: {doc_count}")
    except Exception as e:
        click.echo(f"❌ 数据库连接失败: {str(e)}")
    
    # 检查Kafka连接
    try:
        from kafka import KafkaAdminClient
        admin_client = KafkaAdminClient(
            bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        )
        topics = admin_client.list_topics()
        click.echo(f"✅ Kafka连接正常 - 主题数量: {len(topics)}")
    except Exception as e:
        click.echo(f"❌ Kafka连接失败: {str(e)}")
    
    # 检查Prometheus服务
    try:
        import requests
        response = requests.get(f"http://localhost:8001/metrics")
        if response.status_code == 200:
            click.echo("✅ Prometheus指标服务运行正常")
        else:
            click.echo(f"❌ Prometheus指标服务异常: HTTP {response.status_code}")
    except Exception as e:
        click.echo(f"❌ Prometheus指标服务未运行: {str(e)}")

# 添加查询CLI作为子命令
main.add_command(query_cli, name='query')

if __name__ == "__main__":
    main() 