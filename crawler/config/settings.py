from typing import Dict
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class CrawlerSettings:
    """爬虫配置设置 - 如同精密的狩猎装备清单"""
    
    # Kafka配置
    KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    KAFKA_CAPTURE_TOPIC = os.getenv('KAFKA_CAPTURE_TOPIC', 'worldlora.capture.raw')
    
    # Playwright配置
    PLAYWRIGHT_HEADLESS = os.getenv('PLAYWRIGHT_HEADLESS', 'True').lower() == 'true'
    PLAYWRIGHT_TIMEOUT = int(os.getenv('PLAYWRIGHT_TIMEOUT', 30000))
    
    # 代理配置
    USE_PROXY = os.getenv('USE_PROXY', 'False').lower() == 'true'
    PROXY_SERVER = os.getenv('PROXY_SERVER', '')
    
    # 反爬配置
    STEALTH_ENABLED = os.getenv('STEALTH_ENABLED', 'True').lower() == 'true'
    REQUEST_DELAY = int(os.getenv('REQUEST_DELAY', 2))
    
    # 爬虫通用配置
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    BACKOFF_FACTOR = float(os.getenv('BACKOFF_FACTOR', 1.5))

    @classmethod
    def get_playwright_launch_options(cls) -> Dict:
        """获取Playwright启动选项"""
        options = {
            "headless": cls.PLAYWRIGHT_HEADLESS,
            "timeout": cls.PLAYWRIGHT_TIMEOUT,
        }
        
        if cls.USE_PROXY and cls.PROXY_SERVER:
            options["proxy"] = {
                "server": cls.PROXY_SERVER
            }
            
        return options
        
    @classmethod
    def get_context_options(cls) -> Dict:
        """获取浏览器上下文选项"""
        return {
            "viewport": {
                "width": 1920,
                "height": 1080
            },
            "ignore_https_errors": True,
            "java_script_enabled": True,
            "bypass_csp": True,  # 绕过内容安全策略
        }
        
    @classmethod
    def get_stealth_options(cls) -> Dict:
        """获取反爬虫选项"""
        return {
            "enable_stealth": cls.STEALTH_ENABLED,
            "delay": cls.REQUEST_DELAY,
            "max_retries": cls.MAX_RETRIES,
            "backoff_factor": cls.BACKOFF_FACTOR
        }

# 浏览器设置
BROWSER_HEADLESS = False
BROWSER_TIMEOUT = 30

# 知乎相关设置
ZHIHU_BASE_URL = "https://www.zhihu.com"
ZHIHU_LOGIN_URL = f"{ZHIHU_BASE_URL}/signin"

# Kafka设置
KAFKA_TOPIC = "zhihu_data"

# 代理设置
PROXY_ENABLED = False
PROXY_HOST = os.getenv("PROXY_HOST", "")
PROXY_PORT = os.getenv("PROXY_PORT", "")

# 用户代理设置
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36" 