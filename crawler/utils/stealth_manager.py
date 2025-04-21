import random
import time
from selenium.webdriver.common.action_chains import ActionChains

class StealthManager:
    @staticmethod
    def random_sleep(min_seconds=2, max_seconds=5):
        """随机休眠"""
        time.sleep(random.uniform(min_seconds, max_seconds))
        
    @staticmethod
    def random_scroll(driver):
        """随机滚动页面"""
        scroll_height = random.randint(300, 1000)
        driver.execute_script(f"window.scrollBy(0, {scroll_height});")
        time.sleep(random.uniform(0.5, 1.5))
        
    @staticmethod
    def random_mouse_movement(driver):
        """随机鼠标移动"""
        action = ActionChains(driver)
        x_offset = random.randint(-100, 100)
        y_offset = random.randint(-100, 100)
        action.move_by_offset(x_offset, y_offset)
        action.perform()
        
    @staticmethod
    def random_user_agent():
        """生成随机User-Agent"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0"
        ]
        return random.choice(user_agents) 