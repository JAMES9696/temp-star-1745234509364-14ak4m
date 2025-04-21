package com.worldlora.flink;

import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.configuration.Configuration;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class HtmlCleaner extends RichMapFunction<Document, Document> {
    @Override
    public void open(Configuration parameters) throws Exception {
        // 初始化资源
    }

    @Override
    public Document map(Document doc) throws Exception {
        String content = doc.getContent();
        
        // 使用 Jsoup 解析 HTML
        org.jsoup.nodes.Document htmlDoc = Jsoup.parse(content);
        
        // 移除脚本和样式标签
        htmlDoc.select("script, style").remove();
        
        // 保留链接
        Elements links = htmlDoc.select("a[href]");
        for (Element link : links) {
            String href = link.attr("href");
            link.after(" [" + href + "] ");
        }
        
        // 获取清理后的文本
        String cleanedText = htmlDoc.text()
            .replaceAll("\\s+", " ")
            .trim();
        
        doc.setCleanedContent(cleanedText);
        return doc;
    }

    @Override
    public void close() throws Exception {
        // 清理资源
    }
} 