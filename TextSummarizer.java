package com.worldlora.flink;

import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.configuration.Configuration;
import org.deeplearning4j.models.embeddings.loader.WordVectorSerializer;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.deeplearning4j.text.tokenization.tokenizerfactory.DefaultTokenizerFactory;
import org.deeplearning4j.text.tokenization.tokenizerfactory.TokenizerFactory;

import java.io.File;
import java.util.ArrayList;
import java.util.List;

public class TextSummarizer extends RichMapFunction<Document, Document> {
    private Word2Vec word2Vec;
    private TokenizerFactory tokenizerFactory;

    @Override
    public void open(Configuration parameters) throws Exception {
        // 初始化 Word2Vec 模型
        word2Vec = WordVectorSerializer.readWord2VecModel(new File("path/to/word2vec/model"));
        tokenizerFactory = new DefaultTokenizerFactory();
    }

    @Override
    public Document map(Document doc) throws Exception {
        String content = doc.getCleanedContent();
        
        // 分词
        List<String> tokens = tokenizerFactory.create(content).getTokens();
        
        // 计算句子重要性
        List<String> sentences = splitIntoSentences(content);
        List<Double> sentenceScores = new ArrayList<>();
        
        for (String sentence : sentences) {
            double score = calculateSentenceScore(sentence, tokens);
            sentenceScores.add(score);
        }
        
        // 选择最重要的句子
        String summary = generateSummary(sentences, sentenceScores, 3);
        doc.setSummary(summary);
        
        return doc;
    }

    private List<String> splitIntoSentences(String text) {
        // 简单的句子分割
        String[] sentences = text.split("[.!?]+\\s+");
        return List.of(sentences);
    }

    private double calculateSentenceScore(String sentence, List<String> documentTokens) {
        // 计算句子与文档的相关性得分
        List<String> sentenceTokens = tokenizerFactory.create(sentence).getTokens();
        double score = 0.0;
        
        for (String token : sentenceTokens) {
            if (word2Vec.hasWord(token)) {
                for (String docToken : documentTokens) {
                    if (word2Vec.hasWord(docToken)) {
                        score += word2Vec.similarity(token, docToken);
                    }
                }
            }
        }
        
        return score / (sentenceTokens.size() * documentTokens.size());
    }

    private String generateSummary(List<String> sentences, List<Double> scores, int numSentences) {
        // 选择得分最高的句子
        List<Integer> topIndices = new ArrayList<>();
        for (int i = 0; i < Math.min(numSentences, sentences.size()); i++) {
            int maxIndex = 0;
            double maxScore = Double.MIN_VALUE;
            
            for (int j = 0; j < scores.size(); j++) {
                if (!topIndices.contains(j) && scores.get(j) > maxScore) {
                    maxScore = scores.get(j);
                    maxIndex = j;
                }
            }
            
            topIndices.add(maxIndex);
        }
        
        // 按原始顺序排序
        topIndices.sort(Integer::compareTo);
        
        // 构建摘要
        StringBuilder summary = new StringBuilder();
        for (int index : topIndices) {
            summary.append(sentences.get(index)).append(". ");
        }
        
        return summary.toString().trim();
    }

    @Override
    public void close() throws Exception {
        // 清理资源
    }
} 