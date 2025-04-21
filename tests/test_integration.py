import pytest
import json
import requests
import sys
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from flink.document_cleaner import DocumentCleaningFunction
    from elasticsearch import Elasticsearch
except ImportError as e:
    logger.error(f"导入模块失败: {e}")
    logger.error("请确保已安装所有必要的依赖: pip install -r requirements.txt")
    raise

import time

# 测试配置
ES_HOST = "http://localhost:9200"
INDEX_NAME = "worldlora_docs"
TEST_DOC = {
    "content": """
    <html>
        <head><title>测试文档</title></head>
        <body>
            <h1>作者：张三</h1>
            <p>这是一段测试内容。包含一些实体，如北京、阿里巴巴等。</p>
            <p>这是第二段内容。主要讲述了一些技术细节。</p>
            <p>最后一段是总结。</p>
        </body>
    </html>
    """,
    "source": "test",
    "url": "http://example.com",
    "timestamp": "2023-01-01T00:00:00Z"
}

def create_elasticsearch_index(es_client):
    """创建Elasticsearch索引并应用映射"""
    try:
        # 检查索引是否存在
        if es_client.indices.exists(index=INDEX_NAME):
            logger.info(f"索引 {INDEX_NAME} 已存在，正在删除...")
            es_client.indices.delete(index=INDEX_NAME)
        
        # 定义索引映射
        mapping = {
            "mappings": {
                "properties": {
                    "content_hash": { "type": "keyword" },
                    "source_id": { "type": "keyword" },
                    "url": { "type": "keyword" },
                    "title": { 
                        "type": "text",
                        "analyzer": "smartcn_analyzer",
                        "fields": {
                            "keyword": { "type": "keyword" }
                        }
                    },
                    "clean_content": { 
                        "type": "text",
                        "analyzer": "smartcn_analyzer"
                    },
                    "entities": {
                        "type": "nested", # 明确定义为嵌套类型
                        "properties": {
                            "text": { "type": "keyword" },
                            "label": { "type": "keyword" }
                        }
                    },
                    "summaries": {
                        "properties": {
                            "title": { "type": "text" },
                            "short_summary": { "type": "text" },
                            "structured_summary": { "type": "object" }
                        }
                    },
                    "capture_timestamp": { "type": "date" },
                    "embedding_vector": {
                        "type": "dense_vector",
                        "dims": 768
                    }
                }
            }
        }
        
        # 创建索引并应用映射
        logger.info(f"正在创建索引 {INDEX_NAME}...")
        es_client.indices.create(index=INDEX_NAME, body=mapping)
        # 等待并刷新索引确保映射生效
        time.sleep(1)
        es_client.indices.refresh(index=INDEX_NAME)
        logger.info(f"成功创建并刷新索引 {INDEX_NAME}")
        
    except Exception as e:
        logger.error(f"创建或刷新索引失败: {e}")
        raise

@pytest.fixture(scope="module") # 使用module范围确保索引只创建一次
def es_client():
    """提供Elasticsearch客户端并确保索引存在"""
    try:
        client = Elasticsearch([ES_HOST])
        # 测试连接
        if not client.ping():
            raise ConnectionError("无法连接到Elasticsearch服务")
        # 创建或重置索引
        create_elasticsearch_index(client)
        return client
    except Exception as e:
        logger.error(f"Elasticsearch设置失败: {e}")
        pytest.skip(f"无法连接或设置Elasticsearch: {e}") # 跳过测试如果ES设置失败

@pytest.fixture(scope="module")
def cleaner():
    """提供文档清洗器实例"""
    try:
        return DocumentCleaningFunction()
    except Exception as e:
        logger.error(f"创建DocumentCleaningFunction失败: {e}")
        raise

def test_flink_cleaning_pipeline(cleaner):
    """测试Flink清洗模块的扩展性"""
    try:
        result = cleaner.clean(json.dumps(TEST_DOC))
        cleaned_doc = json.loads(result)
        assert 'clean_content' in cleaned_doc, "缺少clean_content字段"
        assert 'metadata' in cleaned_doc, "缺少metadata字段"
        assert 'entities' in cleaned_doc, "缺少entities字段"
        assert 'summaries' in cleaned_doc, "缺少summaries字段"
        assert 'content_hash' in cleaned_doc, "缺少content_hash字段"
        assert len(cleaned_doc['entities']) > 0, "未识别到实体"
        assert any(ent['label'] == 'LOC' for ent in cleaned_doc['entities']), "未识别到地点实体"
        assert 'short_summary' in cleaned_doc['summaries'], "缺少short_summary"
        assert 'structured_summary' in cleaned_doc['summaries'], "缺少structured_summary"
        logger.info("Flink清洗模块测试通过")
    except Exception as e:
        logger.error(f"Flink清洗模块测试失败: {e}")
        raise

