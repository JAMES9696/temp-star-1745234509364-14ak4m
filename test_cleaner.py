from document_cleaner import DocumentCleaningFunction
import json

def test_document_cleaning():
    # 测试数据
    test_doc = {
        "content": """
        <html>
            <head><title>测试文档</title></head>
            <body>
                <h1>作者：张三</h1>
                <p>这是一段测试内容。包含一些实体，如北京、阿里巴巴等。</p>
                <p>这是第二段内容。主要讲述了一些技术细节。</p>
                <p>最后一段是总结。</p>
            </body>
        </html>
        """,
        "source": "test",
        "url": "http://example.com",
        "timestamp": "2023-01-01T00:00:00Z"
    }
    
    # 创建清洗器
    cleaner = DocumentCleaningFunction()
    
    # 执行清洗
    result = cleaner.clean(json.dumps(test_doc))
    cleaned_doc = json.loads(result)
    
    # 打印结果
    print("原始文档:")
    print(json.dumps(test_doc, indent=2, ensure_ascii=False))
    print("\n清洗后的文档:")
    print(json.dumps(cleaned_doc, indent=2, ensure_ascii=False))
    
    # 验证结果
    assert 'clean_content' in cleaned_doc
    assert 'metadata' in cleaned_doc
    assert 'entities' in cleaned_doc
    assert 'summaries' in cleaned_doc
    assert 'content_hash' in cleaned_doc
    
    print("\n测试通过！")

if __name__ == "__main__":
    test_document_cleaning() 