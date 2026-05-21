from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class DashboardPage(BasePage):
    """仪表盘页面对象"""

    # 页面元素定位器
    GREETING_HEADING = 'h1 >> text=/好/'
    EMPLOYEE_COUNT_TEXT = 'text="共"'
    NEW_AGENT_BUTTON = 'button:has-text("新建数字员工")'
    
    # 统计卡片
    CARD_EMPLOYEE = 'text="数字员工"'
    CARD_TASKS = 'text="进行中任务"'
    CARD_TOKEN = 'text="今日 Token"'
    CARD_ACTIVE = 'text="最近活跃"'

    # 员工列表表头
    TABLE_HEADER_EMPLOYEE = 'text="员工"'
    TABLE_HEADER_DYNAMIC = 'text="最新动态"'
    TABLE_HEADER_TOKEN = 'text="Token"'
    TABLE_HEADER_ACTIVE = 'text="活跃"'

    # 全局活动
    ACTIVITY_HEADING = 'h3:has-text("全局活动")'

    page_loaded_indicator = GREETING_HEADING

    def __init__(self, page: Page):
        """
        初始化仪表盘页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = f"{self.base_url}/dashboard"

    def navigate(self) -> None:
        """导航到仪表盘页面"""
        logger.info(f"导航到仪表盘页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()

    def is_loaded(self) -> bool:
        """检查仪表盘页面是否加载完成"""
        return self.is_element_visible(self.CARD_EMPLOYEE)

    def get_greeting_text(self) -> str:
        """获取问候语文本"""
        greeting_el = self.page.locator('h1')
        if greeting_el.count() > 0:
            return greeting_el.text_content().strip()
        return ""

    def get_employee_count(self) -> str:
        """获取数字员工总数文本"""
        count_el = self.page.locator(self.EMPLOYEE_COUNT_TEXT)
        if count_el.count() > 0:
            parent = count_el.first.locator("..")
            return parent.text_content().strip()
        return ""

    def is_employee_card_visible(self) -> bool:
        """检查数字员工统计卡片是否可见"""
        return self.is_element_visible(self.CARD_EMPLOYEE)

    def is_tasks_card_visible(self) -> bool:
        """检查进行中任务卡片是否可见"""
        return self.is_element_visible(self.CARD_TASKS)

    def is_token_card_visible(self) -> bool:
        """检查今日Token卡片是否可见"""
        return self.is_element_visible(self.CARD_TOKEN)

    def is_active_card_visible(self) -> bool:
        """检查最近活跃卡片是否可见"""
        return self.is_element_visible(self.CARD_ACTIVE)

    def are_all_stats_cards_visible(self) -> bool:
        """检查所有统计卡片是否可见"""
        return (self.is_employee_card_visible() and 
                self.is_tasks_card_visible() and 
                self.is_token_card_visible() and 
                self.is_active_card_visible())

    def get_table_headers(self) -> list:
        """获取员工列表表头"""
        headers = []
        header_selectors = [
            self.TABLE_HEADER_EMPLOYEE,
            self.TABLE_HEADER_DYNAMIC,
            self.TABLE_HEADER_TOKEN,
            self.TABLE_HEADER_ACTIVE
        ]
        for selector in header_selectors:
            el = self.page.locator(selector)
            if el.count() > 0:
                headers.append(el.text_content())
        return headers

    def get_employee_list_count(self) -> int:
        """获取员工列表行数"""
        rows = self.page.locator('[class*=row], [class*=employee], tr')
        return rows.count()

    def click_new_agent_button(self):
        """点击新建数字员工按钮"""
        logger.info("点击新建数字员工按钮")
        new_agent_btn = self.page.get_by_role("button", name="新建数字员工")
        new_agent_btn.click()

    def click_agent_row(self, index: int = 0):
        """点击员工列表中的某一行
        
        Args:
            index: 行索引，从0开始
        """
        logger.info(f"点击员工列表第{index + 1}行")
        rows = self.page.locator('[class*=employee-item], [class*=agent-row], [class*="cursor-pointer"]')
        if rows.count() > index:
            rows.nth(index).click()
            return True
        return False

    def is_activity_section_visible(self) -> bool:
        """检查全局活动区域是否可见"""
        return self.is_element_visible(self.ACTIVITY_HEADING)

    def get_activity_count(self) -> int:
        """获取活动记录数量"""
        activity_items = self.page.locator('[class*=activity], [class*=log]')
        return activity_items.count()
