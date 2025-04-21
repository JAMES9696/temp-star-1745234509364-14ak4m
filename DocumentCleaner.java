package com.worldlora.flink;

import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.configuration.Configuration;

public class DocumentCleaner extends RichMapFunction<Document, Document> {
    @Override
    public void open(Configuration parameters) throws Exception {
        // 初始化资源
    }

    @Override
    public Document map(Document doc) throws Exception {
        String content = doc.getContent();
        
        // 基本文本清洗
        content = content.replaceAll("\\s+", " ")  // 替换多个空格为单个空格
                        .trim()                    // 去除首尾空格
                        .replaceAll("[\\x00-\\x1F\\x7F]", ""); // 去除控制字符
        
        doc.setCleanedContent(content);
        return doc;
    }

    @Override
    public void close() throws Exception {
        // 清理资源
    }
} 