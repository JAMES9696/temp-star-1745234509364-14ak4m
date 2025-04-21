import asyncio
import sys
from crawler.scrapers.zhihu_scraper import ZhihuScraper

async def main():
    print("=== 知乎爬虫测试开始 ===")
    
    try:
        # 创建爬虫实例
        scraper = ZhihuScraper()
        
        # 运行爬虫
        print("\n[Info] 开始爬取知乎热榜...")
        result = await scraper.run()
        
        # 输出结果
        print("\n[Info] 爬取结果:")
        if result is None:
            print("[Error] 未获取到任何结果")
            sys.exit(1)
            
        if isinstance(result, dict):
            if "error" in result:
                print(f"[Error] 爬取失败: {result['error']}")
                print(f"元数据: {result.get('metadata', {})}")
            else:
                print(f"标题: {result.get('title', '无标题')}")
                print(f"链接: {result.get('url', '无链接')}")
                print(f"内容: {result.get('original_content', '无内容')}")
                print(f"元数据: {result.get('metadata', {})}")
        else:
            print(f"[Error] 意外的结果类型: {type(result)}")
            print(f"结果内容: {result}")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"[Critical] 测试过程中发生错误: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 