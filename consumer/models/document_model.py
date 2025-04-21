from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Dict, Any, Optional

class DocumentModel(BaseModel):
    """文档模型 - 数据的标准化容器"""
    
    doc_id: Optional[str] = None
    source_id: str
    source_name: Optional[str] = None
    source_type: Optional[str] = None
    title: Optional[str] = None
    url: Optional[str] = None
    content_hash: str
    original_content: str
    processed_content: Optional[str] = None
    summary: Optional[str] = None
    visibility: str = 'private'
    doc_type: str = 'article'
    metadata: Dict[str, Any] = Field(default_factory=dict)
    capture_timestamp: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    @validator('capture_timestamp', 'created_at', 'updated_at', pre=True)
    def parse_datetime(cls, value):
        if isinstance(value, str):
            return datetime.fromisoformat(value)
        return value
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        } 