from playwright.sync_api import Page, Locator, expect
from typing import Optional, List, Dict, Any
import time
import json
from utils.logger import get_logger

logger = get_logger(__name__)

class PageUtils:
    """页面操作工具类"""
    
    def __init__(self, page: Page):
        """
        初始化页面工具
        
        Args:
            page: Playwright页面对象
        """
        self.page = page
    
    def wait_for_element(self, selector: str, timeout: int = 30000) -> Locator:
        """
        等待元素出现
        
        Args:
            selector: 元素选择器
            timeout: 超时时间(毫秒)
            
        Returns:
            Locator: 元素定位器
        """
        logger.info(f"等待元素: {selector}")
        element = self.page.locator(selector)
        element.wait_for(state="visible", timeout=timeout)
        return element
    
    def safe_click(self, selector: str, timeout: int = 30000) -> bool:
        """
        安全点击元素
        
        Args:
            selector: 元素选择器
            timeout: 超时时间(毫秒)
            
        Returns:
            bool: 是否点击成功
        """
        try:
            element = self.wait_for_element(selector, timeout)
            element.click()
            logger.info(f"成功点击元素: {selector}")
            return True
        except Exception as e:
            logger.error(f"点击元素失败: {selector}, 错误: {e}")
            return False
    
    def safe_fill(self, selector: str, text: str, timeout: int = 30000) -> bool:
        """
        安全填写文本
        
        Args:
            selector: 元素选择器
            text: 要填写的文本
            timeout: 超时时间(毫秒)
            
        Returns:
            bool: 是否填写成功
        """
        try:
            element = self.wait_for_element(selector, timeout)
            element.clear()
            element.fill(text)
            logger.info(f"成功填写文本: {selector} = {text}")
            return True
        except Exception as e:
            logger.error(f"填写文本失败: {selector}, 错误: {e}")
            return False
    
    def get_text(self, selector: str, timeout: int = 30000) -> Optional[str]:
        """
        获取元素文本
        
        Args:
            selector: 元素选择器
            timeout: 超时时间(毫秒)
            
        Returns:
            Optional[str]: 元素文本，获取失败返回None
        """
        try:
            element = self.wait_for_element(selector, timeout)
            text = element.text_content()
            logger.info(f"获取元素文本: {selector} = {text}")
            return text
        except Exception as e:
            logger.error(f"获取元素文本失败: {selector}, 错误: {e}")
            return None
    
    def is_element_visible(self, selector: str, timeout: int = 5000) -> bool:
        """
        检查元素是否可见
        
        Args:
            selector: 元素选择器
            timeout: 超时时间(毫秒)
            
        Returns:
            bool: 元素是否可见
        """
        try:
            element = self.page.locator(selector)
            element.wait_for(state="visible", timeout=timeout)
            return True
        except Exception:
            return False
    
    def wait_for_page_load(self, timeout: int = 30000):
        """
        等待页面加载完成
        
        Args:
            timeout: 超时时间(毫秒)
        """
        logger.info("等待页面加载完成")
        self.page.wait_for_load_state("networkidle", timeout=timeout)
    
    def scroll_to_element(self, selector: str):
        """
        滚动到元素位置
        
        Args:
            selector: 元素选择器
        """
        try:
            element = self.page.locator(selector)
            element.scroll_into_view_if_needed()
            logger.info(f"滚动到元素: {selector}")
        except Exception as e:
            logger.error(f"滚动到元素失败: {selector}, 错误: {e}")
    
    def take_screenshot(self, file_path: str, full_page: bool = True):
        """
        截取屏幕截图
        
        Args:
            file_path: 截图保存路径
            full_page: 是否截取整个页面
        """
        try:
            self.page.screenshot(path=file_path, full_page=full_page)
            logger.info(f"截图已保存: {file_path}")
        except Exception as e:
            logger.error(f"截图失败: {e}")
    
    def execute_script(self, script: str) -> Any:
        """
        执行JavaScript脚本
        
        Args:
            script: JavaScript代码
            
        Returns:
            Any: 脚本执行结果
        """
        try:
            result = self.page.evaluate(script)
            logger.info(f"执行脚本成功: {script}")
            return result
        except Exception as e:
            logger.error(f"执行脚本失败: {script}, 错误: {e}")
            return None
    
    def wait_for_url_change(self, expected_url: str = None, timeout: int = 30000):
        """
        等待URL变化
        
        Args:
            expected_url: 期望的URL
            timeout: 超时时间(毫秒)
        """
        if expected_url:
            self.page.wait_for_url(expected_url, timeout=timeout)
            logger.info(f"URL已变化为: {expected_url}")
        else:
            current_url = self.page.url
            self.page.wait_for_function(f"window.location.href !== '{current_url}'", timeout=timeout)
            logger.info(f"URL已从 {current_url} 变化为 {self.page.url}")
    
    def get_all_elements(self, selector: str) -> List[Locator]:
        """
        获取所有匹配的元素
        
        Args:
            selector: 元素选择器
            
        Returns:
            List[Locator]: 元素列表
        """
        return self.page.locator(selector).all()
    
    def drag_and_drop(self, source_selector: str, target_selector: str):
        """
        拖拽操作
        
        Args:
            source_selector: 源元素选择器
            target_selector: 目标元素选择器
        """
        try:
            source = self.page.locator(source_selector)
            target = self.page.locator(target_selector)
            source.drag_to(target)
            logger.info(f"拖拽操作完成: {source_selector} -> {target_selector}")
        except Exception as e:
            logger.error(f"拖拽操作失败: {e}") 