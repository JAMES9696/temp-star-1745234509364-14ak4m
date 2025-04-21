package com.worldlora.flink;

import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.configuration.Configuration;
import org.deeplearning4j.models.embeddings.loader.WordVectorSerializer;
import org.deeplearning4j.models.word2vec.Word2Vec;
import org.deeplearning4j.text.tokenization.tokenizerfactory.DefaultTokenizerFactory;
import org.deeplearning4j.text.tokenization.tokenizerfactory.TokenizerFactory;

import java.io.File;
import java.util.List;

public class EmbeddingGenerator extends RichMapFunction<Document, Document> {
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
        
        // 计算文档向量
        float[] documentVector = new float[word2Vec.getLayerSize()];
        int validTokens = 0;
        
        for (String token : tokens) {
            if (word2Vec.hasWord(token)) {
                float[] wordVector = word2Vec.getWordVectorMatrix(token).toFloatVector();
                for (int i = 0; i < wordVector.length; i++) {
                    documentVector[i] += wordVector[i];
                }
                validTokens++;
            }
        }
        
        // 平均向量
        if (validTokens > 0) {
            for (int i = 0; i < documentVector.length; i++) {
                documentVector[i] /= validTokens;
            }
        }
        
        doc.setEmbeddings(documentVector);
        return doc;
    }

    @Override
    public void close() throws Exception {
        // 清理资源
    }
} 