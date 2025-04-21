package com.worldlora.flink;

import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.configuration.Configuration;
import java.util.HashMap;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MetadataExtractor extends RichMapFunction<Document, Document> {
    private Pattern authorPattern;
    private Pattern datePattern;

    @Override
    public void open(Configuration parameters) throws Exception {
        // 初始化正则表达式模式
        authorPattern = Pattern.compile("作者[:：]\\s*(\\w+)");
        datePattern = Pattern.compile("日期[:：]\\s*(\\d{4}-\\d{2}-\\d{2})");
    }

    @Override
    public Document map(Document doc) throws Exception {
        String content = doc.getContent();
        Map<String, Object> metadata = new HashMap<>();

        // 提取作者
        Matcher authorMatcher = authorPattern.matcher(content);
        if (authorMatcher.find()) {
            metadata.put("author", authorMatcher.group(1));
        }

        // 提取日期
        Matcher dateMatcher = datePattern.matcher(content);
        if (dateMatcher.find()) {
            metadata.put("date", dateMatcher.group(1));
        }

        // 添加其他元数据
        metadata.put("length", content.length());
        metadata.put("timestamp", System.currentTimeMillis());

        doc.setMetadata(metadata);
        return doc;
    }

    @Override
    public void close() throws Exception {
        // 清理资源
    }
} 