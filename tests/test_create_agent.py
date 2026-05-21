import pytest
from playwright.sync_api import Page, expect
from pages.create_agent_page import CreateAgentPage
from utils.logger import get_logger

logger = get_logger(__name__)


class TestCreateAgentStep1:
    """步骤1: 基础信息与模型选择"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        self.create_page = CreateAgentPage(self.page)
        self.create_page.navigate()

    @pytest.mark.smoke
    @pytest.mark.P0
    def test_create_agent_page_loads(self):
        """CREATE-001: 新建数字员工页面加载"""
        logger.info("开始测试: 新建数字员工页面加载")

        assert self.create_page.is_loaded(), "新建数字员工页面未正确加载"

        expect(self.page.get_by_role("heading", name="新建数字员工")).to_be_visible()

        logger.info("新建数字员工页面加载测试通过")

    @pytest.mark.P0
    def test_step1_basic_info_fields_visible(self):
        """CREATE-002: 步骤1基础字段可见性"""
        logger.info("开始测试: 步骤1基础字段可见性")

        assert self.create_page.is_on_step(1), "当前不在步骤1"

        name_input = self.page.get_by_placeholder("例：小智")
        expect(name_input).to_be_visible()

        role_input = self.page.get_by_placeholder("描述它的角色定位")
        expect(role_input).to_be_visible()

        model_radio = self.page.get_by_role("radio", name="Qwen3.5-122B-A10B-FP8")
        expect(model_radio.first).to_be_visible()

        logger.info("步骤1基础字段可见性测试通过")

    @pytest.mark.P1
    def test_fill_name_field(self):
        """CREATE-003: 填写名称字段"""
        logger.info("开始测试: 填写名称字段")

        test_name = "自动化测试_001"
        self.create_page.fill_name(test_name)

        name_input = self.page.get_by_placeholder("例：小智")
        actual_value = name_input.input_value()
        assert actual_value == test_name, f"预期名称为 {test_name}，实际值: {actual_value}"

        logger.info("填写名称字段测试通过")

    @pytest.mark.P1
    def test_fill_role_field(self):
        """CREATE-004: 填写角色描述字段"""
        logger.info("开始测试: 填写角色描述字段")

        test_role = "自动化测试角色"
        self.create_page.fill_role(test_role)

        role_input = self.page.get_by_placeholder("描述它的角色定位")
        actual_value = role_input.input_value()
        assert actual_value == test_role, f"预期角色为 {test_role}，实际值: {actual_value}"

        logger.info("填写角色描述字段测试通过")

    @pytest.mark.P0
    def test_select_model(self):
        """CREATE-005: 选择主模型"""
        logger.info("开始测试: 选择主模型")

        self.create_page.select_model("Qwen3.5-122B-A10B-FP8")

        model_radio = self.page.get_by_role("radio", name="Qwen3.5-122B-A10B-FP8", checked=True)
        expect(model_radio.first).to_be_checked()

        logger.info("模型选择成功")

    @pytest.mark.P2
    def test_token_limit_inputs_visible(self):
        """CREATE-006: Token限制输入框可见"""
        logger.info("开始测试: Token限制输入框可见")

        spinbuttons = self.page.get_by_role("spinbutton")
        assert spinbuttons.count() >= 2, f"预期至少2个Token输入框，实际数量: {spinbuttons.count()}"

        logger.info(f"Token输入框数量: {spinbuttons.count()}")

    @pytest.mark.P1
    def test_set_daily_token_limit(self):
        """CREATE-007: 设置每日Token上限"""
        logger.info("开始测试: 设置每日Token上限")

        daily_limit = 1000000
        self.create_page.set_daily_token_limit(daily_limit)

        spinbuttons = self.page.get_by_role("spinbutton")
        expect(spinbuttons.first).to_be_visible()
        actual_value = spinbuttons.first.input_value()
        assert str(daily_limit) in actual_value or actual_value == str(daily_limit), \
            f"预期每日Token为 {daily_limit}，实际值: {actual_value}"

    @pytest.mark.P1
    def test_set_monthly_token_limit(self):
        """CREATE-008: 设置每月Token上限"""
        logger.info("开始测试: 设置每月Token上限")

        monthly_limit = 30000000
        self.create_page.set_monthly_token_limit(monthly_limit)

        spinbuttons = self.page.get_by_role("spinbutton")
        expect(spinbuttons.last).to_be_visible()
        actual_value = spinbuttons.last.input_value()
        assert str(monthly_limit) in actual_value or actual_value == str(monthly_limit), \
            f"预期每月Token为 {monthly_limit}，实际值: {actual_value}"


class TestCreateAgentStep2:
    """步骤2: 人格与边界"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        create_page = CreateAgentPage(self.page)
        create_page.navigate()

        create_page.fill_name("自动化测试_001")
        create_page.fill_role("测试角色")
        create_page.select_model()
        create_page.click_next()

        self.create_page = create_page

    @pytest.mark.P0
    def test_step2_loaded(self):
        """CREATE-009: 步骤2加载验证"""
        logger.info("开始测试: 步骤2加载验证")

        assert self.create_page.is_on_step(2), "当前未在步骤2"

    @pytest.mark.P1
    def test_personality_textarea_visible(self):
        """CREATE-010: 人格设定文本框可见"""
        logger.info("开始测试: 人格设定文本框可见")

        textarea = self.page.get_by_placeholder("认真负责、数据驱动、主动汇报...")
        expect(textarea).to_be_visible()

    @pytest.mark.P1
    def test_boundary_textarea_visible(self):
        """CREATE-011: 行为边界文本框可见"""
        logger.info("开始测试: 行为边界文本框可见")

        textarea = self.page.get_by_placeholder("不可修改财务数据、对外沟通需经审批...")
        expect(textarea).to_be_visible()

    @pytest.mark.P1
    def test_fill_personality(self):
        """CREATE-012: 填写人格设定"""
        logger.info("开始测试: 填写人格设定")

        personality = "认真负责、数据驱动、主动汇报工作进展"
        self.create_page.fill_personality(personality)

        textarea = self.page.get_by_placeholder("认真负责、数据驱动、主动汇报...")
        actual_value = textarea.input_value()
        assert actual_value == personality, f"预期人格设定为 {personality[:30]}...，实际值: {actual_value[:30]}..."

    @pytest.mark.P1
    def test_fill_boundary(self):
        """CREATE-013: 填写行为边界"""
        logger.info("开始测试: 填写行为边界")

        boundary = "不可修改财务数据、对外沟通需经审批"
        self.create_page.fill_boundary(boundary)

        textarea = self.page.get_by_placeholder("不可修改财务数据、对外沟通需经审批...")
        actual_value = textarea.input_value()
        assert actual_value == boundary, f"预期行为边界为 {boundary[:30]}...，实际值: {actual_value[:30]}..."


