import pytest
from playwright.sync_api import Page
from pages.login_page import LoginPage
from utils.data_manager import DataManager
from utils.logger import get_logger

logger = get_logger(__name__)

class TestLogin:
    """登录功能测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        self.page = page
        self.login_page = LoginPage(page)
        self.test_data = DataManager.get_test_data("login_data.json", "login_test")
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_valid_login(self):
        """测试有效登录"""
        logger.info("开始测试有效登录")
        
        # 导航到登录页面
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "登录页面未正确加载"
        
        # 使用有效凭据登录
        valid_data = self.test_data[0] if self.test_data else {"username": "admin", "password": "password"}
        success = self.login_page.login(
            username=valid_data["username"],
            password=valid_data["password"]
        )
        
        assert success, "有效凭据登录失败"
        logger.info("有效登录测试通过")
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_invalid_login(self):
        """测试无效登录"""
        logger.info("开始测试无效登录")
        
        # 导航到登录页面
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "登录页面未正确加载"
        
        # 使用无效凭据登录
        success = self.login_page.login(
            username="invalid_user",
            password="invalid_password"
        )
        
        assert not success, "无效凭据应该登录失败"
        
        # 检查错误信息
        error_message = self.login_page.get_error_message()
        assert error_message, "应该显示错误信息"
        logger.info(f"无效登录测试通过，错误信息: {error_message}")
    
    @pytest.mark.regression
    @pytest.mark.ui
    def test_empty_credentials(self):
        """测试空凭据登录"""
        logger.info("开始测试空凭据登录")
        
        # 导航到登录页面
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "登录页面未正确加载"
        
        # 使用空凭据登录
        success = self.login_page.login(username="", password="")
        
        assert not success, "空凭据应该登录失败"
        logger.info("空凭据登录测试通过")
    
    @pytest.mark.ui
    def test_login_form_elements(self):
        """测试登录表单元素"""
        logger.info("开始测试登录表单元素")
        
        # 导航到登录页面
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "登录页面未正确加载"
        
        # 检查表单元素是否可见
        assert self.login_page.is_login_form_visible(), "登录表单元素应该可见"
        
        # 检查页面标题
        title = self.login_page.get_page_title()
        assert "登录" in title or "Login" in title, f"页面标题应包含登录相关字样，实际标题: {title}"
        
        logger.info("登录表单元素测试通过")
    
    @pytest.mark.parametrize("username,password,expected_result", [
        ("admin", "password", True),
        ("user", "123456", True),
        ("invalid", "wrong", False),
        ("", "", False),
    ])
    @pytest.mark.ui
    def test_login_with_different_credentials(self, username, password, expected_result):
        """测试不同凭据的登录"""
        logger.info(f"测试登录凭据: {username}/{password}")
        
        # 导航到登录页面
        self.login_page.navigate()
        assert self.login_page.is_loaded(), "登录页面未正确加载"
        
        # 执行登录
        result = self.login_page.login(username, password)
        
        assert result == expected_result, f"登录结果不符合预期: 预期={expected_result}, 实际={result}"
        logger.info(f"登录凭据测试通过: {username}/{password}")
    
    def teardown_method(self):
        """测试后置清理"""
        logger.info("执行测试清理")
        # 这里可以添加清理逻辑，比如登出、清空缓存等 