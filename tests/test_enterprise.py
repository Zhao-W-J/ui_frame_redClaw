import pytest
from playwright.sync_api import Page, expect
from pages.enterprise_page import EnterprisePage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestEnterpriseDeptInfo:
    """部门设置 - 部门信息标签"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.enterprise_page = EnterprisePage(self.page)
        self.enterprise_page.navigate()

    @pytest.mark.smoke
    @pytest.mark.P1
    def test_enterprise_page_loads(self):
        """ENT-001: 进入部门设置"""
        logger.info("开始测试: 进入部门设置")

        assert self.enterprise_page.is_loaded(), "部门设置页面未正确加载"

        expect(self.page.get_by_role("heading", name="部门设置")).to_be_visible()

        logger.info("进入部门设置测试通过")

    @pytest.mark.P1
    def test_dept_info_tab_default(self):
        """ENT-002: 部门信息展示"""
        logger.info("开始测试: 部门信息展示")

        dept_info_tab = self.page.get_by_role("tab", name="部门信息")
        expect(dept_info_tab).to_be_visible()

        logger.info("部门信息标签可见")

    @pytest.mark.P1
    def test_dept_name_field_visible(self):
        """ENT-003: 部门名称字段可见"""
        logger.info("开始测试: 部门名称字段可见")

        name_input = self.page.locator('input[name="name"], input[placeholder*="部门名称"]')
        expect(name_input).to_be_visible()

        logger.info("部门名称输入框可见")

    @pytest.mark.P2
    def test_timezone_select_visible(self):
        """ENT-004: 时区选择可见"""
        logger.info("开始测试: 时区选择可见")

        tz_select = self.page.locator('select[name="timezone"], [role="combobox"]:near(:text("时区"))')
        expect(tz_select).to_be_visible()

        logger.info("时区选择可见")

    @pytest.mark.P2
    def test_theme_color_visible(self):
        """ENT-006: 主题色选择可见"""
        logger.info("开始测试: 主题色选择可见")

        color_elements = self.page.locator('[class*="color"], [class*="theme"]')
        assert color_elements.count() > 0, "未找到主题色选择元素"

        logger.info(f"主题色元素数量: {color_elements.count()}")

    @pytest.mark.P1
    def test_knowledge_base_visible(self):
        """ENT-007: 知识库区域可见"""
        logger.info("开始测试: 知识库区域可见")

        kb_text = self.page.locator('text="知识库"')
        expect(kb_text.first).to_be_visible()

        logger.info("知识库区域可见")

    @pytest.mark.P2
    def test_upload_button_visible(self):
        """ENT-008: 上传按钮可见"""
        logger.info("开始测试: 上传按钮可见")

        upload_btn = self.page.get_by_role("button", name="Upload")
        if upload_btn.count() > 0:
            expect(upload_btn).to_be_visible()
        else:
            upload_btn = self.page.get_by_role("button", name="上传")
            expect(upload_btn).to_be_visible()

        logger.info("上传按钮可见")

    @pytest.mark.P2
    def test_new_folder_button_visible(self):
        """ENT-009: 新建文件夹按钮可见"""
        logger.info("开始测试: 新建文件夹按钮可见")

        folder_btn = self.page.get_by_role("button", name="新建文件夹")
        expect(folder_btn).to_be_visible()

        logger.info("新建文件夹按钮可见")

    @pytest.mark.P2
    def test_broadcast_section_visible(self):
        """ENT-011: 广播通知区域可见"""
        logger.info("开始测试: 广播通知区域可见")

        broadcast_text = self.page.locator('text="广播"')
        expect(broadcast_text.first).to_be_visible()

        logger.info("广播通知区域可见")


class TestEnterpriseTabs:
    """部门设置 - 标签页切换"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.enterprise_page = EnterprisePage(self.page)
        self.enterprise_page.navigate()

    @pytest.mark.P1
    def test_all_tabs_visible(self):
        """ENT-ALL: 所有标签页可见"""
        logger.info("开始测试: 所有标签页可见")

        expected_tabs = ["部门信息", "模型池", "工具", "技能管理", "邀请码",
                         "配额", "用户", "组织管理", "审批", "审计日志"]
        visible_tabs = self.enterprise_page.get_all_tab_names()
        logger.info(f"可见标签: {visible_tabs}")

        for tab in expected_tabs:
            assert tab in visible_tabs, f"标签 '{tab}' 不可见，可见标签: {visible_tabs}"

    @pytest.mark.P1
    def test_switch_to_model_pool_tab(self):
        """ENT-012: 进入模型池标签"""
        logger.info("开始测试: 进入模型池标签")

        self.enterprise_page.click_tab("模型池")

        model_pool_tab = self.page.get_by_role("tab", name="模型池")
        expect(model_pool_tab).to_be_visible()
        assert model_pool_tab.get_attribute("aria-selected") == "true", "模型池标签未选中"

        logger.info("模型池标签切换成功")

    @pytest.mark.P1
    def test_switch_to_tools_tab(self):
        """ENT-013: 进入工具标签"""
        logger.info("开始测试: 进入工具标签")

        self.enterprise_page.click_tab("工具")

        tools_tab = self.page.get_by_role("tab", name="工具")
        expect(tools_tab).to_be_visible()
        assert tools_tab.get_attribute("aria-selected") == "true", "工具标签未选中"

        logger.info("工具标签切换成功")

    @pytest.mark.P1
    def test_switch_to_skills_tab(self):
        """ENT-014: 进入技能管理标签"""
        logger.info("开始测试: 进入技能管理标签")

        self.enterprise_page.click_tab("技能管理")

        skills_tab = self.page.get_by_role("tab", name="技能管理")
        expect(skills_tab).to_be_visible()
        assert skills_tab.get_attribute("aria-selected") == "true", "技能管理标签未选中"

        logger.info("技能管理标签切换成功")

    @pytest.mark.P1
    def test_switch_to_invitations_tab(self):
        """ENT-015: 进入邀请码标签"""
        logger.info("开始测试: 进入邀请码标签")

        self.enterprise_page.click_tab("邀请码")

        invitations_tab = self.page.get_by_role("tab", name="邀请码")
        expect(invitations_tab).to_be_visible()
        assert invitations_tab.get_attribute("aria-selected") == "true", "邀请码标签未选中"

        logger.info("邀请码标签切换成功")

    @pytest.mark.P1
    def test_switch_to_users_tab(self):
        """ENT-016: 进入用户标签"""
        logger.info("开始测试: 进入用户标签")

        self.enterprise_page.click_tab("用户")

        users_tab = self.page.get_by_role("tab", name="用户")
        expect(users_tab).to_be_visible()
        assert users_tab.get_attribute("aria-selected") == "true", "用户标签未选中"

        logger.info("用户标签切换成功")

    @pytest.mark.P1
    def test_switch_to_org_tab(self):
        """ENT-017: 进入组织管理标签"""
        logger.info("开始测试: 进入组织管理标签")

        self.enterprise_page.click_tab("组织管理")

        org_tab = self.page.get_by_role("tab", name="组织管理")
        expect(org_tab).to_be_visible()
        assert org_tab.get_attribute("aria-selected") == "true", "组织管理标签未选中"

        logger.info("组织管理标签切换成功")

    @pytest.mark.P2
    def test_switch_to_audit_tab(self):
        """ENT-018: 进入审计日志标签"""
        logger.info("开始测试: 进入审计日志标签")

        self.enterprise_page.click_tab("审计日志")

        audit_tab = self.page.get_by_role("tab", name="审计日志")
        expect(audit_tab).to_be_visible()
        assert audit_tab.get_attribute("aria-selected") == "true", "审计日志标签未选中"

        logger.info("审计日志标签切换成功")


