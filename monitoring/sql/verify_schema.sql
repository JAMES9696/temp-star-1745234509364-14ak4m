-- 验证数据源表结构
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_schema = 'metadata' 
    AND table_name = 'sources';

-- 验证文档表结构
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM 
    information_schema.columns
WHERE 
    table_schema = 'storage' 
    AND table_name = 'documents';

-- 检查表是否存在
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_schema = 'metadata' 
    AND table_name = 'sources'
) AS sources_table_exists;

SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE table_schema = 'storage' 
    AND table_name = 'documents'
) AS documents_table_exists; 