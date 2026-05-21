from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class PlazaPage(BasePage):
    """智能体广场页面对象"""

    # 页面元素定位器
    PLAZA_HEADING = 'h1:has-text("智能体广场")'
    SUBTITLE = 'p:has-text("数字员工与人类分享见解、想法和更新的地方。")'
    POSTS_STAT = 'text="帖子"'
    COMMENTS_STAT = 'text="评论"'
    TODAY_STAT = 'text="今日"'
    DELETE_POST_BUTTON = 'button:has-text("删除帖子")'
    SEARCH_INPUT = 'input[placeholder="搜索..."]'

    # 侧边栏导航
    NAV_PLAZA = 'a:has-text("广场")'
    NAV_DASHBOARD = 'a:has-text("仪表盘")'
    NAV_NEW_AGENT = 'a:has-text("新建数字员工")'
    NAV_ENTERPRISE = 'a:has-text("部门设置")'
    NAV_SETTINGS = 'a:has-text("公司设置")'

    # 侧边栏功能按钮
    DARK_MODE_BUTTON = 'button:has-text("深色模式")'
    NOTIFICATION_BUTTON = 'button[aria-label*="通知"]'
    SWITCH_DEPT_BUTTON = 'button:has-text("切换部门")'
    
    # 数字员工列表相关
    AGENT_LINK_TEMPLATE = 'a:has-text("{}")'
    PIN_BUTTON = 'button:has-text("置顶")'

    page_loaded_indicator = PLAZA_HEADING

    def __init__(self, page: Page):
        """
        初始化广场页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = f"{self.base_url}/plaza"

    def navigate(self) -> None:
        """导航到广场页面"""
        logger.info(f"导航到广场页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()

    def is_loaded(self) -> bool:
        """检查广场页面是否加载完成"""
        return self.is_element_visible(self.PLAZA_HEADING)

    def get_posts_count(self) -> str:
        """获取帖子统计数"""
        posts_el = self.page.locator('div >> text=帖子').first
        if posts_el.count() > 0:
            return posts_el.text_content().strip()
        return "0"

    def get_comments_count(self) -> str:
        """获取评论统计数"""
        comments_el = self.page.locator('div >> text=评论').first
        if comments_el.count() > 0:
            return comments_el.text_content().strip()
        return "0"

    def get_today_count(self) -> str:
        """获取今日统计数"""
        today_el = self.page.locator('div >> text=今日').first
        if today_el.count() > 0:
            return today_el.text_content().strip()
        return "0"

    def get_post_list_count(self) -> int:
        """获取帖子列表数量"""
        post_items = self.page.locator('article, [class*=post], [class*=card]')
        return post_items.count()

    def click_delete_post_button(self):
        """点击删除帖子按钮"""
        logger.info("点击删除帖子按钮")
        delete_btn = self.page.get_by_role("button", name="删除帖子")
        if delete_btn.count() > 0:
            delete_btn.first.click()
            return True
        return False

    def search_agents(self, keyword: str):
        """搜索数字员工"""
        logger.info(f"搜索数字员工: {keyword}")
        search_input = self.page.get_by_placeholder("搜索...")
        search_input.fill(keyword)

    def click_agent_by_name(self, agent_name: str):
        """通过名称点击数字员工"""
        logger.info(f"点击数字员工: {agent_name}")
        agent_link = self.page.get_by_role("link", name=agent_name)
        if agent_link.count() > 0:
            agent_link.first.click()
            return True
        return False

    def click_pin_button(self):
        """点击置顶按钮"""
        logger.info("点击置顶按钮")
        pin_btn = self.page.get_by_role("button", name="置顶")
        if pin_btn.count() > 0:
            pin_btn.first.click()
            return True
        return False

    def navigate_to_dashboard(self):
        """导航到仪表盘"""
        logger.info("从广场导航到仪表盘")
        dashboard_link = self.page.get_by_role("link", name="仪表盘")
        dashboard_link.click()

    def navigate_to_new_agent(self):
        """导航到新建数字员工"""
        logger.info("从广场导航到新建数字员工")
        new_agent_link = self.page.get_by_role("link", name="新建数字员工")
        new_agent_link.click()

    def navigate_to_enterprise(self):
        """导航到部门设置"""
        logger.info("从广场导航到部门设置")
        enterprise_link = self.page.get_by_role("link", name="部门设置")
        enterprise_link.click()

    def navigate_to_settings(self):
        """导航到公司设置"""
        logger.info("从广场导航到公司设置")
        settings_link = self.page.get_by_role("link", name="公司设置")
        settings_link.click()

    def toggle_dark_mode(self):
        """切换深色模式"""
        logger.info("切换深色模式")
        dark_mode_btn = self.page.get_by_role("button", name="深色模式")
        dark_mode_btn.click()

    def click_notification(self):
        """点击通知按钮"""
        logger.info("点击通知按钮")
        notification_btn = self.page.locator(self.NOTIFICATION_BUTTON)
        if notification_btn.count() > 0:
            notification_btn.click()
            return True
        return False

    def click_switch_department(self):
        """点击切换部门按钮"""
        logger.info("点击切换部门按钮")
        switch_btn = self.page.get_by_role("button", name="切换部门")
        switch_btn.click()
