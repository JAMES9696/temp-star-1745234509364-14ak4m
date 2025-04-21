-- 获取数据源统计信息
SELECT 
    COUNT(*) as total_sources,
    COUNT(DISTINCT source_type) as unique_source_types,
    MIN(created_at) as oldest_source,
    MAX(created_at) as newest_source
FROM 
    metadata.sources;

-- 获取文档统计信息
SELECT 
    COUNT(*) as total_documents,
    COUNT(DISTINCT source_id) as sources_with_documents,
    MIN(created_at) as oldest_document,
    MAX(created_at) as newest_document
FROM 
    storage.documents;

-- 获取最近24小时的文档创建趋势
SELECT 
    DATE_TRUNC('hour', created_at) as hour,
    COUNT(*) as documents_created
FROM 
    storage.documents
WHERE 
    created_at >= NOW() - INTERVAL '24 hours'
GROUP BY 
    hour
ORDER BY 
    hour DESC;

-- === 基础数据统计 ===
-- 文档总数
SELECT COUNT(*) as total_documents FROM storage.documents;

-- 按数据源统计
SELECT 
    s.name as source_name,
    s.source_type,
    COUNT(d.doc_id) as document_count,
    MAX(d.created_at) as latest_document
FROM metadata.sources s
LEFT JOIN storage.documents d ON s.source_id = d.source_id
GROUP BY s.name, s.source_type
ORDER BY document_count DESC;

-- 最近的文档捕获
SELECT 
    title,
    url,
    created_at,
    jsonb_pretty(metadata) as metadata
FROM storage.documents
ORDER BY created_at DESC
LIMIT 10;

-- === 数据质量检查 ===
-- 空内容文档
SELECT COUNT(*) as empty_content_count
FROM storage.documents
WHERE original_content IS NULL OR original_content = '';

-- 重复文档检测
SELECT 
    content_hash,
    COUNT(*) as duplicate_count,
    array_agg(title) as titles
FROM storage.documents
GROUP BY content_hash
HAVING COUNT(*) > 1;

-- 错误消息统计
SELECT COUNT(*) as error_documents
FROM storage.documents
WHERE metadata->>'type' = 'error';

-- === 性能指标 ===
-- 每日文档捕获量
SELECT 
    DATE(created_at) as capture_date,
    COUNT(*) as documents_captured
FROM storage.documents
GROUP BY DATE(created_at)
ORDER BY capture_date DESC
LIMIT 30;

-- 平均文档大小
SELECT 
    AVG(LENGTH(original_content)) as avg_content_length,
    MAX(LENGTH(original_content)) as max_content_length,
    MIN(LENGTH(original_content)) as min_content_length
FROM storage.documents; 