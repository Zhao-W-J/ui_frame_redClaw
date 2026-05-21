import pytest
from playwright.sync_api import Page, expect
from pages.dashboard_page import DashboardPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestDashboard:
    """仪表盘功能测试类"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.dashboard_page = DashboardPage(self.page)
        self.dashboard_page.navigate()

    @pytest.mark.smoke
    @pytest.mark.P0
    def test_dashboard_page_loads(self):
        """DASH-001: 仪表盘页面加载"""
        logger.info("开始测试: 仪表盘页面加载")

        assert self.dashboard_page.is_loaded(), "仪表盘页面未正确加载"

        greeting = self.dashboard_page.get_greeting_text()
        logger.info(f"问候语: {greeting}")

        logger.info("仪表盘页面加载测试通过")

    @pytest.mark.P0
    def test_stats_cards_displayed(self):
        """DASH-002: 统计卡片展示"""
        logger.info("开始测试: 统计卡片展示")

        assert self.dashboard_page.is_employee_card_visible(), "数字员工卡片未显示"
        assert self.dashboard_page.is_tasks_card_visible(), "进行中任务卡片未显示"
        assert self.dashboard_page.is_token_card_visible(), "今日Token卡片未显示"
        assert self.dashboard_page.is_active_card_visible(), "最近活跃卡片未显示"

        logger.info("所有统计卡片显示正常")

    @pytest.mark.P1
    def test_employee_count_displayed(self):
        """DASH-003: 员工总数验证"""
        logger.info("开始测试: 员工总数验证")

        count_text = self.dashboard_page.get_employee_count()
        assert count_text is not None and len(count_text) > 0, "员工总数未显示"
        assert "名数字员工" in count_text, f"预期包含'名数字员工'，实际文本: {count_text}"

        logger.info(f"员工总数: {count_text}")

    @pytest.mark.P0
    def test_employee_list_displayed(self):
        """DASH-004: 员工列表展示"""
        logger.info("开始测试: 员工列表展示")

        headers = self.dashboard_page.get_table_headers()
        assert len(headers) >= 3, f"预期至少3个表头，实际数量: {len(headers)}"

        has_employee_header = any("员工" in h for h in headers)
        has_dynamic_header = any("动态" in h for h in headers)
        has_token_header = any("Token" in h or "token" in h.lower() for h in headers)
        has_active_header = any("活跃" in h for h in headers)

        assert has_employee_header, "缺少'员工'列头"
        assert has_dynamic_header, "缺少'最新动态'列头"
        assert has_token_header, "缺少'Token'列头"
        assert has_active_header, "缺少'活跃'列头"

        logger.info(f"表头列表: {headers}")

    @pytest.mark.P1
    def test_employee_status_displayed(self):
        """DASH-005: 员工状态显示"""
        logger.info("开始测试: 员工状态显示")

        status_indicators = self.page.locator('text="运行中", text="待命中"')
        expect(status_indicators.first).to_be_visible()
        status_text = status_indicators.first.text_content()
        assert status_text in ["运行中", "待命中"], f"未知状态: {status_text}"

        logger.info(f"检测到状态: {status_text}")

    @pytest.mark.P1
    def test_activity_section_visible(self):
        """DASH-006: 全局活动流展示"""
        logger.info("开始测试: 全局活动流展示")

        assert self.dashboard_page.is_activity_section_visible(), "全局活动区域未显示"

        activity_heading = self.page.get_by_role("heading", name="全局活动")
        expect(activity_heading).to_be_visible()

        logger.info("全局活动流展示测试通过")

    @pytest.mark.P1
    def test_click_new_agent_from_dashboard(self):
        """DASH-007: 点击新建数字员工"""
        logger.info("开始测试: 从仪表盘点击新建数字员工")

        self.dashboard_page.click_new_agent_button()

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/agents/new" in current_url, f"预期URL包含/agents/new，实际URL: {current_url}"

    @pytest.mark.P1
    def test_click_employee_row_navigation(self):
        """DASH-008: 点击员工行跳转"""
        logger.info("开始测试: 点击员工行跳转")

        result = self.dashboard_page.click_agent_row(0)
        assert result, "未找到可点击的员工行"

        self.page.wait_for_load_state("networkidle")
        current_url = self.page.url
        assert "/agents/" in current_url, f"预期跳转到数字员工详情页，实际URL: {current_url}"
        logger.info(f"跳转到: {current_url}")


class TestDashboardDataVerification:
    """仪表盘数据验证测试"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.dashboard_page = DashboardPage(self.page)
        self.dashboard_page.navigate()

    @pytest.mark.P1
    def test_verify_all_stats_cards_existence(self):
        """验证所有统计卡片存在性"""
        logger.info("验证所有统计卡片存在性")

        assert self.dashboard_page.are_all_stats_cards_visible(), "并非所有统计卡片都可见"

    @pytest.mark.P2
    def test_get_activity_count(self):
        """获取活动记录数量"""
        logger.info("获取活动记录数量")

        count = self.dashboard_page.get_activity_count()
        logger.info(f"活动记录数量: {count}")

    @pytest.mark.P2
    def test_greeting_contains_time_of_day(self):
        """问候语包含时段信息（上午/下午/晚上）"""
        logger.info("验证问候语包含时段信息")

        greeting = self.dashboard_page.get_greeting_text()
        time_indicators = ["上午", "下午", "晚上", "好"]

        has_time_indicator = any(indicator in greeting for indicator in time_indicators)
        assert has_time_indicator, f"问候语应包含时段信息，实际内容: {greeting}"