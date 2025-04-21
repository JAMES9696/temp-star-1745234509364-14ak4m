import requests
import json

def setup_elasticsearch_index():
    # Elasticsearch配置
    es_host = "http://localhost:9200"
    index_name = "worldlora_documents"
    
    # 索引映射配置
    index_mapping = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1
        },
        "mappings": {
            "properties": {
                "id":          { "type": "keyword" },
                "source":      { "type": "keyword" },
                "title":       { "type": "text"    },
                "content":     { "type": "text"    },
                "timestamp":   { 
                    "type": "date",
                    "format": "strict_date_optional_time||epoch_millis"
                }
            }
        }
    }
    
    # 检查索引是否存在
    response = requests.head(f"{es_host}/{index_name}")
    if response.status_code == 200:
        print(f"索引 {index_name} 已存在，正在删除...")
        delete_response = requests.delete(f"{es_host}/{index_name}")
        if delete_response.status_code == 200:
            print(f"索引 {index_name} 删除成功。")
        else:
            print(f"警告：删除索引 {index_name} 失败: {delete_response.text}")
    
    # 创建索引
    response = requests.put(
        f"{es_host}/{index_name}",
        headers={"Content-Type": "application/json"},
        data=json.dumps(index_mapping)
    )
    
    if response.status_code == 200:
        print(f"成功创建索引 {index_name}")
        print("索引映射配置:")
        print(json.dumps(index_mapping, indent=2, ensure_ascii=False))
    else:
        print(f"创建索引失败: {response.text}")

if __name__ == "__main__":
    setup_elasticsearch_index() 