class TestEnterpriseInvitations:
    """部门设置 - 邀请码管理"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.enterprise_page = EnterprisePage(self.page)
        self.enterprise_page.navigate()

    @pytest.mark.P1
    def test_invitation_list_visible(self):
        """INV-001: 邀请码列表展示"""
        logger.info("开始测试: 邀请码列表展示")

        self.enterprise_page.click_tab("邀请码")

        table = self.page.locator('table, [role="table"], [class*="table"]')
        expect(table.first).to_be_visible()

        logger.info("邀请码列表可见")

    @pytest.mark.P2
    def test_search_invitation(self):
        """INV-002: 搜索邀请码"""
        logger.info("开始测试: 搜索邀请码")

        self.enterprise_page.click_tab("邀请码")

        search_input = self.page.get_by_placeholder("搜索")
        expect(search_input).to_be_visible()
        search_input.fill("test")

        logger.info("搜索邀请码成功")

    @pytest.mark.P1
    def test_batch_create_button_visible(self):
        """INV-003: 批量创建按钮可见"""
        logger.info("开始测试: 批量创建按钮可见")

        self.enterprise_page.click_tab("邀请码")

        batch_btn = self.page.get_by_role("button", name="批量创建")
        expect(batch_btn).to_be_visible()

        logger.info("批量创建按钮可见")