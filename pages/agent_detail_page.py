from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)


class AgentDetailPage(BasePage):
    """数字员工详情页对象 - 包含11个标签页"""

    PAGE_HEADING = 'h1'

    TAB_STATUS = 'button:has-text("状态"), a:has-text("状态")'
    TAB_AWARE = 'button:has-text("自我意识"), a:has-text("自我意识")'
    TAB_MIND = 'button:has-text("心智"), a:has-text("心智")'
    TAB_TOOLS = 'button:has-text("工具"), a:has-text("工具")'
    TAB_SKILLS = 'button:has-text("技能"), a:has-text("技能")'
    TAB_RELATIONS = 'button:has-text("关系"), a:has-text("关系")'
    TAB_WORKSPACE = 'button:has-text("工作区"), a:has-text("工作区")'
    TAB_CHAT = 'button:has-text("聊天"), a:has-text("聊天")'
    TAB_LOGS = 'button:has-text("工作日志"), a:has-text("工作日志")'
    TAB_APPROVALS = 'button:has-text("审批"), a:has-text("审批")'
    TAB_SETTINGS = 'button:has-text("设置"), a:has-text("设置")'

    CHAT_BUTTON = 'button:has-text("对话")'
    RENEW_BUTTON = 'button:has-text("续期")'

    page_loaded_indicator = PAGE_HEADING

    def __init__(self, page: Page, agent_id: str = None):
        super().__init__(page)
        self.agent_id = agent_id
        if agent_id:
            self.page_url = f"{self.base_url}/agents/{agent_id}"
        else:
            self.page_url = f"{self.base_url}/agents/"

    def navigate(self) -> None:
        logger.info(f"导航到数字员工详情页: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()

    def navigate_to_agent(self, agent_id: str) -> None:
        self.agent_id = agent_id
        self.page_url = f"{self.base_url}/agents/{agent_id}"
        self.navigate()

    def is_loaded(self) -> bool:
        return self.is_element_visible(self.PAGE_HEADING)

    def get_agent_name(self) -> str:
        heading = self.page.locator('h1')
        if heading.count() > 0:
            return heading.text_content().strip()
        return ""

    def click_tab(self, tab_name: str):
        tab_map = {
            "状态": self.TAB_STATUS,
            "自我意识": self.TAB_AWARE,
            "心智": self.TAB_MIND,
            "工具": self.TAB_TOOLS,
            "技能": self.TAB_SKILLS,
            "关系": self.TAB_RELATIONS,
            "工作区": self.TAB_WORKSPACE,
            "聊天": self.TAB_CHAT,
            "工作日志": self.TAB_LOGS,
            "审批": self.TAB_APPROVALS,
            "设置": self.TAB_SETTINGS,
        }
        logger.info(f"点击标签: {tab_name}")
        tab = self.page.get_by_role("tab", name=tab_name)
        if tab.count() > 0:
            tab.click()
        else:
            tab_btn = self.page.locator(f'button:has-text("{tab_name}"), a:has-text("{tab_name}")')
            if tab_btn.count() > 0:
                tab_btn.first.click()
        self.page.wait_for_timeout(500)

    def click_chat_button(self):
        logger.info("点击对话按钮")
        chat_btn = self.page.get_by_role("button", name="对话")
        if chat_btn.count() > 0:
            chat_btn.click()
            return True
        return False

    def click_renew_button(self):
        logger.info("点击续期按钮")
        renew_btn = self.page.get_by_role("button", name="续期")
        if renew_btn.count() > 0:
            renew_btn.click()
            return True
        return False

    def is_status_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_STATUS)

    def is_aware_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_AWARE)

    def is_mind_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_MIND)

    def is_tools_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_TOOLS)

    def is_skills_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_SKILLS)

    def is_relations_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_RELATIONS)

    def is_workspace_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_WORKSPACE)

    def is_chat_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_CHAT)

    def is_logs_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_LOGS)

    def is_approvals_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_APPROVALS)

    def is_settings_tab_visible(self) -> bool:
        return self.is_element_visible(self.TAB_SETTINGS)

    def get_all_tab_names(self) -> list:
        tabs = [
            "状态", "自我意识", "心智", "工具", "技能",
            "关系", "工作区", "聊天", "工作日志", "审批", "设置"
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

    def get_status_text(self) -> str:
        status_el = self.page.locator('text="正在工作", text="待命中"')
        if status_el.count() > 0:
            return status_el.first.text_content().strip()
        return ""

    def is_on_detail_page(self) -> bool:
        current_url = self.page.url
        return "/agents/" in current_url

    def is_on_chat_page(self) -> bool:
        current_url = self.page.url
        return "/agents/" in current_url and "/chat" in current_url

    def click_edit_button(self):
        logger.info("点击编辑按钮")
        edit_btn = self.page.get_by_role("button", name="编辑")
        if edit_btn.count() > 0:
            edit_btn.first.click()
            return True
        return False

    def click_delete_button(self):
        logger.info("点击删除按钮")
        delete_btn = self.page.get_by_role("button", name="删除")
        if delete_btn.count() > 0:
            delete_btn.click()
            return True
        return False

    def confirm_dialog(self):
        logger.info("确认对话框")
        confirm_btn = self.page.get_by_role("button", name="确认")
        if confirm_btn.count() > 0:
            confirm_btn.click()
            return True
        return False

    def cancel_dialog(self):
        logger.info("取消对话框")
        cancel_btn = self.page.get_by_role("button", name="取消")
        if cancel_btn.count() > 0:
            cancel_btn.click()
            return True
        return False

    def send_chat_message(self, message: str):
        logger.info(f"发送聊天消息: {message}")
        textarea = self.page.locator('textarea, [contenteditable="true"]')
        if textarea.count() > 0:
            textarea.first.fill(message)
            self.page.keyboard.press("Enter")
            return True
        return False

    def click_new_session(self):
        logger.info("点击新建会话")
        new_btn = self.page.get_by_role("button", name="新建会话")
        if new_btn.count() > 0:
            new_btn.click()
            return True
        return False

    def click_new_folder(self):
        logger.info("点击新建文件夹")
        folder_btn = self.page.get_by_role("button", name="新建文件夹")
        if folder_btn.count() > 0:
            folder_btn.click()
            return True
        return False

    def click_new_file(self):
        logger.info("点击新建文件")
        file_btn = self.page.get_by_role("button", name="新建文件")
        if file_btn.count() > 0:
            file_btn.click()
            return True
        return False

    def click_upload_file(self):
        logger.info("点击上传文件")
        upload_btn = self.page.get_by_role("button", name="上传")
        if upload_btn.count() > 0:
            upload_btn.click()
            return True
        return False

    def click_download_button(self):
        logger.info("点击下载按钮")
        download_btn = self.page.locator('[aria-label="下载"], button:has-text("下载")')
        if download_btn.count() > 0:
            download_btn.first.click()
            return True
        return False

    def click_approve_button(self):
        logger.info("点击同意审批")
        approve_btn = self.page.get_by_role("button", name="同意")
        if approve_btn.count() > 0:
            approve_btn.click()
            return True
        return False

    def click_reject_button(self):
        logger.info("点击拒绝审批")
        reject_btn = self.page.get_by_role("button", name="拒绝")
        if reject_btn.count() > 0:
            reject_btn.click()
            return True
        return False

    def toggle_tool(self, tool_name: str):
        logger.info(f"切换工具状态: {tool_name}")
        tool_switch = self.page.locator(f'label:has-text("{tool_name}") >> [role="switch"], label:has-text("{tool_name}") >> [type="checkbox"]')
        if tool_switch.count() > 0:
            tool_switch.first.click()
            return True
        return False

    def click_reset_to_global(self):
        logger.info("点击重置为全局配置")
        reset_btn = self.page.get_by_role("button", name="重置")
        if reset_btn.count() > 0:
            reset_btn.click()
            return True
        return False

    def click_test_connection(self):
        logger.info("点击测试连接")
        test_btn = self.page.get_by_role("button", name="测试连接")
        if test_btn.count() > 0:
            test_btn.click()
            return True
        return False

    def click_new_skill(self):
        logger.info("点击新建技能")
        new_btn = self.page.get_by_role("button", name="新建技能")
        if new_btn.count() > 0:
            new_btn.click()
            return True
        return False

    def click_github_import(self):
        logger.info("点击从GitHub导入")
        import_btn = self.page.get_by_role("button", name="GitHub导入")
        if import_btn.count() > 0:
            import_btn.click()
            return True
        return False

    def click_clawhub_install(self):
        logger.info("点击从ClawHub安装")
        install_btn = self.page.get_by_role("button", name="ClawHub")
        if install_btn.count() > 0:
            install_btn.click()
            return True
        return False

    def add_relation(self, target_name: str, relation_type: str):
        logger.info(f"添加关系: {target_name} - {relation_type}")
        add_btn = self.page.get_by_role("button", name="添加关系")
        if add_btn.count() > 0:
            add_btn.click()
            return True
        return False

    def edit_relation_description(self, description: str):
        logger.info(f"编辑关系描述: {description}")
        desc_input = self.page.locator('textarea, input[type="text"]')
        if desc_input.count() > 0:
            desc_input.first.fill(description)
            return True
        return False

    def delete_relation(self):
        logger.info("删除关系")
        delete_btn = self.page.get_by_role("button", name="删除关系")
        if delete_btn.count() > 0:
            delete_btn.click()
            return True
        return False

    def select_model_in_settings(self, model_name: str):
        logger.info(f"在设置中选择模型: {model_name}")
        model_select = self.page.get_by_role("combobox")
        if model_select.count() > 0:
            model_select.first.select_option(model_name)
            return True
        return False

    def set_autonomy_level(self, level: str):
        logger.info(f"设置自主性级别: {level}")
        level_radio = self.page.get_by_role("radio", name=level)
        if level_radio.count() > 0:
            level_radio.click()
            return True
        return False

    def set_visibility(self, visibility: str):
        logger.info(f"设置可见范围: {visibility}")
        vis_radio = self.page.get_by_role("radio", name=visibility)
        if vis_radio.count() > 0:
            vis_radio.click()
            return True
        return False

    def set_expiry_date(self, date_str: str):
        logger.info(f"设置过期时间: {date_str}")
        date_input = self.page.locator('input[type="date"]')
        if date_input.count() > 0:
            date_input.first.fill(date_str)
            return True
        return False

    def toggle_heartbeat(self):
        logger.info("切换心跳配置")
        hb_switch = self.page.locator('[role="switch"]:near(:text("心跳"))')
        if hb_switch.count() > 0:
            hb_switch.click()
            return True
        return False

    def click_save_settings(self):
        logger.info("点击保存设置")
        save_btn = self.page.get_by_role("button", name="保存")
        if save_btn.count() > 0:
            save_btn.click()
            return True
        return False

    def click_stop_generation(self):
        logger.info("点击停止生成")
        stop_btn = self.page.get_by_role("button", name="停止")
        if stop_btn.count() > 0:
            stop_btn.click()
            return True
        return False

    def upload_chat_file(self, file_path: str):
        logger.info(f"上传聊天文件: {file_path}")
        file_input = self.page.locator('input[type="file"]')
        if file_input.count() > 0:
            file_input.first.set_input_files(file_path)
            return True
        return False