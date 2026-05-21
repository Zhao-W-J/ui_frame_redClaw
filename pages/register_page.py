from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class RegisterPage(BasePage):
    """注册页面对象"""

    USERNAME_INPUT = 'input[placeholder*="用户名"]'
    EMAIL_INPUT = 'input[placeholder*="邮箱"], input[type="email"]'
    PASSWORD_INPUT = 'input[placeholder*="密码"][type="password"]'
    DISPLAY_NAME_INPUT = 'input[placeholder*="显示名称"], input[placeholder*="昵称"]'
    INVITE_CODE_INPUT = 'input[placeholder*="邀请码"]'
    REGISTER_BUTTON = 'button:has-text("注册"), button:has-text("提交")'
    LOGIN_LINK = 'a:has-text("登录"), a:has-text("去登录")'

    page_loaded_indicator = REGISTER_BUTTON

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = f"{self.base_url}/register"

    def navigate(self) -> None:
        logger.info(f"导航到注册页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()

    def is_loaded(self) -> bool:
        return self.is_element_visible(self.REGISTER_BUTTON)

    def fill_username(self, username: str):
        logger.info(f"填写用户名: {username}")
        username_input = self.page.locator(self.USERNAME_INPUT)
        if username_input.count() > 0:
            username_input.fill(username)
            return True
        return False

    def fill_email(self, email: str):
        logger.info(f"填写邮箱: {email}")
        email_input = self.page.locator(self.EMAIL_INPUT)
        if email_input.count() > 0:
            email_input.fill(email)
            return True
        return False

    def fill_password(self, password: str):
        logger.info("填写密码")
        password_input = self.page.locator(self.PASSWORD_INPUT)
        if password_input.count() > 0:
            password_input.fill(password)
            return True
        return False

    def fill_display_name(self, display_name: str):
        logger.info(f"填写显示名称: {display_name}")
        display_input = self.page.locator(self.DISPLAY_NAME_INPUT)
        if display_input.count() > 0:
            display_input.fill(display_name)
            return True
        return False

    def fill_invite_code(self, invite_code: str):
        logger.info(f"填写邀请码: {invite_code}")
        invite_input = self.page.locator(self.INVITE_CODE_INPUT)
        if invite_input.count() > 0:
            invite_input.fill(invite_code)
            return True
        return False

    def click_register(self):
        logger.info("点击注册按钮")
        register_btn = self.page.locator(self.REGISTER_BUTTON)
        if register_btn.count() > 0:
            register_btn.click()
            return True
        return False

    def click_login_link(self):
        logger.info("点击去登录链接")
        login_link = self.page.locator(self.LOGIN_LINK)
        if login_link.count() > 0:
            login_link.click()
            return True
        return False

    def register(self, username: str, email: str, password: str,
                 display_name: str = "", invite_code: str = "") -> bool:
        logger.info(f"执行注册: 用户名={username}, 邮箱={email}")
        self.fill_username(username)
        self.fill_email(email)
        self.fill_password(password)
        if display_name:
            self.fill_display_name(display_name)
        if invite_code:
            self.fill_invite_code(invite_code)
        self.click_register()
        try:
            self.page.wait_for_load_state("networkidle", timeout=10000)
            self.page.wait_for_timeout(1000)
            current_url = self.page.url
            return "/register" not in current_url
        except Exception as e:
            logger.warning(f"注册等待超时: {e}")
            return "/register" not in self.page.url

    def is_on_register_page(self) -> bool:
        return "/register" in self.page.url

    def get_error_message(self) -> str:
        error_el = self.page.locator('[class*="error"], [class*="Error"], [role="alert"]')
        if error_el.count() > 0:
            return error_el.first.text_content().strip()
        return ""