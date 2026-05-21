from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class LoginPage(BasePage):
    """登录页面对象"""

    # 页面元素定位器 - 使用语义化选择器
    USERNAME_INPUT = 'input[placeholder="请输入用户名"]'
    PASSWORD_INPUT = 'input[placeholder="请输入密码"]'
    LOGIN_BUTTON = 'button:has-text("登录→")'
    LANGUAGE_BUTTON = 'button:has-text("EN")'
    REGISTER_LINK = 'a:has-text("去注册")'
    LOGIN_HEADING = 'h2:has-text("登录")'
    WELCOME_TEXT = 'p:has-text("欢迎回来，请登录继续。")'
    
    page_loaded_indicator = USERNAME_INPUT

    def __init__(self, page: Page):
        """
        初始化登录页面
        
        Args:
            page: Playwright页面对象
        """
        super().__init__(page)
        self.page_url = f"{self.base_url}/login"

    def navigate(self) -> None:
        """导航到登录页面"""
        logger.info(f"导航到登录页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()

    def is_loaded(self) -> bool:
        """检查登录页面是否加载完成"""
        return self.is_element_visible(self.USERNAME_INPUT)

    def login(self, username: str, password: str) -> bool:
        """
        执行登录操作
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            bool: 登录是否成功
        """
        logger.info(f"开始登录: 用户名={username}")

        # 填写用户名
        username_input = self.page.get_by_placeholder("请输入用户名")
        username_input.fill(username)
        
        # 填写密码
        password_input = self.page.get_by_placeholder("请输入密码")
        password_input.fill(password)
        
        # 点击登录按钮
        login_btn = self.page.get_by_role("button", name="登录→")
        login_btn.click()
        
        # 等待页面跳转完成
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
            self.page.wait_for_timeout(1000)
            current_url = self.page.url
            
            # 检查是否已离开登录页
            if "/login" not in current_url:
                logger.info(f"登录成功，当前URL: {current_url}")
                return True
            else:
                logger.warning(f"仍在登录页面，可能登录失败")
                return False
        except Exception as e:
            logger.warning(f"登录等待超时: {e}")
            current_url = self.page.url
            return "/login" not in current_url

    def login_with_empty_username(self, password: str):
        """空用户名登录测试"""
        logger.info("执行空用户名登录测试")
        
        password_input = self.page.get_by_placeholder("请输入密码")
        password_input.fill(password)
        
        login_btn = self.page.get_by_role("button", name="登录→")
        login_btn.click()
        
        return self.is_login_page()

    def login_with_empty_password(self, username: str):
        """空密码登录测试"""
        logger.info("执行空密码登录测试")
        
        username_input = self.page.get_by_placeholder("请输入用户名")
        username_input.fill(username)
        
        login_btn = self.page.get_by_role("button", name="登录→")
        login_btn.click()
        
        return self.is_login_page()

    def login_with_wrong_password(self, username: str, wrong_password: str):
        """错误密码登录测试"""
        logger.info(f"执行错误密码登录测试: 用户名={username}")
        
        username_input = self.page.get_by_placeholder("请输入用户名")
        username_input.fill(username)
        
        password_input = self.page.get_by_placeholder("请输入密码")
        password_input.fill(wrong_password)
        
        login_btn = self.page.get_by_role("button", name="登录→")
        login_btn.click()
        
        return self.is_login_page()

    def click_language_switch(self):
        """点击语言切换按钮"""
        logger.info("点击语言切换按钮")
        lang_btn = self.page.get_by_role("button", name="EN")
        lang_btn.click()

    def click_register_link(self):
        """点击去注册链接"""
        logger.info("点击去注册链接")
        register_link = self.page.get_by_role("link", name="去注册")
        register_link.click()

    def is_login_page(self) -> bool:
        """检查当前是否在登录页面"""
        current_url = self.page.url
        return "/login" in current_url

    def get_welcome_text(self) -> str:
        """获取欢迎语文本"""
        welcome_el = self.page.locator(self.WELCOME_TEXT)
        if welcome_el.count() > 0:
            return welcome_el.text_content()
        return ""

    def clear_login_form(self):
        """清空登录表单"""
        username_input = self.page.get_by_placeholder("请输入用户名")
        password_input = self.page.get_by_placeholder("请输入密码")
        username_input.clear()
        password_input.clear()
