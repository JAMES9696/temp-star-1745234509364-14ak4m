import asyncio
import random
from typing import Dict, Any, List
from datetime import datetime
from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from .base_scraper import BaseScraper

class ZhihuScraper(BaseScraper):
    """
    知乎爬虫 - 精准猎取高质量知识
    """
    
    def __init__(self):
        super().__init__(source_name="知乎", source_type="q&a")
        self.base_url = "https://www.zhihu.com"
    
    async def _safe_extract_text(self, element, default: str = "") -> str:
        """安全地提取元素文本"""
        try:
            if element:
                return (await element.inner_text()).strip()
            return default
        except Exception as e:
            print(f"[Warning] 提取文本失败: {str(e)}")
            return default
    
    async def _safe_get_attribute(self, element, attr: str, default: str = "") -> str:
        """安全地获取元素属性"""
        try:
            if element:
                value = await element.get_attribute(attr)
                return value if value else default
            return default
        except Exception as e:
            print(f"[Warning] 获取属性失败: {str(e)}")
            return default
    
    async def _handle_anti_crawler(self):
        """处理反爬虫机制 - 模拟人类行为"""
        try:
            # 随机滚动页面
            await self.page.evaluate("""
                window.scrollTo({
                    top: Math.random() * document.body.scrollHeight,
                    behavior: 'smooth'
                });
            """)
            
            # 随机鼠标移动
            await self.page.mouse.move(
                random.randint(0, 800),
                random.randint(0, 600)
            )
            
            # 模拟人类行为的随机延迟
            await asyncio.sleep(self.settings.REQUEST_DELAY * (0.5 + random.random()))
            
        except Exception as e:
            print(f"[Warning] 反爬虫处理失败: {str(e)}")
    
    async def extract_data(self) -> Dict[str, Any]:
        """
        从知乎提取数据 - 采用更智能的狩猎策略
        """
        try:
            # 访问知乎热榜页面
            print("[Info] 正在访问知乎热榜页面...")
            await self.page.goto(f"{self.base_url}/hot", wait_until='networkidle')
            
            # 等待页面加载
            print("[Info] 等待页面加载...")
            await self.page.wait_for_load_state('domcontentloaded')
            await asyncio.sleep(2)  # 给页面一些额外的加载时间
            
            # 获取页面HTML
            page_content = await self.page.content()
            if "知乎" not in page_content:
                raise Exception("页面加载不完整")
            
            # 应用反爬虫策略
            await self._handle_anti_crawler()
            
            # 尝试不同的选择器
            selectors = [
                ".HotList-list .HotItem",  # 原始选择器
                ".HotList .HotItem",       # 简化选择器
                "[data-za-detail-view-path-module='item']",  # 数据属性选择器
                ".Card.HotItem"            # 备用选择器
            ]
            
            hot_items = None
            for selector in selectors:
                print(f"[Info] 尝试选择器: {selector}")
                hot_items = await self.page.query_selector_all(selector)
                if hot_items and len(hot_items) > 0:
                    print(f"[Success] 找到 {len(hot_items)} 个热榜项目")
                    break
            
            if not hot_items or len(hot_items) == 0:
                raise Exception("未能找到任何热榜项目")
            
            results = []
            for item in hot_items[:5]:  # 获取前5个热榜项目
                try:
                    # 提取标题（尝试多个可能的选择器）
                    title = ""
                    for title_selector in [".HotItem-title", "h2", ".title"]:
                        title_element = await item.query_selector(title_selector)
                        title = await self._safe_extract_text(title_element)
                        if title:
                            break
                    
                    if not title:
                        print("[Warning] 跳过：未找到标题")
                        continue
                    
                    # 提取链接
                    link = ""
                    link_element = await item.query_selector("a")
                    link = await self._safe_get_attribute(link_element, "href", "")
                    
                    # 处理相对链接
                    if link and not link.startswith("http"):
                        link = f"{self.base_url}{link}"
                    
                    if not link:
                        print("[Warning] 跳过：未找到链接")
                        continue
                    
                    # 提取热度信息（尝试多个可能的选择器）
                    metrics = ""
                    for metrics_selector in [".HotItem-metrics", ".metrics", ".hot-rank"]:
                        metrics_element = await item.query_selector(metrics_selector)
                        metrics = await self._safe_extract_text(metrics_element)
                        if metrics:
                            break
                    
                    result = {
                        "url": link,
                        "title": title,
                        "original_content": f"热榜标题: {title}\n热度: {metrics}",
                        "metadata": {
                            "type": "hot_item",
                            "platform": "zhihu",
                            "language": "zh-CN",
                            "extract_time": datetime.now().isoformat(),
                            "metrics": metrics
                        }
                    }
                    
                    # 单独发送每个热榜项目
                    print(f"[Info] 发送数据: {title}")
                    success = await self.save_to_kafka(result)
                    if success:
                        results.append(result)
                        print("[Success] 数据发送成功")
                    
                    # 添加延时，避免过于频繁
                    await asyncio.sleep(1)
                    
                except Exception as e:
                    print(f"[Warning] 处理热榜项目失败: {str(e)}")
                    continue
            
            if not results:
                error_data = {
                    "error": "未找到有效的热榜数据",
                    "metadata": {
                        "type": "error",
                        "platform": "zhihu",
                        "timestamp": datetime.now().isoformat()
                    }
                }
                await self.save_to_kafka(error_data)
                return error_data
            
            print(f"[Info] 成功提取 {len(results)} 个热榜项目")
            return results[0]
            
        except PlaywrightTimeoutError as e:
            error_data = {
                "error": f"页面加载超时: {str(e)}",
                "metadata": {
                    "type": "error",
                    "platform": "zhihu",
                    "timestamp": datetime.now().isoformat()
                }
            }
            await self.save_to_kafka(error_data)
            return error_data
            
        except Exception as e:
            error_data = {
                "error": f"知乎爬虫遇到异常: {str(e)}",
                "metadata": {
                    "type": "error",
                    "platform": "zhihu",
                    "timestamp": datetime.now().isoformat()
                }
            }
            await self.save_to_kafka(error_data)
            return error_data 