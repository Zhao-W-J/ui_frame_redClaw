import pytest
from playwright.sync_api import Page, expect
from pages.admin_page import AdminPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestAdminDashboard:
    """公司管理 - 公司仪表盘"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.admin_page = AdminPage(self.page)
        self.admin_page.navigate()

    @pytest.mark.smoke
    @pytest.mark.P1
    def test_admin_page_loads(self):
        """ADMIN-001: 进入公司设置"""
        logger.info("开始测试: 进入公司设置")

        assert self.admin_page.is_loaded(), "公司管理页面未正确加载"

        expect(self.page.get_by_role("heading", name="公司设置")).to_be_visible()

        logger.info("进入公司设置测试通过")

    @pytest.mark.P1
    def test_dashboard_metrics_visible(self):
        """ADMIN-002: 公司仪表盘展示"""
        logger.info("开始测试: 公司仪表盘展示")

        metrics = self.admin_page.get_dashboard_metrics()
        logger.info(f"可见指标: {metrics}")

        assert len(metrics) > 0, "未找到仪表盘指标"

    @pytest.mark.P2
    def test_time_range_buttons_visible(self):
        """ADMIN-003: 时间范围切换按钮可见"""
        logger.info("开始测试: 时间范围切换按钮可见")

        last_7 = self.page.locator('button:has-text("Last 7 Days")')
        expect(last_7).to_be_visible()

        last_30 = self.page.locator('button:has-text("Last 30 Days")')
        expect(last_30).to_be_visible()

        logger.info("时间范围切换按钮可见")


class TestAdminSettings:
    """公司管理 - 公司设置标签"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.admin_page = AdminPage(self.page)
        self.admin_page.navigate()

    @pytest.mark.P1
    def test_switch_to_settings_tab(self):
        """ADMIN-004: 进入公司设置标签"""
        logger.info("开始测试: 进入公司设置标签")

        self.admin_page.click_tab("公司设置")

        settings_tab = self.page.get_by_role("tab", name="公司设置")
        expect(settings_tab).to_be_visible()
        assert settings_tab.get_attribute("aria-selected") == "true", "公司设置标签未选中"

        logger.info("公司设置标签切换成功")

    @pytest.mark.P2
    def test_announcement_section_visible(self):
        """ADMIN-005: 公告栏配置区域可见"""
        logger.info("开始测试: 公告栏配置区域可见")

        self.admin_page.click_tab("公司设置")

        ann_text = self.page.locator('text="公告"')
        expect(ann_text.first).to_be_visible()

        logger.info("公告栏配置区域可见")

    @pytest.mark.P2
    def test_email_config_section_visible(self):
        """ADMIN-006: 邮箱配置区域可见"""
        logger.info("开始测试: 邮箱配置区域可见")

        self.admin_page.click_tab("公司设置")

        email_text = self.page.locator('text="SMTP", text="邮箱"')
        expect(email_text.first).to_be_visible()

        logger.info("邮箱配置区域可见")


class TestAdminDeptManagement:
    """公司管理 - 部门管理标签"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.admin_page = AdminPage(self.page)
        self.admin_page.navigate()

    @pytest.mark.P1
    def test_switch_to_dept_mgmt_tab(self):
        """ADMIN-008: 进入部门管理标签"""
        logger.info("开始测试: 进入部门管理标签")

        self.admin_page.click_tab("部门管理")

        dept_tab = self.page.get_by_role("tab", name="部门管理")
        expect(dept_tab).to_be_visible()
        assert dept_tab.get_attribute("aria-selected") == "true", "部门管理标签未选中"

        logger.info("部门管理标签切换成功")

    @pytest.mark.P2
    def test_create_dept_button_visible(self):
        """ADMIN-009: 创建部门按钮可见"""
        logger.info("开始测试: 创建部门按钮可见")

        self.admin_page.click_tab("部门管理")

        create_btn = self.page.get_by_role("button", name="创建部门")
        expect(create_btn).to_be_visible()

        logger.info("创建部门按钮可见")


class TestAdminModelPool:
    """公司管理 - 公司模型池标签"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.admin_page = AdminPage(self.page)
        self.admin_page.navigate()

    @pytest.mark.P1
    def test_switch_to_model_pool_tab(self):
        """ADMIN-010: 进入公司模型池标签"""
        logger.info("开始测试: 进入公司模型池标签")

        self.admin_page.click_tab("公司模型池")

        model_tab = self.page.get_by_role("tab", name="公司模型池")
        expect(model_tab).to_be_visible()
        assert model_tab.get_attribute("aria-selected") == "true", "公司模型池标签未选中"

        logger.info("公司模型池标签切换成功")


class TestAdminSkills:
    """公司管理 - 技能管理标签"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.admin_page = AdminPage(self.page)
        self.admin_page.navigate()

    @pytest.mark.P1
    def test_switch_to_skills_tab(self):
        """ADMIN-012: 进入技能管理标签"""
        logger.info("开始测试: 进入技能管理标签")

        self.admin_page.click_tab("技能管理")

        skills_tab = self.page.get_by_role("tab", name="技能管理")
        expect(skills_tab).to_be_visible()
        assert skills_tab.get_attribute("aria-selected") == "true", "技能管理标签未选中"

        logger.info("技能管理标签切换成功")


class TestAdminAllTabs:
    """公司管理 - 所有标签页"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.admin_page = AdminPage(self.page)
        self.admin_page.navigate()

    @pytest.mark.P1
    def test_all_tabs_visible(self):
        """ADMIN-ALL: 所有标签页可见"""
        logger.info("开始测试: 所有标签页可见")

        expected_tabs = ["公司仪表盘", "公司设置", "部门管理", "公司模型池", "技能管理"]
        visible_tabs = self.admin_page.get_all_tab_names()
        logger.info(f"可见标签: {visible_tabs}")

        for tab in expected_tabs:
            assert tab in visible_tabs, f"标签 '{tab}' 不可见，可见标签: {visible_tabs}"