-- WorldLoRa Nebula 基础架构

-- 创建扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
CREATE EXTENSION IF NOT EXISTS "pg_trgm"; -- 用于模糊搜索

-- 创建架构
CREATE SCHEMA IF NOT EXISTS capture;
CREATE SCHEMA IF NOT EXISTS processing;
CREATE SCHEMA IF NOT EXISTS storage;
CREATE SCHEMA IF NOT EXISTS metadata;

-- 来源注册表
CREATE TABLE metadata.sources (
    source_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    url_pattern TEXT,
    capture_frequency INTERVAL,
    credentials JSONB,
    headers JSONB,
    active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 文档主表
CREATE TABLE storage.documents (
    doc_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES metadata.sources(source_id),
    title TEXT,
    url TEXT,
    content_hash TEXT NOT NULL,
    original_content TEXT,
    processed_content TEXT,
    summary TEXT,
    processed_at TIMESTAMP WITH TIME ZONE,
    visibility VARCHAR(20) DEFAULT 'private', -- private, friends, public
    doc_type VARCHAR(50) DEFAULT 'article',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

-- 创建实体表
CREATE TABLE metadata.entities (
    entity_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    entity_type VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    metadata JSONB
);

-- 文档-实体关联表
CREATE TABLE metadata.document_entities (
    doc_id UUID REFERENCES storage.documents(doc_id),
    entity_id UUID REFERENCES metadata.entities(entity_id),
    confidence FLOAT,
    relation_type VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (doc_id, entity_id)
);

-- 标签表
CREATE TABLE metadata.tags (
    tag_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    parent_tag_id UUID REFERENCES metadata.tags(tag_id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 文档标签关联表
CREATE TABLE metadata.document_tags (
    doc_id UUID REFERENCES storage.documents(doc_id),
    tag_id UUID REFERENCES metadata.tags(tag_id),
    confidence FLOAT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(255),
    PRIMARY KEY (doc_id, tag_id)
);

-- 向量索引表 (用于语义搜索)
CREATE TABLE storage.document_vectors (
    doc_id UUID REFERENCES storage.documents(doc_id),
    model_id VARCHAR(100) NOT NULL,
    vector_data BYTEA NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    PRIMARY KEY (doc_id, model_id)
);

-- 捕获日志表
CREATE TABLE capture.capture_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES metadata.sources(source_id),
    status VARCHAR(50),
    started_at TIMESTAMP WITH TIME ZONE,
    finished_at TIMESTAMP WITH TIME ZONE,
    items_captured INTEGER,
    items_rejected INTEGER,
    error_message TEXT,
    details JSONB
);

-- 版本历史表
CREATE TABLE storage.document_versions (
    version_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doc_id UUID REFERENCES storage.documents(doc_id),
    content_hash TEXT NOT NULL,
    content TEXT,
    diff TEXT,
    version_number INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 用户活动日志表
CREATE TABLE metadata.user_activities (
    activity_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    doc_id UUID REFERENCES storage.documents(doc_id),
    activity_type VARCHAR(50) NOT NULL,
    activity_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 索引
CREATE INDEX idx_documents_content_hash ON storage.documents(content_hash);
CREATE INDEX idx_documents_source_id ON storage.documents(source_id);
CREATE INDEX idx_documents_created_at ON storage.documents(created_at);
CREATE INDEX idx_documents_visibility ON storage.documents(visibility);
CREATE INDEX idx_document_entities_entity_id ON metadata.document_entities(entity_id);
CREATE INDEX idx_document_tags_tag_id ON metadata.document_tags(tag_id);
CREATE INDEX idx_tags_name ON metadata.tags(name);
CREATE INDEX idx_entities_name ON metadata.entities(name);
CREATE INDEX idx_entities_type ON metadata.entities(entity_type);

-- 触发器函数：更新时间戳
CREATE OR REPLACE FUNCTION update_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- 添加更新时间戳触发器
CREATE TRIGGER update_sources_timestamp BEFORE UPDATE ON metadata.sources
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER update_documents_timestamp BEFORE UPDATE ON storage.documents
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER update_entities_timestamp BEFORE UPDATE ON metadata.entities
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

CREATE TRIGGER update_tags_timestamp BEFORE UPDATE ON metadata.tags
FOR EACH ROW EXECUTE FUNCTION update_timestamp();

-- 添加全文搜索功能
ALTER TABLE storage.documents ADD COLUMN ts_vector TSVECTOR 
GENERATED ALWAYS AS (
    setweight(to_tsvector('english', coalesce(title, '')), 'A') || 
    setweight(to_tsvector('english', coalesce(processed_content, '')), 'B')
) STORED;

CREATE INDEX idx_documents_ts_vector ON storage.documents USING GIN(ts_vector); 