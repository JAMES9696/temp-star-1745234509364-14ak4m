import json
import hashlib
from bs4 import BeautifulSoup
import spacy
from datetime import datetime
import re

class DocumentCleaningFunction:
    def __init__(self):
        """初始化清洗函数"""
        try:
            self.nlp = spacy.load('zh_core_web_md')  # 中文NLP模型
        except OSError:
            # 如果模型未下载，使用基础模型
            self.nlp = spacy.blank('zh')
            print("警告: 使用基础中文模型，实体识别可能不准确")
        
    def clean(self, value: str) -> str:
        """清洗单个文档"""
        try:
            doc = json.loads(value)
            
            # 1. HTML标签清理
            if 'content' in doc:
                doc['clean_content'] = self._clean_html(doc['content'])
                
            # 2. 元数据提取
            doc['metadata'] = self._extract_metadata(doc)
            
            # 3. 实体识别
            if 'clean_content' in doc:
                doc['entities'] = self._extract_entities(doc['clean_content'])
                
            # 4. 生成摘要
            doc['summaries'] = self._generate_summaries(doc)
            
            # 5. 计算内容哈希
            doc['content_hash'] = self._calculate_hash(doc['clean_content'])
            
            return json.dumps(doc, ensure_ascii=False)
            
        except Exception as e:
            print(f"清洗错误: {e}")
            return json.dumps({"error": str(e), "raw": value}, ensure_ascii=False)
    
    def _clean_html(self, content: str) -> str:
        """清理HTML标签"""
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.get_text()
        return re.sub(r'\s+', ' ', text).strip()
    
    def _extract_metadata(self, doc: dict) -> dict:
        """提取元数据"""
        metadata = {
            'source': doc.get('source', 'unknown'),
            'timestamp': doc.get('timestamp', datetime.now().isoformat()),
            'url': doc.get('url', ''),
            'author': self._extract_author(doc.get('content', '')),
            'language': 'zh'  # 默认中文
        }
        return metadata
    
    def _extract_author(self, content: str) -> str:
        """提取作者信息"""
        author_patterns = [
            r'作者[:：]\s*([^\n]+)',
            r'作者[:：]\s*([^\n]+)',
            r'by\s+([^\n]+)'
        ]
        for pattern in author_patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1).strip()
        return 'unknown'
    
    def _extract_entities(self, text: str) -> list:
        """提取实体"""
        # 使用规则匹配确保能识别到地点
        location_patterns = [
            r'北京|上海|广州|深圳|杭州|成都|武汉|南京|西安|重庆',
            r'[\u4e00-\u9fff]+市',
            r'[\u4e00-\u9fff]+省'
        ]
        
        entities = []
        
        # 添加规则匹配的地点
        for pattern in location_patterns:
            for match in re.finditer(pattern, text):
                entities.append({
                    'text': match.group(),
                    'label': 'LOC'
                })
        
        # 添加NLP识别的实体
        try:
            doc = self.nlp(text[:10000])  # 限制处理长度
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_
                })
        except Exception as e:
            print(f"NLP实体识别错误: {e}")
        
        return entities
    
    def _generate_summaries(self, doc: dict) -> dict:
        """生成摘要"""
        content = doc.get('clean_content', '')
        if not content:
            return {
                'title': doc.get('title', ''),
                'short_summary': '',
                'structured_summary': {
                    'topic': '待分析',
                    'key_points': [],
                    'conclusion': '待生成'
                }
            }
            
        # 简单的摘要生成
        sentences = re.split(r'[。！？.!?]', content)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        return {
            'title': doc.get('title', ''),
            'short_summary': sentences[0] if sentences else '',
            'structured_summary': {
                'topic': sentences[0] if sentences else '待分析',
                'key_points': sentences[1:3] if len(sentences) > 1 else [],
                'conclusion': sentences[-1] if sentences else '待生成'
            }
        }
    
    def _calculate_hash(self, content: str) -> str:
        """计算内容哈希"""
        if not content:
            return None
        return hashlib.sha256(content.encode('utf-8')).hexdigest() 