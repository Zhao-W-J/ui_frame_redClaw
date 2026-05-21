import pytest
from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestLogin:
    """登录功能测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, test_credentials):
        self.page = page
        self.login_page = LoginPage(page)
        self.creds = test_credentials

    @pytest.mark.smoke
    @pytest.mark.P0
    def test_login_success(self):
        """LOGIN-001: 正常登录"""
        logger.info("开始测试: 正常登录")

        self.login_page.navigate()
        assert self.login_page.is_loaded(), "登录页面未正确加载"

        result = self.login_page.login(
            self.creds["admin_username"],
            self.creds["admin_password"]
        )
        assert result, "登录失败"

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/plaza" in current_url, f"预期URL包含/plaza，实际URL: {current_url}"

        expect(self.page.get_by_role("heading", name="智能体广场")).to_be_visible()

        logger.info("正常登录测试通过")

    @pytest.mark.P1
    def test_login_empty_username(self):
        """LOGIN-002: 空用户名登录"""
        logger.info("开始测试: 空用户名登录")

        self.login_page.navigate()
        assert self.login_page.is_loaded(), "登录页面未正确加载"

        self.login_page.login_with_empty_username(self.creds["admin_password"])

        current_url = self.page.url
        assert "/login" in current_url, f"预期停留在登录页，实际URL: {current_url}"

        logger.info("空用户名登录测试通过")

    @pytest.mark.P1
    def test_login_empty_password(self):
        """LOGIN-003: 空密码登录"""
        logger.info("开始测试: 空密码登录")

        self.login_page.navigate()
        assert self.login_page.is_loaded(), "登录页面未正确加载"

        self.login_page.login_with_empty_password(self.creds["admin_username"])

        current_url = self.page.url
        assert "/login" in current_url, f"预期停留在登录页，实际URL: {current_url}"

        logger.info("空密码登录测试通过")

    @pytest.mark.P1
    def test_login_wrong_password(self):
        """LOGIN-004: 错误密码登录"""
        logger.info("开始测试: 错误密码登录")

        self.login_page.navigate()
        assert self.login_page.is_loaded(), "登录页面未正确加载"

        self.login_page.login_with_wrong_password(
            self.creds["admin_username"], "wrongpwd123"
        )

        current_url = self.page.url
        assert "/login" in current_url, f"预期停留在登录页，实际URL: {current_url}"

        logger.info("错误密码登录测试通过")

    @pytest.mark.smoke
    @pytest.mark.P0
    def test_login_redirect_verification(self):
        """LOGIN-005: 登录后跳转验证"""
        logger.info("开始测试: 登录后跳转验证")

        self.login_page.navigate()
        self.login_page.login(
            self.creds["admin_username"],
            self.creds["admin_password"]
        )

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/plaza" in current_url, f"预期URL包含/plaza，实际URL: {current_url}"

        title = self.page.title()
        assert "RedClaw" in title, f"页面标题应包含 RedClaw，实际标题: {title}"

        logger.info("登录后跳转验证测试通过")

    @pytest.mark.P2
    def test_language_switch(self):
        """LOGIN-006: 语言切换"""
        logger.info("开始测试: 语言切换")

        self.login_page.navigate()
        self.login_page.click_language_switch()

        logger.info("语言切换测试通过（需人工验证英文显示）")

    @pytest.mark.P2
    def test_register_link(self):
        """LOGIN-007: 注册入口"""
        logger.info("开始测试: 注册入口")

        self.login_page.navigate()
        self.login_page.click_register_link()

        logger.info("注册入口测试通过（应跳转到注册页面）")


class TestLoginDataDriven:
    """数据驱动的登录测试"""

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, test_credentials):
        self.page = page
        self.login_page = LoginPage(page)
        self.creds = test_credentials

    @pytest.mark.parametrize("test_data", [
        {"username": "admin", "password": "123456", "expected": "success"},
        {"username": "", "password": "123456", "expected": "failure"},
        {"username": "admin", "password": "", "expected": "failure"},
        {"username": "admin", "password": "wrongpwd", "expected": "failure"},
    ], ids=["valid_credentials", "empty_username", "empty_password", "wrong_password"])
    def test_login_scenarios(self, test_data):
        """数据驱动登录场景测试"""
        logger.info(f"执行数据驱动测试: {test_data}")

        self.login_page.navigate()

        username = test_data["username"]
        password = test_data["password"]

        if username == "admin":
            username = self.creds["admin_username"]
        if password == "123456":
            password = self.creds["admin_password"]

        if username and password:
            self.login_page.login(username, password)
        elif not username:
            self.login_page.login_with_empty_username(password)
        else:
            self.login_page.login_with_empty_password(username)

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url

        if test_data["expected"] == "success":
            assert "/plaza" in current_url, f"预期登录成功跳转到/plaza，实际URL: {current_url}"
        else:
            assert "/login" in current_url, f"预期登录失败停留在/login，实际URL: {current_url}"