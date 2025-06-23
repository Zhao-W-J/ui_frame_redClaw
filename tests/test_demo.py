import pytest
from playwright.sync_api import Page
from pages.base_page import BasePage

class DemoPage(BasePage):
    """演示页面类"""
    
    def navigate(self):
        """导航到演示页面"""
        self.page.goto("https://example.com")
    
    def is_loaded(self):
        """检查页面是否加载"""
        return "Example Domain" in self.page.title()

class TestDemo:
    """演示测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试设置"""
        self.page = page
        self.demo_page = DemoPage(page)
    
    @pytest.mark.smoke
    def test_page_load(self):
        """测试页面加载"""
        self.demo_page.navigate()
        assert self.demo_page.is_loaded(), "页面未正确加载"
        
        # 获取页面标题
        title = self.demo_page.get_page_title()
        assert "Example Domain" in title
        
        print("✅ 页面加载测试通过")
    
    @pytest.mark.ui
    def test_basic_operations(self):
        """测试基本操作"""
        self.demo_page.navigate()
        
        # 测试页面基本信息获取
        url = self.demo_page.get_current_url()
        assert "example.com" in url
        
        title = self.demo_page.get_page_title()
        assert title is not None
        
        print("✅ 基本操作测试通过") 