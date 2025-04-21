#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Elasticsearch 连接测试脚本
用于验证与Elasticsearch的连接和索引配置
"""

from elasticsearch import Elasticsearch
import logging
import json
import sys
import time

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("ESConnectionTest")

def test_es_connection(hosts=None, retry_count=3, retry_delay=5):
    """测试ES连接并检查集群状态"""
    if not hosts:
        hosts = ['http://localhost:9200']
    
    logger.info(f"尝试连接到 Elasticsearch: {hosts}")
    
    for attempt in range(retry_count):
        try:
            es = Elasticsearch(hosts=hosts, timeout=30)
            
            # 检查连接是否成功
            if not es.ping():
                raise ConnectionError("ping 失败，无法连接到 Elasticsearch")
            
            # 获取集群健康状态
            health = es.cluster.health()
            logger.info(f"ES集群状态: {health['status']}")
            
            # 获取节点信息
            nodes_info = es.nodes.info()
            node_count = len(nodes_info['nodes'])
            logger.info(f"ES集群节点数: {node_count}")
            
            # 获取索引信息
            indices = es.indices.get_alias("*")
            logger.info(f"ES索引列表: {', '.join(indices.keys())}")
            
            logger.info("ES连接测试成功!")
            return es
            
        except Exception as e:
            logger.error(f"连接失败 (尝试 {attempt+1}/{retry_count}): {str(e)}")
            if attempt < retry_count - 1:
                logger.info(f"等待 {retry_delay} 秒后重试...")
                time.sleep(retry_delay)
    
    logger.error(f"在 {retry_count} 次尝试后仍无法连接到 Elasticsearch")
    return None

def test_index_creation(es, index_name="test_index"):
    """测试索引创建功能"""
    try:
        # 如果索引已存在，先删除
        if es.indices.exists(index=index_name):
            logger.info(f"删除已存在的索引: {index_name}")
            es.indices.delete(index=index_name)
        
        # 创建测试索引
        mapping = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0
            },
            "mappings": {
                "properties": {
                    "title": {"type": "text"},
                    "content": {"type": "text"},
                    "timestamp": {"type": "date"}
                }
            }
        }
        
        es.indices.create(index=index_name, body=mapping)
        logger.info(f"成功创建测试索引: {index_name}")
        
        # 插入测试文档
        doc = {
            "title": "测试文档",
            "content": "这是一个用于测试ES连接的文档",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
        }
        
        es.index(index=index_name, body=doc, id=1)
        logger.info("成功插入测试文档")
        
        # 刷新索引确保可查询
        es.indices.refresh(index=index_name)
        
        # 查询测试文档
        result = es.get(index=index_name, id=1)
        logger.info(f"查询结果: {result['_source']}")
        
        # 删除测试索引
        es.indices.delete(index=index_name)
        logger.info(f"测试完成，已删除索引: {index_name}")
        
        return True
    except Exception as e:
        logger.error(f"索引测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    # 解析命令行参数
    hosts = ['http://localhost:9200']
    if len(sys.argv) > 1:
        hosts = [sys.argv[1]]
    
    # 测试连接
    es = test_es_connection(hosts)
    if es:
        # 测试索引
        test_index_creation(es)
    else:
        sys.exit(1) 