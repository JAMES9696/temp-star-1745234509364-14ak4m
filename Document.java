package com.worldlora.flink;

import java.util.List;
import java.util.Map;

public class Document {
    private String id;
    private String content;
    private String cleanedContent;
    private Map<String, Object> metadata;
    private String language;
    private List<Entity> entities;
    private String summary;
    private float[] embeddings;
    private long timestamp;

    // Getters and Setters
    public String getId() { return id; }
    public void setId(String id) { this.id = id; }

    public String getContent() { return content; }
    public void setContent(String content) { this.content = content; }

    public String getCleanedContent() { return cleanedContent; }
    public void setCleanedContent(String cleanedContent) { this.cleanedContent = cleanedContent; }

    public Map<String, Object> getMetadata() { return metadata; }
    public void setMetadata(Map<String, Object> metadata) { this.metadata = metadata; }

    public String getLanguage() { return language; }
    public void setLanguage(String language) { this.language = language; }

    public List<Entity> getEntities() { return entities; }
    public void setEntities(List<Entity> entities) { this.entities = entities; }

    public String getSummary() { return summary; }
    public void setSummary(String summary) { this.summary = summary; }

    public float[] getEmbeddings() { return embeddings; }
    public void setEmbeddings(float[] embeddings) { this.embeddings = embeddings; }

    public long getTimestamp() { return timestamp; }
    public void setTimestamp(long timestamp) { this.timestamp = timestamp; }
}

class Entity {
    private String text;
    private String type;
    private int start;
    private int end;

    public Entity(String text, String type, int start, int end) {
        this.text = text;
        this.type = type;
        this.start = start;
        this.end = end;
    }

    // Getters
    public String getText() { return text; }
    public String getType() { return type; }
    public int getStart() { return start; }
    public int getEnd() { return end; }
} 