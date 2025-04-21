#!/usr/bin/env python3
import sys
import click
from datetime import datetime
from .config.consumer_settings import ConsumerSettings
from .services.kafka_consumer_service import KafkaConsumerService

def print_banner():
    """打印启动横幅"""
    banner = r"""
  _____         _           _                       
 |   __|___ ___|_|___ ___ _| |___ _____ ___ ___ ___ 
 |__   | . |  _| | - |   | . | -_|     | - |   |_ -|
 |_____|___|_| |_|___|_|_|___|___|_|_|_|___|_|_|___|
                                                    
    Kafka Consumer Service for WorldLoRa Nebula v1.1
    ----------------------------------------------- 
    """
    print(f"{banner}")
    print(f"启动时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50 + "\n")

@click.command()
@click.option('--batch-size', default=50, help='批次大小')
@click.option('--commit-interval', default=1000, help='提交间隔（毫秒）')
def main(batch_size, commit_interval):
    """消费者服务主入口"""
    print_banner()
    
    # 创建设置
    settings = ConsumerSettings()
    settings.BATCH_SIZE = batch_size
    settings.COMMIT_INTERVAL = commit_interval
    
    # 创建并运行消费者服务
    consumer_service = KafkaConsumerService(settings)
    consumer_service.run()

if __name__ == "__main__":
    main() 