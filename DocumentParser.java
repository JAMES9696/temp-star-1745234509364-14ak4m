package com.worldlora.flink;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.flink.api.common.functions.MapFunction;

public class DocumentParser implements MapFunction<String, Document> {
    private static final ObjectMapper mapper = new ObjectMapper();

    @Override
    public Document map(String value) throws Exception {
        Document doc = new Document();
        // 解析 JSON 字符串
        Map<String, Object> json = mapper.readValue(value, Map.class);
        
        // 设置基本字段
        doc.setId((String) json.get("id"));
        doc.setContent((String) json.get("content"));
        doc.setTimestamp(System.currentTimeMillis());
        
        return doc;
    }
} 