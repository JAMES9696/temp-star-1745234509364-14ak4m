package com.worldlora.flink;

import org.apache.flink.api.common.functions.RichMapFunction;
import org.apache.flink.configuration.Configuration;
import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.ling.*;
import edu.stanford.nlp.util.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class NERProcessor extends RichMapFunction<Document, Document> {
    private StanfordCoreNLP pipeline;

    @Override
    public void open(Configuration parameters) throws Exception {
        // 初始化 Stanford CoreNLP
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner");
        props.setProperty("ner.applyNumericClassifiers", "false");
        props.setProperty("ner.useSUTime", "false");
        pipeline = new StanfordCoreNLP(props);
    }

    @Override
    public Document map(Document doc) throws Exception {
        String content = doc.getCleanedContent();
        List<Entity> entities = new ArrayList<>();

        // 创建文档
        CoreDocument document = new CoreDocument(content);
        
        // 运行所有注解
        pipeline.annotate(document);

        // 提取命名实体
        for (CoreEntityMention em : document.entityMentions()) {
            String type = em.entityType();
            if (type.equals("PERSON") || type.equals("ORGANIZATION") || type.equals("LOCATION")) {
                entities.add(new Entity(
                    em.text(),
                    type,
                    em.charOffsets().first,
                    em.charOffsets().second
                ));
            }
        }

        doc.setEntities(entities);
        return doc;
    }

    @Override
    public void close() throws Exception {
        // 清理资源
    }
} 