import pytest
from playwright.sync_api import Page, expect
from pages.register_page import RegisterPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestRegister:
    """注册功能测试"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        self.page = page
        self.register_page = RegisterPage(page)

    @pytest.mark.P1
    def test_register_page_loads(self):
        """REG-001: 注册页面加载"""
        logger.info("开始测试: 注册页面加载")

        self.register_page.navigate()
        assert self.register_page.is_loaded(), "注册页面未正确加载"

        expect(self.page.get_by_role("button", name="注册")).to_be_visible()

        logger.info("注册页面加载测试通过")

    @pytest.mark.P1
    def test_username_field_visible(self):
        """REG-002: 用户名字段可见"""
        logger.info("开始测试: 用户名字段可见")

        self.register_page.navigate()

        username_input = self.page.get_by_placeholder("用户名")
        expect(username_input).to_be_visible()

        logger.info("用户名输入框可见")

    @pytest.mark.P1
    def test_email_field_visible(self):
        """REG-003: 邮箱字段可见"""
        logger.info("开始测试: 邮箱字段可见")

        self.register_page.navigate()

        email_input = self.page.locator('input[type="email"], input[placeholder*="邮箱"]')
        expect(email_input.first).to_be_visible()

        logger.info("邮箱输入框可见")

    @pytest.mark.P1
    def test_password_field_visible(self):
        """REG-004: 密码字段可见"""
        logger.info("开始测试: 密码字段可见")

        self.register_page.navigate()

        password_input = self.page.locator('input[type="password"]')
        expect(password_input.first).to_be_visible()

        logger.info("密码输入框可见")

    @pytest.mark.P1
    def test_register_button_visible(self):
        """REG-005: 注册按钮可见"""
        logger.info("开始测试: 注册按钮可见")

        self.register_page.navigate()

        register_btn = self.page.get_by_role("button", name="注册")
        expect(register_btn).to_be_visible()

        logger.info("注册按钮可见")

    @pytest.mark.P2
    def test_login_link_visible(self):
        """REG-006: 去登录链接可见"""
        logger.info("开始测试: 去登录链接可见")

        self.register_page.navigate()

        login_link = self.page.locator('a:has-text("登录"), a:has-text("去登录")')
        expect(login_link.first).to_be_visible()

        logger.info("去登录链接可见")

    @pytest.mark.P2
    def test_click_login_link(self):
        """REG-007: 点击去登录链接"""
        logger.info("开始测试: 点击去登录链接")

        self.register_page.navigate()

        login_link = self.page.locator('a:has-text("登录"), a:has-text("去登录")')
        expect(login_link.first).to_be_visible()
        login_link.first.click()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/login" in current_url, f"预期跳转到登录页，实际URL: {current_url}"

        logger.info("跳转到登录页成功")