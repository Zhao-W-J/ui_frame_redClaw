from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class CreateAgentPage(BasePage):
    """数字员工创建页面对象 - 5步向导"""

    # 页面元素定位器
    PAGE_HEADING = 'h1:has-text("新建数字员工")'
    
    # 步骤指示器
    STEP_1_INDICATOR = ':text("1") >> text="基本信息"'
    STEP_2_INDICATOR = ':text("2") >> text="人格设定"'
    STEP_3_INDICATOR = ':text("3") >> text="技能配置"'
    STEP_4_INDICATOR = ':text("4") >> text="权限设置"'
    STEP_5_INDICATOR = ':text("5") >> text="通道绑定"'

    # 创建类型选择
    TYPE_HOSTED = 'text="平台托管"'
    TYPE_LAB = 'text="Lab"'

    # ===== 步骤1: 基础信息与模型选择 =====
    STEP1_HEADING = 'h3:has-text("基础信息与模型选择")'
    NAME_INPUT = 'input[placeholder*="小智"]'
    ROLE_INPUT = 'input[placeholder*="角色定位"]'
    MODEL_RADIO = 'input[type="radio"][value*="Qwen"], label:has-text("Qwen3.5")'
    DAILY_TOKEN_INPUT = 'input[type="number"]:first-of-type, input[aria-label*="每日"]'
    MONTHLY_TOKEN_INPUT = 'input[type="number"]:last-of-type, input[aria-label*="每月"]'
    NEXT_BUTTON = 'button:has-text("下一步 →")'
    PREV_BUTTON = 'button:has-text("上一步")'
    CANCEL_BUTTON = 'button:has-text("取消")'
    JSON_IMPORT_LINK = 'text="↑ 从 JSON 导入"'
    
    # 模板选择
    TEMPLATE_CUSTOM = 'text="自定义"'
    TEMPLATE_PM = 'text="PM"'
    TEMPLATE_DS = 'text="DS"'
    TEMPLATE_PI = 'text="PI"'
    TEMPLATE_MR = 'text="MR"'

    # ===== 步骤2: 人格与边界 =====
    STEP2_HEADING = 'h3:has-text("人格与边界")'
    PERSONALITY_TEXTAREA = 'textarea[placeholder*="认真负责"]'
    BOUNDARY_TEXTAREA = 'textarea[placeholder*="不可修改"]'

    # ===== 步骤3: 技能配置 =====
    STEP3_HEADING = 'h3:has-text("技能配置")'
    SKILL_COMPETITIVE_ANALYSIS = 'label:has-text("Competitive Analysis"), [role=checkbox]:near(:text("Competitive Analysis"))'
    SKILL_COMPLEX_TASK = 'label:has-text("Complex Task Executor"), [role=checkbox]:near(:text("Complex Task Executor"))'
    SKILL_CONTENT_RESEARCH = 'label:has-text("Content Research Writer"), [role=checkbox]:near(:text("Content Research Writer"))'
    SKILL_CONTENT_WRITING = 'label:has-text("Content Writing"), [role=checkbox]:near(:text("Content Writing"))'
    SKILL_DATA_ANALYSIS = 'label:has-text("Data Analysis"), [role=checkbox]:near(:text("Data Analysis"))'
    SKILL_MCP_INSTALLER = 'label:has-text("MCP Tool Installer"), [role=checkbox]:near(:text("MCP Tool Installer"))'
    SKILL_MEETING_NOTES = 'label:has-text("Meeting Notes"), [role=checkbox]:near(:text("Meeting Notes"))'
    SKILL_SKILL_CREATOR = 'label:has-text("Skill Creator"), [role=checkbox]:near(:text("Skill Creator"))'
    SKILL_WEB_RESEARCH = 'label:has-text("Web Research"), [role=checkbox]:near(:text("Web Research"))'

    # ===== 步骤4: 权限设置 =====
    STEP4_HEADING = 'h3:has-text("权限设置")'
    VISIBILITY_ALL = 'label:has-text("全部门可见"), [role=radio]:near(:text("全部门可见"))'
    VISIBILITY_SELF = 'label:has-text("仅自己"), [role=radio]:near(:text("仅自己"))'
    ACCESS_USE = 'label:has-text("使用"), [role=radio]:near(:text("使用")):not(:near(:text("全部门")))'
    ACCESS_MANAGE = 'label:has-text("管理"), [role=radio]:near(:text("管理")):not(:near(:text("完全访问")))' if False else '[role=radio]:near(:text("管理"):not(:text("使用")))'

    # ===== 步骤5: 渠道配置 =====
    STEP5_HEADING = 'h3:has-text("渠道配置")'
    CHANNEL_SLACK = 'img[alt*="Slack"], img:has-text("Slack")'
    CHANNEL_DISCORD = 'img[alt*="Discord"]'
    CHANNEL_TEAMS = 'img[alt*="Teams"]'
    CHANNEL_FEISHU = 'img[alt*="Feishu"], img[alt*="飞书"]'
    CHANNEL_WECOM = 'img[alt*="WeCom"], img[alt*="企业微信"]'
    CHANNEL_DINGTALK = 'img[alt*="DingTalk"], img[alt*="钉钉"]'
    CHANNEL_ATLASSIAN = 'img[alt*="Atlassian"]'
    COMPLETE_BUTTON = 'button:has-text("完成创建")'

    page_loaded_indicator = PAGE_HEADING

    def __init__(self, page: Page):
        """
        初始化数字员工创建页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = f"{self.base_url}/agents/new"
        self.current_step = 1

    def navigate(self) -> None:
        """导航到新建数字员工页面"""
        logger.info(f"导航到新建数字员工页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()
        self.current_step = 1

    def is_loaded(self) -> bool:
        """检查页面是否加载完成"""
        return self.is_element_visible(self.PAGE_HEADING)

    def is_on_step(self, step_num: int) -> bool:
        """检查当前是否在指定步骤
        
        Args:
            step_num: 步骤号 (1-5)
        """
        step_indicators = {
            1: self.STEP1_HEADING,
            2: self.STEP2_HEADING,
            3: self.STEP3_HEADING,
            4: self.STEP4_HEADING,
            5: self.STEP5_HEADING
        }
        return self.is_element_visible(step_indicators.get(step_num, ""))

    # ===== 步骤1操作方法 =====
    
    def fill_name(self, name: str):
        """填写名称"""
        logger.info(f"填写数字员工名称: {name}")
        name_input = self.page.get_by_placeholder("例：小智")
        name_input.fill(name)

    def fill_role(self, role: str):
        """填写角色描述"""
        logger.info(f"填写角色描述: {role}")
        role_input = self.page.get_by_placeholder("描述它的角色定位")
        role_input.fill(role)

    def select_model(self, model_name: str = "Qwen3.5-122B-A10B-FP8"):
        """选择主模型"""
        logger.info(f"选择主模型: {model_name}")
        radio = self.page.get_by_role("radio", name=model_name)
        if radio.count() > 0:
            radio.click()
        else:
            radio = self.page.locator('label:has-text("{}")'.format(model_name))
            if radio.count() > 0:
                radio.click()

    def set_daily_token_limit(self, limit: int | str):
        """设置每日Token上限"""
        logger.info(f"设置每日Token上限: {limit}")
        spinbuttons = self.page.get_by_role("spinbutton")
        if spinbuttons.count() >= 1:
            spinbuttons.first.fill(str(limit))

    def set_monthly_token_limit(self, limit: int | str):
        """设置每月Token上限"""
        logger.info(f"设置每月Token上限: {limit}")
        spinbuttons = self.page.get_by_role("spinbutton")
        if spinbuttons.count() >= 2:
            spinbuttons.last.fill(str(limit))

    def click_next(self):
        """点击下一步按钮"""
        logger.info("点击下一步按钮")
        next_btn = self.page.get_by_role("button", name="下一步 →")
        next_btn.click()
        self.current_step = min(5, self.current_step + 1)

    def click_prev(self):
        """点击上一步按钮"""
        logger.info("点击上一步按钮")
        prev_btn = self.page.get_by_role("button", name="上一步")
        prev_btn.click()
        self.current_step = max(1, self.current_step - 1)

    def click_cancel(self):
        """点击取消按钮"""
        logger.info("点击取消按钮")
        cancel_btn = self.page.get_by_role("button", name="取消")
        cancel_btn.click()

    def click_json_import(self):
        """点击从JSON导入链接"""
        logger.info("点击从JSON导入")
        import_link = self.page.get_text("↑ 从 JSON 导入")
        if not import_link:
            import_link = self.page.locator(self.JSON_IMPORT_LINK)
        if import_link.count() > 0:
            import_link.click()

    def select_template(self, template_name: str):
        """选择模板
        
        Args:
            template_name: 模板名称 (PM/DS/PI/MR/自定义)
        """
        logger.info(f"选择模板: {template_name}")
        template_map = {
            "PM": "项目经理",
            "DS": "设计师",
            "PI": "产品实习生",
            "MR": "市场研究员",
            "自定义": "自定义"
        }
        
        display_name = template_map.get(template_name, template_name)
        template_el = self.page.locator(f'text="{display_name}"').first
        if template_el.count() > 0:
            template_el.click()

    def switch_to_lab_type(self):
        """切换到Lab类型（OpenClaw）"""
        logger.info("切换到Lab类型")
        lab_el = self.page.locator(self.TYPE_LAB)
        if lab_el.count() > 0:
            lab_el.click()

    # ===== 步骤2操作方法 =====
    
    def fill_personality(self, personality: str):
        """填写人格设定"""
        logger.info(f"填写人格设定: {personality[:50]}...")
        textarea = self.page.get_by_placeholder("认真负责、数据驱动、主动汇报...")
        textarea.fill(personality)

    def fill_boundary(self, boundary: str):
        """填写行为边界"""
        logger.info(f"填写行为边界: {boundary[:50]}...")
        textarea = self.page.get_by_placeholder("不可修改财务数据、对外沟通需经审批...")
        textarea.fill(boundary)

    # ===== 步骤3操作方法 =====
    
    def toggle_skill(self, skill_name: str, checked: bool = True):
        """勾选或取消技能
        
        Args:
            skill_name: 技能名称
            checked: 是否勾选
        """
        logger.info(f"设置技能 {skill_name}: {'勾选' if checked else '取消'}")
        skill_map = {
            "Competitive Analysis": self.SKILL_COMPETITIVE_ANALYSIS,
            "Complex Task Executor": self.SKILL_COMPLEX_TASK,
            "Content Research Writer": self.SKILL_CONTENT_RESEARCH,
            "Content Writing": self.SKILL_CONTENT_WRITING,
            "Data Analysis": self.SKILL_DATA_ANALYSIS,
            "MCP Tool Installer": self.SKILL_MCP_INSTALLER,
            "Meeting Notes": self.SKILL_MEETING_NOTES,
            "Skill Creator": self.SKILL_SKILL_CREATOR,
            "Web Research": self.SKILL_WEB_RESEARCH
        }
        
        selector = skill_map.get(skill_name, "")
        if selector:
            checkbox = self.page.locator(selector).first
            if checkbox.count() > 0 and checkbox.is_enabled():
                current_state = checkbox.is_checked()
                if current_state != checked:
                    checkbox.check() if checked else checkbox.uncheck()

    def get_required_skills_count(self) -> int:
        """获取必填技能数量（应为3个）"""
        required_skills = [
            self.SKILL_COMPLEX_TASK,
            self.SKILL_MCP_INSTALLER,
            self.SKILL_SKILL_CREATOR
        ]
        count = 0
        for selector in required_skills:
            el = self.page.locator(selector)
            if el.count() > 0:
                count += 1
        return count

    # ===== 步骤4操作方法 =====
    
    def set_visibility_all(self):
        """设置为全部门可见"""
        logger.info("设置为全部门可见")
        radio = self.page.get_by_role("radio", name="全部门可见")
        if radio.count() > 0:
            radio.click()

    def set_visibility_self(self):
        """设置为仅自己可见"""
        logger.info("设置为仅自己可见")
        radio = self.page.get_by_role("radio", name="仅自己")
        if radio.count() > 0:
            radio.click()

    def set_access_use(self):
        """设置使用权限"""
        logger.info("设置使用权限")
        radio = self.page.get_by_role("radio", name="使用").first
        if radio.count() > 0:
            radio.click()

    def set_access_manage(self):
        """设置管理权限"""
        logger.info("设置管理权限")
        radios = self.page.get_by_role("radio", name="管理")
        for i in range(radios.count()):
            radio = radios.nth(i)
            text = radio.text_content() or ""
            if "完全访问" in text or "设置、心智" in text:
                radio.click()
                break

    # ===== 步骤5操作方法 =====
    
    def get_channel_list(self) -> list:
        """获取可用渠道列表"""
        channels = []
        channel_names = ["Slack", "Discord", "Teams", "Feishu", "WeCom", "DingTalk", "Atlassian"]
        for name in channel_names:
            img = self.page.get_by_role("img", name=name)
            if img.count() > 0:
                channels.append(name)
        return channels

    def click_complete(self):
        """点击完成创建按钮"""
        logger.info("点击完成创建按钮")
        complete_btn = self.page.get_by_role("button", name="完成创建")
        complete_btn.click()

    # ===== 完整流程方法 =====
    
    def create_agent_basic(
        self,
        name: str,
        role: str = "测试角色",
        personality: str = "认真负责",
        boundary: str = "不可修改数据",
        visibility: str = "all",
        access_level: str = "use"
    ):
        """
        完整的创建流程（简化版）
        
        Args:
            name: 数字员工名称
            role: 角色描述
            personality: 人格设定
            boundary: 行为边界
            visibility: 可见性 (all/self)
            access_level: 访问级别 (use/manage)
        """
        logger.info(f"开始创建数字员工: {name}")

        # 步骤1: 基础信息
        self.fill_name(name)
        self.fill_role(role)
        self.select_model()
        self.click_next()

        # 步骤2: 人格设定
        self.fill_personality(personality)
        self.fill_boundary(boundary)
        self.click_next()

        # 步骤3: 技能配置（跳过，使用默认）
        self.click_next()

        # 步骤4: 权限设置
        if visibility == "self":
            self.set_visibility_self()
        else:
            self.set_visibility_all()
            
        if access_level == "manage":
            self.set_access_manage()
        else:
            self.set_access_use()
            
        self.click_next()

        # 步骤5: 渠道配置（跳过）
        self.click_complete()

        logger.info(f"数字员工创建完成: {name}")
