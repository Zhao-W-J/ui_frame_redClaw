import pytest
from playwright.sync_api import Page, expect
from pages.plaza_page import PlazaPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestPlaza:
    """智能体广场功能测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.plaza_page = PlazaPage(self.page)
        self.plaza_page.navigate()

    @pytest.mark.smoke
    @pytest.mark.P0
    def test_plaza_page_loads(self):
        """PLAZA-001: 广场页面加载"""
        logger.info("开始测试: 广场页面加载")

        assert self.plaza_page.is_loaded(), "广场页面未正确加载"

        heading = self.page.get_by_role("heading", name="智能体广场")
        expect(heading).to_be_visible()

        logger.info("广场页面加载测试通过")

    @pytest.mark.P1
    def test_stats_displayed(self):
        """PLAZA-002: 统计数据展示"""
        logger.info("开始测试: 统计数据展示")

        posts_count = self.plaza_page.get_posts_count()
        comments_count = self.plaza_page.get_comments_count()
        today_count = self.plaza_page.get_today_count()

        assert posts_count is not None, "帖子统计未显示"
        assert comments_count is not None, "评论统计未显示"
        assert today_count is not None, "今日统计未显示"

        logger.info(f"统计数据 - 帖子: {posts_count}, 评论: {comments_count}, 今日: {today_count}")
        logger.info("统计数据展示测试通过")

    @pytest.mark.P0
    def test_post_list_displayed(self):
        """PLAZA-003: 帖子列表展示"""
        logger.info("开始测试: 帖子列表展示")

        post_count = self.plaza_page.get_post_list_count()
        assert post_count > 0, f"预期至少显示一条帖子，实际数量: {post_count}"

        logger.info(f"帖子列表数量: {post_count}")
        logger.info("帖子列表展示测试通过")

    @pytest.mark.P1
    def test_delete_post_button_visible(self):
        """PLAZA-005: 删除帖子按钮可见"""
        logger.info("开始测试: 删除帖子按钮可见")

        delete_btn = self.page.get_by_role("button", name="删除帖子")
        expect(delete_btn.first).to_be_visible()

        logger.info("删除帖子按钮可见")

    @pytest.mark.P2
    def test_search_functionality(self):
        """PLAZA-006: 搜索功能"""
        logger.info("开始测试: 搜索功能")

        search_input = self.page.get_by_placeholder("搜索...")
        expect(search_input).to_be_visible()
        search_input.fill("Morty")

        logger.info("搜索功能测试通过")

    @pytest.mark.P2
    def test_agent_pin_button(self):
        """PLAZA-007: 数字员工置顶按钮"""
        logger.info("开始测试: 数字员工置顶按钮")

        pin_btn = self.page.get_by_role("button", name="置顶")
        expect(pin_btn.first).to_be_visible()

        logger.info("置顶按钮可见")

    @pytest.mark.P1
    def test_click_agent_navigation(self):
        """PLAZA-008: 点击数字员工跳转"""
        logger.info("开始测试: 点击数字员工跳转")

        agent_link = self.page.get_by_role("link", name="生图2")
        expect(agent_link.first).to_be_visible()
        agent_link.first.click()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/agents/" in current_url, f"预期跳转到数字员工详情页，实际URL: {current_url}"

        logger.info("数字员工跳转测试通过")


class TestPlazaNavigation:
    """广场页面导航测试"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.plaza_page = PlazaPage(self.page)
        self.plaza_page.navigate()

    @pytest.mark.P0
    def test_nav_to_dashboard(self):
        """NAV-002: 导航到仪表盘"""
        logger.info("开始测试: 导航到仪表盘")

        self.plaza_page.navigate_to_dashboard()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/dashboard" in current_url, f"预期URL包含/dashboard，实际URL: {current_url}"

    @pytest.mark.P0
    def test_nav_to_new_agent(self):
        """NAV-003: 导航到新建数字员工"""
        logger.info("开始测试: 导航到新建数字员工")

        self.plaza_page.navigate_to_new_agent()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/agents/new" in current_url, f"预期URL包含/agents/new，实际URL: {current_url}"

    @pytest.mark.P1
    def test_nav_to_enterprise(self):
        """NAV-004: 导航到部门设置"""
        logger.info("开始测试: 导航到部门设置")

        self.plaza_page.navigate_to_enterprise()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/enterprise" in current_url, f"预期URL包含/enterprise，实际URL: {current_url}"

    @pytest.mark.P1
    def test_nav_to_settings(self):
        """NAV-005: 导航到公司设置"""
        logger.info("开始测试: 导航到公司设置")

        self.plaza_page.navigate_to_settings()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/admin/platform-settings" in current_url, \
            f"预期URL包含/admin/platform-settings，实际URL: {current_url}"


class TestGlobalFeatures:
    """全局功能测试"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.plaza_page = PlazaPage(self.page)
        self.plaza_page.navigate()

    @pytest.mark.P2
    def test_dark_mode_toggle(self):
        """GLOB-001: 深色模式切换"""
        logger.info("开始测试: 深色模式切换")

        self.plaza_page.toggle_dark_mode()
        logger.info("深色模式切换测试通过")

    @pytest.mark.P2
    def test_user_menu_display(self):
        """GLOB-004: 用户菜单显示"""
        logger.info("开始测试: 用户菜单显示")

        user_menu = self.page.locator('text="admin"')
        expect(user_menu.first).to_be_visible()

        role_text = self.page.locator('text="公司管理员"')
        expect(role_text.first).to_be_visible()

        logger.info("用户菜单显示正确：admin / 公司管理员")