#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import time
import logging
import sys
import os  # 添加os模块导入

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ES_Connection_Test")

def test_es_connection(es_host="es-worldlora", es_port=9200):
    """测试Elasticsearch连接"""
    url = f"http://{es_host}:{es_port}"
    
    logger.info(f"测试连接到 Elasticsearch: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            logger.info(f"连接成功! Elasticsearch 返回: {response.json()}")
            return True
        else:
            logger.error(f"连接失败! 状态码: {response.status_code}, 响应: {response.text}")
            return False
    except requests.exceptions.ConnectionError as e:
        logger.error(f"连接错误: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"发生错误: {str(e)}")
        return False

def send_test_document(es_host="es-worldlora", es_port=9200):
    """发送测试文档到 Elasticsearch"""
    url = f"http://{es_host}:{es_port}/worldlora_test/_doc/1"
    
    logger.info(f"向 Elasticsearch 发送测试文档到: {url}")
    
    test_doc = {
        "title": "测试文档",
        "content": "这是一个测试文档，用于验证 Flink 到 Elasticsearch 的连接。",
        "timestamp": int(time.time() * 1000),
        "source": "flink_test",
        "test_id": "test-001"
    }
    
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, data=json.dumps(test_doc), headers=headers, timeout=10)
        
        if response.status_code in [200, 201]:
            logger.info(f"文档发送成功! 响应: {response.json()}")
            return True
        else:
            logger.error(f"文档发送失败! 状态码: {response.status_code}, 响应: {response.text}")
            return False
    except Exception as e:
        logger.error(f"发送文档时发生错误: {str(e)}")
        return False

def create_test_index(es_host="es-worldlora", es_port=9200):
    """创建测试索引"""
    url = f"http://{es_host}:{es_port}/worldlora_test"
    
    logger.info(f"创建测试索引: {url}")
    
    mapping = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "title": {"type": "text"},
                "content": {"type": "text"},
                "timestamp": {"type": "date"},
                "source": {"type": "keyword"},
                "test_id": {"type": "keyword"}
            }
        }
    }
    
    try:
        headers = {"Content-Type": "application/json"}
        response = requests.put(url, data=json.dumps(mapping), headers=headers, timeout=10)
        
        if response.status_code in [200, 201]:
            logger.info(f"索引创建成功! 响应: {response.json()}")
            return True
        else:
            logger.error(f"索引创建失败! 状态码: {response.status_code}, 响应: {response.text}")
            return False
    except Exception as e:
        logger.error(f"创建索引时发生错误: {str(e)}")
        return False

def test_ping_host(host="es-worldlora"):
    """测试能否 ping 通主机"""
    logger.info(f"尝试 ping {host}...")
    exit_code = os.system(f"ping -c 3 {host}")
    if exit_code == 0:
        logger.info(f"Ping {host} 成功!")
        return True
    else:
        logger.error(f"Ping {host} 失败!")
        return False

def main():
    """主函数"""
    logger.info("开始测试 Elasticsearch 连接...")
    
    # 获取命令行参数
    if len(sys.argv) > 1:
        es_host = sys.argv[1]
    else:
        es_host = "es-worldlora"
    
    if len(sys.argv) > 2:
        es_port = int(sys.argv[2])
    else:
        es_port = 9200
    
    logger.info(f"使用 Elasticsearch 主机: {es_host}:{es_port}")
    
    # 检查Docker网络信息
    logger.info("检查容器网络配置:")
    os.system("cat /etc/hosts")
    os.system("ip route")
    
    # 测试网络连通性
    try:
        test_ping_host(es_host)
    except:
        logger.error("ping命令不可用")
    
    # 测试ES连接
    if test_es_connection(es_host, es_port):
        # 如果连接成功，创建测试索引
        if create_test_index(es_host, es_port):
            # 发送测试文档
            send_test_document(es_host, es_port)
    else:
        logger.error("无法连接到 Elasticsearch。请检查网络配置和服务状态。")
        logger.info("检查是否可以连接到其他服务:")
        try:
            test_es_connection("kafka", 29092)
        except:
            logger.error("无法连接到kafka")

if __name__ == "__main__":
    main() 