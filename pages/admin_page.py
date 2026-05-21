from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class AdminPage(BasePage):
    """公司管理页面对象 - 包含5个标签页"""

    PAGE_HEADING = 'h1:has-text("公司设置")'

    TAB_DASHBOARD = 'button:has-text("公司仪表盘"), a:has-text("公司仪表盘")'
    TAB_SETTINGS = 'button:has-text("公司设置"), a:has-text("公司设置")'
    TAB_DEPT_MGMT = 'button:has-text("部门管理"), a:has-text("部门管理")'
    TAB_MODEL_POOL = 'button:has-text("公司模型池"), a:has-text("公司模型池")'
    TAB_SKILLS = 'button:has-text("技能管理"), a:has-text("技能管理")'

    LAST_7_DAYS_BUTTON = 'button:has-text("Last 7 Days")'
    LAST_30_DAYS_BUTTON = 'button:has-text("Last 30 Days")'

    ANNOUNCEMENT_TOGGLE = '[role="switch"]:near(:text("公告栏"))'
    ANNOUNCEMENT_INPUT = 'textarea[placeholder*="公告"], input[placeholder*="公告"]'

    SMTP_HOST_INPUT = 'input[placeholder*="SMTP"], input[name*="smtp_host"]'
    SMTP_PORT_INPUT = 'input[placeholder*="端口"], input[name*="smtp_port"]'
    SMTP_USER_INPUT = 'input[placeholder*="用户名"], input[name*="smtp_user"]'
    SMTP_PASS_INPUT = 'input[placeholder*="密码"], input[name*="smtp_pass"]'
    TEST_EMAIL_BUTTON = 'button:has-text("测试发送")'

    CREATE_DEPT_BUTTON = 'button:has-text("创建部门")'
    DEPT_NAME_INPUT = 'input[name="name"], input[placeholder*="部门名称"]'

    SAVE_BUTTON = 'button:has-text("保存")'

    page_loaded_indicator = PAGE_HEADING

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = f"{self.base_url}/admin/platform-settings"

    def navigate(self) -> None:
        logger.info(f"导航到公司管理页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()

    def is_loaded(self) -> bool:
        return self.is_element_visible(self.PAGE_HEADING)

    def click_tab(self, tab_name: str):
        logger.info(f"点击公司管理标签: {tab_name}")
        tab = self.page.get_by_role("tab", name=tab_name)
        if tab.count() > 0:
            tab.click()
        else:
            tab_btn = self.page.locator(f'button:has-text("{tab_name}"), a:has-text("{tab_name}")')
            if tab_btn.count() > 0:
                tab_btn.first.click()
        self.page.wait_for_timeout(500)

    def click_last_7_days(self):
        logger.info("点击Last 7 Days")
        btn = self.page.locator(self.LAST_7_DAYS_BUTTON)
        if btn.count() > 0:
            btn.click()
            return True
        return False

    def click_last_30_days(self):
        logger.info("点击Last 30 Days")
        btn = self.page.locator(self.LAST_30_DAYS_BUTTON)
        if btn.count() > 0:
            btn.click()
            return True
        return False

    def is_dashboard_visible(self) -> bool:
        charts = self.page.locator('canvas, [class*="chart"], [class*="Chart"]')
        return charts.count() > 0

    def toggle_announcement(self):
        logger.info("切换公告栏开关")
        toggle = self.page.locator(self.ANNOUNCEMENT_TOGGLE)
        if toggle.count() > 0:
            toggle.click()
            return True
        return False

    def set_announcement_text(self, text: str):
        logger.info(f"设置公告文本: {text}")
        ann_input = self.page.locator(self.ANNOUNCEMENT_INPUT)
        if ann_input.count() > 0:
            ann_input.fill(text)
            return True
        return False

    def configure_smtp(self, host: str, port: str, username: str, password: str):
        logger.info(f"配置SMTP: {host}:{port}")
        host_input = self.page.locator(self.SMTP_HOST_INPUT)
        if host_input.count() > 0:
            host_input.fill(host)
        port_input = self.page.locator(self.SMTP_PORT_INPUT)
        if port_input.count() > 0:
            port_input.fill(port)
        user_input = self.page.locator(self.SMTP_USER_INPUT)
        if user_input.count() > 0:
            user_input.fill(username)
        pass_input = self.page.locator(self.SMTP_PASS_INPUT)
        if pass_input.count() > 0:
            pass_input.fill(password)
        return True

    def click_test_email(self):
        logger.info("点击测试邮件发送")
        test_btn = self.page.locator(self.TEST_EMAIL_BUTTON)
        if test_btn.count() > 0:
            test_btn.click()
            return True
        return False

    def click_create_department(self):
        logger.info("点击创建部门")
        create_btn = self.page.locator(self.CREATE_DEPT_BUTTON)
        if create_btn.count() > 0:
            create_btn.click()
            return True
        return False

    def set_department_name(self, name: str):
        logger.info(f"设置部门名称: {name}")
        name_input = self.page.locator(self.DEPT_NAME_INPUT)
        if name_input.count() > 0:
            name_input.fill(name)
            return True
        return False

    def click_save(self):
        logger.info("点击保存按钮")
        save_btn = self.page.get_by_role("button", name="保存")
        if save_btn.count() > 0:
            save_btn.click()
            return True
        return False

    def is_dashboard_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_DASHBOARD)

    def is_settings_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_SETTINGS)

    def is_dept_mgmt_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_DEPT_MGMT)

    def is_model_pool_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_MODEL_POOL)

    def is_skills_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_SKILLS)

    def get_all_tab_names(self) -> list:
        tabs = ["公司仪表盘", "公司设置", "部门管理", "公司模型池", "技能管理"]
        visible_tabs = []
        for tab in tabs:
            tab_el = self.page.get_by_role("tab", name=tab)
            if tab_el.count() > 0:
                visible_tabs.append(tab)
            else:
                btn = self.page.locator(f'button:has-text("{tab}"), a:has-text("{tab}")')
                if btn.count() > 0:
                    visible_tabs.append(tab)
        return visible_tabs

    def get_dashboard_metrics(self) -> list:
        metrics = []
        metric_texts = ["Avg Tokens", "Retention", "Companies", "Users", "Token Usage"]
        for text in metric_texts:
            el = self.page.locator(f'text="{text}"')
            if el.count() > 0:
                metrics.append(text)
        return metrics

    def distribute_model_to_department(self, model_name: str, dept_name: str):
        logger.info(f"分发模型 {model_name} 到部门 {dept_name}")
        distribute_btn = self.page.get_by_role("button", name="分发")
        if distribute_btn.count() > 0:
            distribute_btn.first.click()
            return True
        return False