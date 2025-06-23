import pytest
from playwright.sync_api import Browser, BrowserContext, Page, Playwright
from pathlib import Path
import os
from datetime import datetime
from typing import Generator

@pytest.fixture(scope="session")
def browser_type_launch_args(pytestconfig):
    """浏览器启动参数"""
    return {
        "headless": False,
        "slow_mo": 100,
        "args": [
            "--disable-blink-features=AutomationControlled",
            "--disable-extensions",
            "--no-sandbox",
            "--disable-dev-shm-usage",
        ]
    }

@pytest.fixture(scope="session")
def browser_context_args(browser_type_launch_args):
    """浏览器上下文参数"""
    return {
        "viewport": {"width": 1920, "height": 1080},
        "ignore_https_errors": True,
        "record_video_dir": "reports/videos/",
        "record_video_size": {"width": 1920, "height": 1080}
    }

@pytest.fixture(scope="function")
def page(context: BrowserContext) -> Generator[Page, None, None]:
    """页面fixture"""
    page = context.new_page()
    
    # 设置默认超时时间
    page.set_default_timeout(30000)
    page.set_default_navigation_timeout(30000)
    
    # 监听控制台日志
    page.on("console", lambda msg: print(f"浏览器控制台: {msg.text}"))
    
    # 监听页面错误
    page.on("pageerror", lambda error: print(f"页面错误: {error}"))
    
    yield page
    
    # 测试失败时截图
    if hasattr(pytest, "current_test_failed") and pytest.current_test_failed:
        screenshot_path = f"reports/screenshots/failed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"测试失败截图已保存: {screenshot_path}")
    
    page.close()

@pytest.fixture(autouse=True)
def test_info(request):
    """测试信息fixture"""
    test_name = request.node.name
    test_file = request.node.fspath.basename
    
    print(f"开始执行测试: {test_file}::{test_name}")
    
    # 标记测试开始
    pytest.current_test_failed = False
    
    def fin():
        if request.node.rep_call.failed:
            pytest.current_test_failed = True
            print(f"测试失败: {test_file}::{test_name}")
        else:
            print(f"测试通过: {test_file}::{test_name}")
    
    request.addfinalizer(fin)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """生成测试报告钩子"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)

@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """设置测试环境"""
    # 创建必要的目录
    directories = [
        "reports",
        "reports/screenshots", 
        "reports/videos",
        "reports/allure-results",
        "test_data"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
    
    print("测试环境初始化完成")
    
    yield
    
    print("测试环境清理完成") 