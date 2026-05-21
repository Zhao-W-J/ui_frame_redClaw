import pytest
from playwright.sync_api import Page, expect
from pages.plaza_page import PlazaPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestGlobalNavigation:
    """全局导航测试"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.plaza_page = PlazaPage(self.page)
        self.plaza_page.navigate()

    @pytest.mark.P1
    def test_navigate_to_dashboard(self):
        """NAV-001: 导航到仪表盘"""
        logger.info("开始测试: 导航到仪表盘")

        dashboard_link = self.page.get_by_role("link", name="仪表盘")
        expect(dashboard_link).to_be_visible()
        dashboard_link.click()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/dashboard" in current_url, f"预期URL包含/dashboard，实际URL: {current_url}"

        logger.info("导航到仪表盘成功")

    @pytest.mark.P1
    def test_navigate_to_new_agent(self):
        """NAV-002: 导航到新建数字员工"""
        logger.info("开始测试: 导航到新建数字员工")

        new_agent_link = self.page.get_by_role("link", name="新建数字员工")
        expect(new_agent_link).to_be_visible()
        new_agent_link.click()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/create" in current_url or "/new" in current_url, \
            f"预期URL包含/create或/new，实际URL: {current_url}"

        logger.info("导航到新建数字员工成功")

    @pytest.mark.P1
    def test_navigate_to_enterprise(self):
        """NAV-003: 导航到部门设置"""
        logger.info("开始测试: 导航到部门设置")

        enterprise_link = self.page.get_by_role("link", name="部门设置")
        expect(enterprise_link).to_be_visible()
        enterprise_link.click()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/enterprise" in current_url, f"预期URL包含/enterprise，实际URL: {current_url}"

        logger.info("导航到部门设置成功")

    @pytest.mark.P1
    def test_navigate_to_admin(self):
        """NAV-004: 导航到公司设置"""
        logger.info("开始测试: 导航到公司设置")

        admin_link = self.page.get_by_role("link", name="公司设置")
        expect(admin_link).to_be_visible()
        admin_link.click()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/admin" in current_url, f"预期URL包含/admin，实际URL: {current_url}"

        logger.info("导航到公司设置成功")

    @pytest.mark.P1
    def test_navigate_back_to_plaza(self):
        """NAV-005: 导航回广场"""
        logger.info("开始测试: 导航回广场")

        plaza_link = self.page.get_by_role("link", name="广场")
        expect(plaza_link).to_be_visible()
        plaza_link.click()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/plaza" in current_url, f"预期URL包含/plaza，实际URL: {current_url}"

        logger.info("导航回广场成功")


class TestGlobalFeatures:
    """全局功能测试"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.plaza_page = PlazaPage(self.page)
        self.plaza_page.navigate()

    @pytest.mark.P2
    def test_dark_mode_toggle(self):
        """GLOBAL-001: 深色模式切换"""
        logger.info("开始测试: 深色模式切换")

        dark_mode_btn = self.page.get_by_role("button", name="深色模式")
        expect(dark_mode_btn).to_be_visible()
        dark_mode_btn.click()

        html = self.page.locator('html')
        theme = html.get_attribute("data-theme")
        logger.info(f"当前主题: {theme}")

    @pytest.mark.P2
    def test_notification_button_visible(self):
        """GLOBAL-002: 通知按钮可见"""
        logger.info("开始测试: 通知按钮可见")

        notification_btn = self.page.locator('[aria-label*="通知"], button:has-text("通知")')
        expect(notification_btn.first).to_be_visible()

        logger.info("通知按钮可见")

    @pytest.mark.P2
    def test_switch_department_button_visible(self):
        """GLOBAL-003: 切换部门按钮可见"""
        logger.info("开始测试: 切换部门按钮可见")

        switch_btn = self.page.get_by_role("button", name="切换部门")
        expect(switch_btn).to_be_visible()

        logger.info("切换部门按钮可见")

    @pytest.mark.P2
    def test_user_menu_visible(self):
        """GLOBAL-004: 用户菜单可见"""
        logger.info("开始测试: 用户菜单可见")

        user_area = self.page.locator('[class*="user"], [class*="avatar"], [class*="profile"]')
        assert user_area.count() > 0, "未找到用户菜单区域"

        logger.info(f"用户区域元素数量: {user_area.count()}")

    @pytest.mark.P2
    def test_search_input_visible(self):
        """GLOBAL-005: 搜索输入框可见"""
        logger.info("开始测试: 搜索输入框可见")

        search_input = self.page.get_by_placeholder("搜索...")
        expect(search_input).to_be_visible()

        logger.info("搜索输入框可见")


class TestUserProfile:
    """账号设置/个人资料测试"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.plaza_page = PlazaPage(self.page)
        self.plaza_page.navigate()

    @pytest.mark.P1
    def test_user_menu_click(self):
        """PROF-001: 打开用户菜单"""
        logger.info("开始测试: 打开用户菜单")

        user_avatar = self.page.locator('[class*="avatar"], [class*="user-menu"], button:has-text("admin")')
        expect(user_avatar.first).to_be_visible()
        user_avatar.first.click()

        admin_text = self.page.locator('text="admin"')
        expect(admin_text.first).to_be_visible()

        logger.info("用户菜单打开成功，显示admin用户名")

    @pytest.mark.P2
    def test_logout_visible(self):
        """PROF-005: 退出登录可见"""
        logger.info("开始测试: 退出登录可见")

        user_avatar = self.page.locator('[class*="avatar"], [class*="user-menu"], button:has-text("admin")')
        expect(user_avatar.first).to_be_visible()
        user_avatar.first.click()

        logout_text = self.page.locator('text="退出登录"')
        expect(logout_text.first).to_be_visible()

        logger.info("退出登录选项可见")


class TestMessages:
    """消息中心测试"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.plaza_page = PlazaPage(self.page)
        self.plaza_page.navigate()

    @pytest.mark.P1
    def test_notification_click(self):
        """MSG-001: 点击通知按钮"""
        logger.info("开始测试: 点击通知按钮")

        notification_btn = self.page.locator('[aria-label*="通知"], button:has-text("通知")')
        expect(notification_btn.first).to_be_visible()
        notification_btn.first.click()

        logger.info("通知按钮点击成功")

    @pytest.mark.P2
    def test_messages_page_navigate(self):
        """MSG-002: 导航到消息中心"""
        logger.info("开始测试: 导航到消息中心")

        self.page.goto(f"{self.plaza_page.base_url}/messages")
        self.page.wait_for_load_state("networkidle")

        current_url = self.page.url
        assert "/messages" in current_url, f"预期URL包含/messages，实际URL: {current_url}"

        logger.info("消息中心页面加载成功")