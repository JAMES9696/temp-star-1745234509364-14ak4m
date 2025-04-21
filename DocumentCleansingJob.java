package com.worldlora.flink;

import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.base.DeliveryGuarantee;
import org.apache.flink.connector.elasticsearch.sink.ElasticsearchSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.http.HttpHost;
import org.elasticsearch.client.RestClient;
import org.elasticsearch.client.RestHighLevelClient;

import java.util.ArrayList;
import java.util.List;

public class DocumentCleansingJob {
    public static void main(String[] args) throws Exception {
        // 创建执行环境
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();

        // 配置 Kafka 源
        KafkaSource<String> source = KafkaSource.<String>builder()
            .setBootstrapServers("localhost:9092")
            .setTopics("worldlora.capture.raw")
            .setGroupId("worldlora-cleansing")
            .setStartingOffsets(OffsetsInitializer.earliest())
            .setValueOnlyDeserializer(new SimpleStringSchema())
            .build();

        // 创建数据流
        DataStream<String> stream = env.fromSource(
            source,
            WatermarkStrategy.noWatermarks(),
            "Kafka Source"
        );

        // 应用清洗函数
        DataStream<Document> cleanedStream = stream
            .map(new DocumentParser())
            .process(new DocumentCleaner())
            .process(new MetadataExtractor())
            .process(new HtmlCleaner())
            .process(new TextNormalizer())
            .process(new LanguageDetector())
            .process(new NERProcessor())
            .process(new TextSummarizer())
            .process(new EmbeddingGenerator());

        // 配置 Elasticsearch 接收器
        List<HttpHost> httpHosts = new ArrayList<>();
        httpHosts.add(new HttpHost("localhost", 9200, "http"));

        ElasticsearchSink<Document> sink = ElasticsearchSink.<Document>builder()
            .setHosts(httpHosts)
            .setBulkFlushMaxActions(1000)
            .setBulkFlushInterval(10000)
            .setDeliveryGuarantee(DeliveryGuarantee.AT_LEAST_ONCE)
            .setSerializer(new DocumentSerializer())
            .build();

        // 添加接收器
        cleanedStream.sinkTo(sink);

        // 执行作业
        env.execute("Document Cleansing Job");
    }
} 