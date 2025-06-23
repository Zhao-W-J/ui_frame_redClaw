from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class LoginPage(BasePage):
    """登录页面"""
    
    # 页面元素选择器
    USERNAME_INPUT = "#username"
    PASSWORD_INPUT = "#password"
    LOGIN_BUTTON = "#login-button"
    ERROR_MESSAGE = ".error-message"
    LOGOUT_BUTTON = "#logout-button"
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
        if not self.fill_text(self.USERNAME_INPUT, username):
            return False
        
        # 填写密码
        if not self.fill_text(self.PASSWORD_INPUT, password):
            return False
        
        # 点击登录按钮
        if not self.click_element(self.LOGIN_BUTTON):
            return False
        
        # 等待页面跳转或错误信息出现
        try:
            # 等待一段时间看是否有错误信息
            if self.is_element_visible(self.ERROR_MESSAGE, timeout=3000):
                error_text = self.get_element_text(self.ERROR_MESSAGE)
                logger.error(f"登录失败: {error_text}")
                return False
            else:
                logger.info("登录成功")
                return True
        except Exception as e:
            logger.error(f"登录过程出现异常: {e}")
            return False
    
    def get_error_message(self) -> str:
        """获取错误信息"""
        return self.get_element_text(self.ERROR_MESSAGE) or ""
    
    def is_login_form_visible(self) -> bool:
        """检查登录表单是否可见"""
        return (self.is_element_visible(self.USERNAME_INPUT) and 
                self.is_element_visible(self.PASSWORD_INPUT) and 
                self.is_element_visible(self.LOGIN_BUTTON))
    
    def clear_login_form(self):
        """清空登录表单"""
        self.fill_text(self.USERNAME_INPUT, "")
        self.fill_text(self.PASSWORD_INPUT, "") 