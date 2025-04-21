import uuid
from typing import List, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError, OperationalError
from contextlib import contextmanager
from ..config.consumer_settings import ConsumerSettings
from ..models.document_model import DocumentModel

class PostgresService:
    """PostgreSQL服务 - 数据的最终归宿"""
    
    def __init__(self, settings: ConsumerSettings):
        self.settings = settings
        self.engine = create_engine(
            settings.DB_URL,
            pool_size=10,
            max_overflow=20,
            pool_timeout=30,
            pool_recycle=1800
        )
    
    @contextmanager
    def get_connection(self):
        """获取数据库连接的上下文管理器"""
        conn = self.engine.connect()
        try:
            yield conn
        finally:
            conn.close()
    
    def ensure_source_exists(self, conn, doc: DocumentModel) -> None:
        """确保数据源存在"""
        query = text("""
            INSERT INTO metadata.sources (source_id, name, source_type, active)
            VALUES (:source_id, :name, :source_type, :active)
            ON CONFLICT (source_id) DO NOTHING
        """)
        
        conn.execute(query, {
            'source_id': doc.source_id,
            'name': doc.source_name or doc.source_type or 'Unknown',
            'source_type': doc.source_type or 'unknown',
            'active': True
        })
    
    def save_document(self, doc: DocumentModel) -> bool:
        """保存文档到数据库"""
        try:
            with self.get_connection() as conn:
                with conn.begin():
                    # 确保源存在
                    self.ensure_source_exists(conn, doc)
                    
                    # 检查文档是否已存在
                    check_query = text("""
                        SELECT doc_id FROM storage.documents 
                        WHERE content_hash = :content_hash
                    """)
                    result = conn.execute(check_query, {'content_hash': doc.content_hash}).fetchone()
                    
                    if result:
                        print(f"[Info] 文档已存在，跳过: {doc.url}")
                        return True
                    
                    # 插入新文档
                    doc.doc_id = str(uuid.uuid4())
                    insert_query = text("""
                        INSERT INTO storage.documents (
                            doc_id, source_id, title, url, content_hash, 
                            original_content, processed_content, summary,
                            visibility, doc_type, metadata, created_at
                        ) VALUES (
                            :doc_id, :source_id, :title, :url, :content_hash,
                            :original_content, :processed_content, :summary,
                            :visibility, :doc_type, :metadata::jsonb, CURRENT_TIMESTAMP
                        )
                    """)
                    
                    conn.execute(insert_query, {
                        'doc_id': doc.doc_id,
                        'source_id': doc.source_id,
                        'title': doc.title,
                        'url': doc.url,
                        'content_hash': doc.content_hash,
                        'original_content': doc.original_content,
                        'processed_content': doc.processed_content,
                        'summary': doc.summary,
                        'visibility': doc.visibility,
                        'doc_type': doc.doc_type,
                        'metadata': doc.model_dump_json(include={'metadata'}, exclude_none=True)
                    })
                    
                    print(f"[Success] 文档保存成功: {doc.url}")
                    return True
                    
        except IntegrityError as e:
            print(f"[Error] 数据完整性错误: {str(e)}")
            return False
        except OperationalError as e:
            print(f"[Error] 数据库操作错误: {str(e)}")
            return False
        except Exception as e:
            print(f"[Error] 未知错误: {str(e)}")
            return False
    
    def batch_save_documents(self, documents: List[DocumentModel]) -> tuple[int, int]:
        """批量保存文档"""
        success_count = 0
        error_count = 0
        
        for doc in documents:
            if self.save_document(doc):
                success_count += 1
            else:
                error_count += 1
        
        return success_count, error_count 