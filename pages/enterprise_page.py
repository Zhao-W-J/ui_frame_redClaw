from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class EnterprisePage(BasePage):
    """部门设置页面对象 - 包含10个标签页"""

    PAGE_HEADING = 'h1:has-text("部门设置")'

    TAB_DEPT_INFO = 'button:has-text("部门信息"), a:has-text("部门信息")'
    TAB_MODEL_POOL = 'button:has-text("模型池"), a:has-text("模型池")'
    TAB_TOOLS = 'button:has-text("工具"), a:has-text("工具")'
    TAB_SKILLS = 'button:has-text("技能管理"), a:has-text("技能管理")'
    TAB_INVITATIONS = 'button:has-text("邀请码"), a:has-text("邀请码")'
    TAB_QUOTA = 'button:has-text("配额"), a:has-text("配额")'
    TAB_USERS = 'button:has-text("用户"), a:has-text("用户")'
    TAB_ORG = 'button:has-text("组织管理"), a:has-text("组织管理")'
    TAB_APPROVALS = 'button:has-text("审批"), a:has-text("审批")'
    TAB_AUDIT = 'button:has-text("审计日志"), a:has-text("审计日志")'

    DEPT_NAME_INPUT = 'input[name="name"], input[placeholder*="部门名称"]'
    DEPT_DESC_INPUT = 'textarea[name="description"], textarea[placeholder*="简介"]'
    TIMEZONE_SELECT = 'select[name="timezone"], [role="combobox"]:near(:text("时区"))'
    SAVE_BUTTON = 'button:has-text("保存")'

    BROADCAST_TITLE_INPUT = 'input[placeholder*="标题"]'
    BROADCAST_CONTENT_INPUT = 'textarea[placeholder*="内容"]'
    BROADCAST_SEND_BUTTON = 'button:has-text("发送")'

    UPLOAD_BUTTON = 'button:has-text("Upload"), button:has-text("上传")'
    NEW_FOLDER_BUTTON = 'button:has-text("新建文件夹")'

    page_loaded_indicator = PAGE_HEADING

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = f"{self.base_url}/enterprise"

    def navigate(self) -> None:
        logger.info(f"导航到部门设置页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()

    def is_loaded(self) -> bool:
        return self.is_element_visible(self.PAGE_HEADING)

    def click_tab(self, tab_name: str):
        logger.info(f"点击部门设置标签: {tab_name}")
        tab = self.page.get_by_role("tab", name=tab_name)
        if tab.count() > 0:
            tab.click()
        else:
            tab_btn = self.page.locator(f'button:has-text("{tab_name}"), a:has-text("{tab_name}")')
            if tab_btn.count() > 0:
                tab_btn.first.click()
        self.page.wait_for_timeout(500)

    def get_department_name(self) -> str:
        name_input = self.page.locator(self.DEPT_NAME_INPUT)
        if name_input.count() > 0:
            return name_input.input_value()
        return ""

    def set_department_name(self, name: str):
        logger.info(f"设置部门名称: {name}")
        name_input = self.page.locator(self.DEPT_NAME_INPUT)
        if name_input.count() > 0:
            name_input.fill(name)
            return True
        return False

    def set_department_description(self, description: str):
        logger.info(f"设置部门简介: {description}")
        desc_input = self.page.locator(self.DEPT_DESC_INPUT)
        if desc_input.count() > 0:
            desc_input.fill(description)
            return True
        return False

    def select_timezone(self, timezone: str):
        logger.info(f"选择时区: {timezone}")
        tz_select = self.page.locator(self.TIMEZONE_SELECT)
        if tz_select.count() > 0:
            tz_select.select_option(timezone)
            return True
        return False

    def select_theme_color(self, color_index: int = 0):
        logger.info(f"选择主题色: 第{color_index}个")
        color_buttons = self.page.locator('[class*="color"], [class*="theme"] button, [class*="color"] div[role="button"]')
        if color_buttons.count() > color_index:
            color_buttons.nth(color_index).click()
            return True
        return False

    def click_save(self):
        logger.info("点击保存按钮")
        save_btn = self.page.get_by_role("button", name="保存")
        if save_btn.count() > 0:
            save_btn.click()
            return True
        return False

    def upload_knowledge_file(self, file_path: str):
        logger.info(f"上传知识库文件: {file_path}")
        file_input = self.page.locator('input[type="file"]')
        if file_input.count() > 0:
            file_input.first.set_input_files(file_path)
            return True
        return False

    def click_new_folder(self):
        logger.info("点击新建文件夹")
        folder_btn = self.page.get_by_role("button", name="新建文件夹")
        if folder_btn.count() > 0:
            folder_btn.click()
            return True
        return False

    def delete_knowledge_file(self, file_name: str):
        logger.info(f"删除知识库文件: {file_name}")
        delete_btn = self.page.locator(f'[aria-label="删除 {file_name}"], button:has-text("×"):near(:text("{file_name}"))')
        if delete_btn.count() > 0:
            delete_btn.first.click()
            return True
        return False

    def send_broadcast(self, title: str, content: str):
        logger.info(f"发送广播通知: {title}")
        title_input = self.page.locator(self.BROADCAST_TITLE_INPUT)
        if title_input.count() > 0:
            title_input.fill(title)
        content_input = self.page.locator(self.BROADCAST_CONTENT_INPUT)
        if content_input.count() > 0:
            content_input.fill(content)
        send_btn = self.page.locator(self.BROADCAST_SEND_BUTTON)
        if send_btn.count() > 0:
            send_btn.click()
            return True
        return False

    def is_dept_info_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_DEPT_INFO)

    def is_model_pool_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_MODEL_POOL)

    def is_tools_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_TOOLS)

    def is_skills_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_SKILLS)

    def is_invitations_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_INVITATIONS)

    def is_quota_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_QUOTA)

    def is_users_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_USERS)

    def is_org_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_ORG)

    def is_approvals_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_APPROVALS)

    def is_audit_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_AUDIT)

    def get_all_tab_names(self) -> list:
        tabs = [
            "部门信息", "模型池", "工具", "技能管理", "邀请码",
            "配额", "用户", "组织管理", "审批", "审计日志"
        ]
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

    def search_invitation_code(self, keyword: str):
        logger.info(f"搜索邀请码: {keyword}")
        search_input = self.page.get_by_placeholder("搜索")
        if search_input.count() > 0:
            search_input.fill(keyword)
            return True
        return False

    def batch_create_invitations(self, count: int, max_uses: int):
        logger.info(f"批量创建邀请码: 数量={count}, 最大使用次数={max_uses}")
        batch_btn = self.page.get_by_role("button", name="批量创建")
        if batch_btn.count() > 0:
            batch_btn.click()
            return True
        return False

    def deactivate_invitation(self):
        logger.info("停用邀请码")
        deactivate_btn = self.page.get_by_role("button", name="停用")
        if deactivate_btn.count() > 0:
            deactivate_btn.first.click()
            return True
        return False

    def export_csv(self):
        logger.info("导出CSV")
        export_btn = self.page.get_by_role("button", name="导出")
        if export_btn.count() > 0:
            export_btn.click()
            return True
        return False

    def click_upload_button(self):
        logger.info("点击上传按钮")
        upload_btn = self.page.get_by_role("button", name="Upload")
        if upload_btn.count() > 0:
            upload_btn.click()
            return True
        upload_btn = self.page.get_by_role("button", name="上传")
        if upload_btn.count() > 0:
            upload_btn.click()
            return True
        return False