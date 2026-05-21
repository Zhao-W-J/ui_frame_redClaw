import pytest
from playwright.sync_api import Page, expect
from pages.plaza_page import PlazaPage
from pages.agent_detail_page import AgentDetailPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestAgentDetailStatus:
    """数字员工详情页 - 状态标签"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        plaza_page = PlazaPage(self.page)
        plaza_page.navigate()

        agent_link = self.page.get_by_role("link", name="生图2")
        expect(agent_link.first).to_be_visible()
        agent_link.first.click()
        self.page.wait_for_load_state("networkidle")

        self.detail_page = AgentDetailPage(self.page)

    @pytest.mark.smoke
    @pytest.mark.P0
    def test_agent_detail_page_loads(self):
        """AGENT-001: 数字员工详情页加载"""
        logger.info("开始测试: 数字员工详情页加载")

        assert self.detail_page.is_on_detail_page(), "未进入数字员工详情页"

        heading = self.page.locator('h1')
        expect(heading).to_be_visible()

        logger.info("数字员工详情页加载测试通过")

    @pytest.mark.P0
    def test_status_tab_default(self):
        """AGENT-002: 默认显示状态标签"""
        logger.info("开始测试: 默认显示状态标签")

        status_tab = self.page.get_by_role("tab", name="状态")
        expect(status_tab).to_be_visible()

        aria_selected = status_tab.get_attribute("aria-selected")
        assert aria_selected == "true", f"预期状态标签默认选中，实际aria-selected={aria_selected}"

        logger.info("默认显示状态标签测试通过")

    @pytest.mark.P0
    def test_status_text_visible(self):
        """AGENT-003: 状态文本可见"""
        logger.info("开始测试: 状态文本可见")

        status_texts = self.page.locator('text="正在工作", text="待命中"')
        expect(status_texts.first).to_be_visible()
        status_text = status_texts.first.text_content().strip()
        assert status_text in ["正在工作", "待命中"], f"未知状态: {status_text}"

        logger.info(f"当前状态: {status_text}")

    @pytest.mark.P1
    def test_token_cards_visible(self):
        """AGENT-004: Token用量卡片可见"""
        logger.info("开始测试: Token用量卡片可见")

        today_token = self.page.locator('text="今日 Token"')
        expect(today_token.first).to_be_visible()

        month_token = self.page.locator('text="本月 Token"')
        expect(month_token.first).to_be_visible()

        logger.info("Token用量卡片可见")

    @pytest.mark.P1
    def test_llm_call_card_visible(self):
        """AGENT-005: LLM调用卡片可见"""
        logger.info("开始测试: LLM调用卡片可见")

        llm_text = self.page.locator('text="LLM 调用"')
        expect(llm_text.first).to_be_visible()

        logger.info("LLM调用卡片可见")

    @pytest.mark.P1
    def test_activity_card_visible(self):
        """AGENT-006: 24h活动卡片可见"""
        logger.info("开始测试: 24h活动卡片可见")

        activity_text = self.page.locator('text="24h 活动"')
        expect(activity_text.first).to_be_visible()

        logger.info("24h活动卡片可见")

    @pytest.mark.P1
    def test_chat_button_visible(self):
        """AGENT-007: 对话按钮可见"""
        logger.info("开始测试: 对话按钮可见")

        chat_btn = self.page.get_by_role("button", name="对话")
        expect(chat_btn).to_be_visible()

        logger.info("对话按钮可见")


class TestAgentDetailTabs:
    """数字员工详情页 - 标签页切换"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        plaza_page = PlazaPage(self.page)
        plaza_page.navigate()

        agent_link = self.page.get_by_role("link", name="生图2")
        expect(agent_link.first).to_be_visible()
        agent_link.first.click()
        self.page.wait_for_load_state("networkidle")

        self.detail_page = AgentDetailPage(self.page)

    @pytest.mark.P0
    def test_all_tabs_visible(self):
        """AGENT-008: 所有标签页可见"""
        logger.info("开始测试: 所有标签页可见")

        expected_tabs = ["状态", "自我意识", "心智", "工具", "技能",
                         "关系", "工作区", "聊天", "工作日志", "审批", "设置"]
        visible_tabs = self.detail_page.get_all_tab_names()
        logger.info(f"可见标签: {visible_tabs}")

        for tab in expected_tabs:
            assert tab in visible_tabs, f"标签 '{tab}' 不可见，可见标签: {visible_tabs}"

    @pytest.mark.P1
    def test_switch_to_aware_tab(self):
        """AGENT-009: 切换到自我意识标签"""
        logger.info("开始测试: 切换到自我意识标签")

        self.detail_page.click_tab("自我意识")

        aware_tab = self.page.get_by_role("tab", name="自我意识")
        expect(aware_tab).to_be_visible()
        assert aware_tab.get_attribute("aria-selected") == "true", "自我意识标签未选中"

        logger.info("自我意识标签切换成功")

    @pytest.mark.P1
    def test_switch_to_mind_tab(self):
        """AGENT-010: 切换到心智标签"""
        logger.info("开始测试: 切换到心智标签")

        self.detail_page.click_tab("心智")

        mind_tab = self.page.get_by_role("tab", name="心智")
        expect(mind_tab).to_be_visible()
        assert mind_tab.get_attribute("aria-selected") == "true", "心智标签未选中"

        logger.info("心智标签切换成功")

    @pytest.mark.P1
    def test_switch_to_tools_tab(self):
        """AGENT-011: 切换到工具标签"""
        logger.info("开始测试: 切换到工具标签")

        self.detail_page.click_tab("工具")

        tools_tab = self.page.get_by_role("tab", name="工具")
        expect(tools_tab).to_be_visible()
        assert tools_tab.get_attribute("aria-selected") == "true", "工具标签未选中"

        logger.info("工具标签切换成功")

    @pytest.mark.P1
    def test_switch_to_skills_tab(self):
        """AGENT-012: 切换到技能标签"""
        logger.info("开始测试: 切换到技能标签")

        self.detail_page.click_tab("技能")

        skills_tab = self.page.get_by_role("tab", name="技能")
        expect(skills_tab).to_be_visible()
        assert skills_tab.get_attribute("aria-selected") == "true", "技能标签未选中"

        logger.info("技能标签切换成功")

    @pytest.mark.P1
    def test_switch_to_workspace_tab(self):
        """AGENT-013: 切换到工作区标签"""
        logger.info("开始测试: 切换到工作区标签")

        self.detail_page.click_tab("工作区")

        ws_tab = self.page.get_by_role("tab", name="工作区")
        expect(ws_tab).to_be_visible()
        assert ws_tab.get_attribute("aria-selected") == "true", "工作区标签未选中"

        logger.info("工作区标签切换成功")

    @pytest.mark.P1
    def test_switch_to_chat_tab(self):
        """AGENT-014: 切换到聊天标签"""
        logger.info("开始测试: 切换到聊天标签")

        self.detail_page.click_tab("聊天")

        chat_tab = self.page.get_by_role("tab", name="聊天")
        expect(chat_tab).to_be_visible()
        assert chat_tab.get_attribute("aria-selected") == "true", "聊天标签未选中"

        logger.info("聊天标签切换成功")

    @pytest.mark.P1
    def test_switch_to_settings_tab(self):
        """AGENT-015: 切换到设置标签"""
        logger.info("开始测试: 切换到设置标签")

        self.detail_page.click_tab("设置")

        settings_tab = self.page.get_by_role("tab", name="设置")
        expect(settings_tab).to_be_visible()
        assert settings_tab.get_attribute("aria-selected") == "true", "设置标签未选中"

        logger.info("设置标签切换成功")