class TestCreateAgentStep3:
    """步骤3: 技能配置"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        create_page = CreateAgentPage(self.page)
        create_page.navigate()

        create_page.fill_name("自动化测试_001")
        create_page.fill_role("测试角色")
        create_page.select_model()
        create_page.click_next()

        create_page.fill_personality("认真负责")
        create_page.fill_boundary("不可修改数据")
        create_page.click_next()

        self.create_page = create_page

    @pytest.mark.P0
    def test_step3_loaded(self):
        """CREATE-014: 步骤3加载验证"""
        logger.info("开始测试: 步骤3加载验证")

        assert self.create_page.is_on_step(3), "当前未在步骤3"

    @pytest.mark.P1
    def test_required_skills_displayed(self):
        """CREATE-015: 必填技能显示（3个）"""
        logger.info("开始测试: 必填技能显示")

        required_count = self.create_page.get_required_skills_count()
        assert required_count >= 3, f"预期至少3个必填技能，实际数量: {required_count}"

    @pytest.mark.P2
    def test_toggle_skill(self):
        """CREATE-016: 切换技能勾选状态"""
        logger.info("开始测试: 切换技能勾选状态")

        skill_name = "Data Analysis"
        self.create_page.toggle_skill(skill_name, checked=True)


class TestCreateAgentStep4:
    """步骤4: 权限设置"""

    @pytest.fixture(autouse=True)
    def setup(self, logged_in_page: Page):
        self.page = logged_in_page
        create_page = CreateAgentPage(self.page)
        create_page.navigate()

        create_page.fill_name("自动化测试_001")
        create_page.fill_role("测试角色")
        create_page.select_model()
        create_page.click_next()

        create_page.fill_personality("认真负责")
        create_page.fill_boundary("不可修改数据")
        create_page.click_next()

        create_page.click_next()

        self.create_page = create_page

    @pytest.mark.P0
    def test_step4_loaded(self):
        """CREATE-017: 步骤4加载验证"""
        logger.info("开始测试: 步骤4加载验证")

        assert self.create_page.is_on_step(4), "当前未在步骤4"

    @pytest.mark.P1
    def test_visibility_options_visible(self):
        """CREATE-018: 可见范围选项可见"""
        logger.info("开始测试: 可见范围选项可见")

        radio_all = self.page.get_by_role("radio", name="全部门可见")
        radio_self = self.page.get_by_role("radio", name="仅自己")

        expect(radio_all).to_be_visible()
        expect(radio_self).to_be_visible()