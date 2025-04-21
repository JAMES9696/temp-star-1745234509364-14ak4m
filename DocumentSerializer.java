package com.worldlora.flink;

import org.apache.flink.connector.elasticsearch.sink.ElasticsearchSinkFunction;
import org.apache.flink.connector.elasticsearch.sink.RequestIndexer;
import org.elasticsearch.action.index.IndexRequest;
import org.elasticsearch.client.Requests;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.util.HashMap;
import java.util.Map;

public class DocumentSerializer implements ElasticsearchSinkFunction<Document> {
    private static final ObjectMapper mapper = new ObjectMapper();

    @Override
    public void process(Document document, RuntimeContext ctx, RequestIndexer indexer) {
        Map<String, Object> json = new HashMap<>();
        
        // 添加基本字段
        json.put("id", document.getId());
        json.put("content", document.getContent());
        json.put("cleaned_content", document.getCleanedContent());
        json.put("metadata", document.getMetadata());
        json.put("language", document.getLanguage());
        json.put("summary", document.getSummary());
        json.put("timestamp", document.getTimestamp());
        
        // 添加实体
        if (document.getEntities() != null) {
            json.put("entities", document.getEntities());
        }
        
        // 添加向量嵌入
        if (document.getEmbeddings() != null) {
            json.put("embeddings", document.getEmbeddings());
        }
        
        // 创建索引请求
        IndexRequest request = Requests.indexRequest()
            .index("worldlora_docs")
            .id(document.getId())
            .source(json);
        
        // 添加到索引器
        indexer.add(request);
    }
} 