class TestAgentDetailChat:
    """数字员工详情页 - 聊天功能"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        plaza_page = PlazaPage(self.page)
        plaza_page.navigate()

        agent_link = self.page.get_by_role("link", name="生图2")
        expect(agent_link.first).to_be_visible()
        agent_link.first.click()
        self.page.wait_for_load_state("networkidle")

        self.detail_page = AgentDetailPage(self.page)

    @pytest.mark.P1
    def test_chat_tab_has_textarea(self):
        """AGENT-016: 聊天标签有输入框"""
        logger.info("开始测试: 聊天标签有输入框")

        self.detail_page.click_tab("聊天")

        textarea = self.page.locator('textarea, [contenteditable="true"]')
        expect(textarea.first).to_be_visible()

        logger.info("聊天输入框可见")

    @pytest.mark.P2
    def test_send_chat_message(self):
        """AGENT-017: 发送聊天消息"""
        logger.info("开始测试: 发送聊天消息")

        self.detail_page.click_tab("聊天")

        test_message = "你好，这是一条自动化测试消息"
        result = self.detail_page.send_chat_message(test_message)
        assert result, "发送聊天消息失败"

        logger.info("聊天消息发送成功")

    @pytest.mark.P2
    def test_new_session_button(self):
        """AGENT-018: 新建会话按钮"""
        logger.info("开始测试: 新建会话按钮")

        self.detail_page.click_tab("聊天")

        new_btn = self.page.get_by_role("button", name="新建会话")
        expect(new_btn).to_be_visible()

        logger.info("新建会话按钮可见")


class TestAgentDetailSettings:
    """数字员工详情页 - 设置功能"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        plaza_page = PlazaPage(self.page)
        plaza_page.navigate()

        agent_link = self.page.get_by_role("link", name="生图2")
        expect(agent_link.first).to_be_visible()
        agent_link.first.click()
        self.page.wait_for_load_state("networkidle")

        self.detail_page = AgentDetailPage(self.page)

    @pytest.mark.P1
    def test_settings_tab_loaded(self):
        """AGENT-019: 设置标签加载"""
        logger.info("开始测试: 设置标签加载")

        self.detail_page.click_tab("设置")

        settings_tab = self.page.get_by_role("tab", name="设置")
        expect(settings_tab).to_be_visible()
        assert settings_tab.get_attribute("aria-selected") == "true", "设置标签未选中"

        logger.info("设置标签加载成功")

    @pytest.mark.P2
    def test_agent_name_field_visible(self):
        """AGENT-020: 数字员工名称字段可见"""
        logger.info("开始测试: 数字员工名称字段可见")

        self.detail_page.click_tab("设置")

        name_input = self.page.locator('input[name="name"], input[placeholder*="名称"]')
        expect(name_input).to_be_visible()

        logger.info("数字员工名称字段可见")

    @pytest.mark.P2
    def test_delete_agent_button_visible(self):
        """AGENT-021: 删除数字员工按钮可见"""
        logger.info("开始测试: 删除数字员工按钮可见")

        self.detail_page.click_tab("设置")

        delete_btn = self.page.get_by_role("button", name="删除")
        expect(delete_btn).to_be_visible()

        logger.info("删除数字员工按钮可见")