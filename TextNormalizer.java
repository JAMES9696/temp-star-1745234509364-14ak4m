package com.worldlora.flink;

import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.configuration.Configuration;

public class TextNormalizer extends RichMapFunction<Document, Document> {
    @Override
    public void open(Configuration parameters) throws Exception {
        // 初始化资源
    }

    @Override
    public Document map(Document doc) throws Exception {
        String content = doc.getCleanedContent();
        
        // 规范化空白字符
        content = content.replaceAll("\\s+", " ")
                        .replaceAll("[\\u00A0\\u1680\\u180E\\u2000-\\u200B\\u202F\\u205F\\u3000\\uFEFF]", " ")
                        .trim();
        
        // 规范化标点符号
        content = content.replaceAll("，", ", ")
                        .replaceAll("。", ". ")
                        .replaceAll("！", "! ")
                        .replaceAll("？", "? ")
                        .replaceAll("：", ": ")
                        .replaceAll("；", "; ");
        
        // 规范化引号
        content = content.replaceAll("[「」『』]", "\"")
                        .replaceAll("[『』]", "'");
        
        doc.setCleanedContent(content);
        return doc;
    }

    @Override
    public void close() throws Exception {
        // 清理资源
    }
} 