def test_elasticsearch_mapping(es_client):
    """测试Elasticsearch映射的扩展性"""
    try:
        mapping = es_client.indices.get_mapping(index=INDEX_NAME)
        properties = mapping[INDEX_NAME]['mappings']['properties']
        logger.info(f"获取到的映射属性: {properties}")
        
        # 验证实体字段
        assert 'entities' in properties, "缺少entities字段映射"
        # 确认 'entities' 键下有 'type' 键
        assert 'type' in properties['entities'], "entities映射缺少'type'键"
        assert properties['entities']['type'] == 'nested', "entities字段类型不正确，应为 'nested'"
        assert 'properties' in properties['entities'], "entities映射缺少'properties'键"
        assert 'text' in properties['entities']['properties'], "缺少entities.text字段"
        assert 'label' in properties['entities']['properties'], "缺少entities.label字段"
        
        # 验证向量字段
        assert 'embedding_vector' in properties, "缺少embedding_vector字段映射"
        assert properties['embedding_vector']['type'] == 'dense_vector', "embedding_vector字段类型不正确"
        assert properties['embedding_vector']['dims'] == 768, "embedding_vector维度不正确"
        
        logger.info("Elasticsearch映射测试通过")
    except Exception as e:
        logger.error(f"Elasticsearch映射测试失败: {e}")
        raise

def test_search_ui_functionality(es_client, cleaner):
    """测试搜索UI的模块化设计（通过ES查询验证）"""
    try:
        cleaned_doc = json.loads(cleaner.clean(json.dumps(TEST_DOC)))
        content_hash = cleaned_doc.get('content_hash')
        assert content_hash is not None, "清洗后的文档缺少content_hash"
        
        # 索引测试文档
        logger.info(f"正在索引文档 ID: {content_hash}")
        es_client.index(
            index=INDEX_NAME,
            id=content_hash,
            document=cleaned_doc, # 使用 'document' 参数
            refresh=True # 确保文档立即可搜索
        )
        logger.info("文档索引完成")
        
        # --- 测试基本搜索 ---
        logger.info("测试基本搜索...")
        response_basic = es_client.search(
            index=INDEX_NAME,
            body={
                "query": {
                    "multi_match": {
                        "query": "北京",
                        "fields": ["title^3", "clean_content"]
                    }
                }
            }
        )
        logger.info(f"基本搜索响应: {response_basic['hits']}")
        assert response_basic['hits']['total']['value'] > 0, "基本搜索未返回结果"
        
        # --- 测试实体搜索 (Nested Query) ---
        logger.info("测试实体搜索 (Nested Query)...")
        nested_query_body = {
            "query": {
                "nested": {
                    "path": "entities",
                    "query": {
                        "bool": {
                            "must": [
                                {"match": {"entities.text": "北京"}},
                                {"match": {"entities.label": "LOC"}}
                            ]
                        }
                    }
                }
            }
        }
        logger.info(f"Nested Query Body: {json.dumps(nested_query_body)}")
        response_nested = es_client.search(
            index=INDEX_NAME,
            body=nested_query_body
        )
        logger.info(f"实体搜索响应: {response_nested['hits']}")
        assert response_nested['hits']['total']['value'] > 0, "实体搜索 (Nested Query) 未返回结果"
        
        # --- 测试高亮功能 ---
        logger.info("测试高亮功能...")
        response_highlight = es_client.search(
            index=INDEX_NAME,
            body={
                "query": {
                    "multi_match": {
                        "query": "北京",
                        "fields": ["clean_content"]
                    }
                },
                "highlight": {
                    "fields": {
                        "clean_content": {}
                    }
                }
            }
        )
        logger.info(f"高亮搜索响应: {response_highlight['hits']['hits']}")
        assert len(response_highlight['hits']['hits']) > 0, "高亮搜索未返回任何命中"
        assert 'highlight' in response_highlight['hits']['hits'][0], "搜索结果未包含高亮信息"
        
        logger.info("搜索UI功能测试通过")
    except Exception as e:
        logger.error(f"搜索UI功能测试失败: {e}")
        raise

if __name__ == "__main__":
    pytest.main([__file__]) 