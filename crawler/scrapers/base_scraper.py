import asyncio
import hashlib
import uuid
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Any, Optional, List
from playwright.async_api import async_playwright, Page, Browser, BrowserContext
from playwright_stealth import stealth_async
from ..utils.kafka_producer import KafkaProducerManager
from ..config.settings import CrawlerSettings

class BaseScraper(ABC):
    """
    基础爬虫类 - 统一狩猎规范，优雅且致命
    """
    
    def __init__(self, source_name: str, source_type: str = 'web'):
        self.source_id = str(uuid.uuid4())
        self.source_name = source_name
        self.source_type = source_type
        self.settings = CrawlerSettings()
        self.producer = KafkaProducerManager()
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.success_count = 0
        self.error_count = 0
    
    async def initialize_browser(self):
        """初始化浏览器 - 精密武器的校准过程"""
        self.playwright = await async_playwright().start()
        
        # 更精细的浏览器配置
        launch_options = {
            'headless': self.settings.PLAYWRIGHT_HEADLESS,
            'args': [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--disable-gpu',
                '--window-size=1920,1080',
                '--disable-blink-features=AutomationControlled'
            ]
        }
        
        if self.settings.USE_PROXY:
            launch_options['proxy'] = {'server': self.settings.PROXY_SERVER}
        
        self.browser = await self.playwright.chromium.launch(**launch_options)
        
        # 使用独立的上下文，更好的内存管理
        self.context = await self.browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        )
        
        self.page = await self.context.new_page()
        
        # 应用隐身技术
        if self.settings.STEALTH_ENABLED:
            await stealth_async(self.page)
        
        self.page.set_default_timeout(self.settings.PLAYWRIGHT_TIMEOUT)
    
    async def wait_for_page_ready(self, selectors: List[str] = None):
        """智能等待页面就绪 - 如同精确判断猎物的最佳时机"""
        if self.page:
            # 基础网络等待
            await self.page.wait_for_load_state('networkidle')
            
            # 等待特定选择器（如果有的话）
            if selectors:
                for selector in selectors:
                    try:
                        await self.page.wait_for_selector(selector, timeout=5000)
                    except Exception:
                        print(f"[Warning] 选择器 {selector} 未找到，继续执行...")
            
            # 额外等待动态内容
            await asyncio.sleep(self.settings.REQUEST_DELAY)
    
    def calculate_content_hash(self, content: str) -> str:
        """计算内容哈希 - 独特的DNA标记"""
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    async def save_to_kafka(self, data: Dict[str, Any]) -> bool:
        """将数据发送到Kafka - 优雅的收获过程"""
        try:
            data['source_id'] = self.source_id
            data['source_name'] = self.source_name
            data['source_type'] = self.source_type
            
            success = await self.producer.send_message(
                self.settings.KAFKA_CAPTURE_TOPIC, 
                data
            )
            
            if success:
                self.success_count += 1
            else:
                self.error_count += 1
            
            return success
        except Exception as e:
            print(f"[Error] Kafka保存失败: {str(e)}")
            self.error_count += 1
            return False
    
    @abstractmethod
    async def extract_data(self) -> Dict[str, Any]:
        """抽取数据的抽象方法 - 每个狩猎技巧的核心"""
        pass
    
    async def close(self):
        """关闭资源 - 战场清理，留下优雅背影"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        if self.producer:
            await self.producer.close()
        
        print(f"\n[Statistics] 成功: {self.success_count}, 失败: {self.error_count}")
    
    async def run(self):
        """运行爬虫 - 开启狩猎盛宴"""
        data = None
        run_successful = False
        try:
            print("[BaseScraper.run] Initializing browser...")
            await self.initialize_browser()
            print("[BaseScraper.run] Browser initialized. Extracting data...")
            data = await self.extract_data()
            print(f"[BaseScraper.run] Data extracted: {type(data)}")
            if isinstance(data, dict):
                 run_successful = True # Mark as successful if data extraction returned a dict
        except Exception as e:
            print(f"[Critical] 爬虫执行异常 in run try block: {str(e)}")
            # Attempt to save error
            if hasattr(self, 'producer') and self.producer:
                 try:
                     await self.save_to_kafka({ # This might fail if producer isn't initialized
                         "error": str(e),
                         "metadata": {
                             "type": "error",
                             "source": self.source_name,
                             "timestamp": datetime.now().isoformat()
                         }
                     })
                 except Exception as kafka_err:
                     print(f"[Critical] Failed to save critical error to Kafka: {kafka_err}")
            # data remains None
        finally:
            print("[BaseScraper.run] Entering finally block...")
            await self.close()
            print("[BaseScraper.run] Exiting finally block.")

        if not run_successful:
             print("[BaseScraper.run] Run was not successful, returning None.")
             return None
        else:
             print(f"[BaseScraper.run] Run successful, returning data of type {type(data)}.")
             return data 