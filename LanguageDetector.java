package com.worldlora.flink;

import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.configuration.Configuration;
import com.optimaize.languagedetector.LanguageDetector;
import com.optimaize.languagedetector.LanguageDetectorBuilder;
import com.optimaize.languagedetector.ngram.NgramExtractors;
import com.optimaize.languagedetector.profiles.LanguageProfileReader;

import java.io.IOException;
import java.util.List;

public class LanguageDetector extends RichMapFunction<Document, Document> {
    private com.optimaize.languagedetector.LanguageDetector detector;

    @Override
    public void open(Configuration parameters) throws Exception {
        // 初始化语言检测器
        detector = LanguageDetectorBuilder.create(NgramExtractors.standard())
            .withProfiles(new LanguageProfileReader().readAllBuiltIn())
            .build();
    }

    @Override
    public Document map(Document doc) throws Exception {
        String content = doc.getCleanedContent();
        
        // 检测语言
        List<com.optimaize.languagedetector.LanguageDetectorResult> results = detector.getProbabilities(content);
        
        if (!results.isEmpty()) {
            // 获取最可能的语言
            String language = results.get(0).getLanguage().getLanguage();
            doc.setLanguage(language);
        } else {
            doc.setLanguage("unknown");
        }
        
        return doc;
    }

    @Override
    public void close() throws Exception {
        // 清理资源
    }
} 