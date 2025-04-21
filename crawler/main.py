import asyncio
import sys
import traceback
from datetime import datetime
from dotenv import load_dotenv
from crawler.scrapers.zhihu_scraper import ZhihuScraper
from crawler.utils.kafka_producer import KafkaProducerManager
from crawler.utils.stealth_manager import StealthManager
from crawler.config.settings import CrawlerSettings

class CrawlerManager:
    """爬虫管理器 - 统筹整个狩猎行动"""
    
    def __init__(self):
        self.settings = CrawlerSettings()
        self.start_time = None
        
    def print_banner(self):
        """打印启动横幅"""
        banner = """
╭──────────────────────────────────────╮
│     🌟 星际罗盘爬虫系统 - v1.0      │
│      StarCompass Crawler System      │
╰──────────────────────────────────────╯
        """
        print(banner)
        
    def print_status(self, message: str, status: str = "INFO"):
        """打印状态信息"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{status}] {message}")
        
    async def run_crawler(self):
        """运行爬虫"""
        scraper = None
        try:
            self.start_time = datetime.now()
            self.print_banner()
            self.print_status("系统初始化...")
            
            # 创建并运行知乎爬虫
            scraper = ZhihuScraper()
            self.print_status("开始数据采集...")
            await scraper.run()
            
            # 计算运行时间
            end_time = datetime.now()
            duration = (end_time - self.start_time).total_seconds()
            self.print_status(f"任务完成！总耗时: {duration:.2f} 秒")
            
        except KeyboardInterrupt:
            self.print_status("收到中断信号，正在优雅关闭...", "WARN")
            if scraper:
                await scraper.close()
            sys.exit(0)
            
        except Exception as e:
            self.print_status(f"发生错误: {str(e)}", "ERROR")
            self.print_status("错误详情:", "ERROR")
            traceback.print_exc()
            if scraper:
                await scraper.close()
            sys.exit(1)

async def main():
    """
    主程序 - 狩猎开始
    """
    manager = CrawlerManager()
    await manager.run_crawler()

if __name__ == "__main__":
    # 设置事件循环策略（Windows特定）
    # if sys.platform == "win32":
    #     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    # 运行主程序
    asyncio.run(main()) 