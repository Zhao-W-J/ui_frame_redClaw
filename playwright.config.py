from playwright.sync_api import Playwright
import os

def pytest_playwright_configure(playwright: Playwright):
    """Playwright配置"""
    # 浏览器配置
    playwright.chromium.launch_persistent_context(
        user_data_dir="",
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
    )

# Playwright配置选项
BROWSER_CONFIG = {
    "headless": False,  # 是否无头模式
    "slow_mo": 100,     # 操作间隔时间(ms)
    "timeout": 30000,   # 默认超时时间(ms)
    "viewport": {
        "width": 1920,
        "height": 1080
    },
    "video": "retain-on-failure",  # 视频录制
    "screenshot": "only-on-failure",  # 截图
}

# 浏览器类型配置
BROWSERS = {
    "chromium": {
        "channel": "chrome",
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
    },
    "firefox": {},
    "webkit": {}
}

# 环境配置
BASE_URL = os.getenv("BASE_URL", "https://example.com")
TEST_ENV = os.getenv("TEST_ENV", "dev") 