"""
简化版循环对话测试脚本
功能：对指定数字员工循环执行对话流程（不创建新数字员工）
流程：对话 -> 新建会话 -> 选择技能 -> 输入消息 -> 发送
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List
import time

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from utils.config_reader import ConfigReader
from utils.logger import get_logger
from pages.login_page import LoginPage
from pages.agent_detail_page import AgentDetailPage

logger = get_logger(__name__)


class SimpleLoopTestExecutor:
    """简化版循环测试执行器 - 不创建数字员工，只测试对话流程"""
    
    def __init__(self, config: ConfigReader, agent_id: str):
        self.config = config
        self.agent_id = agent_id
        self.base_url = config.get("test.base_url", "http://10.11.150.76:10088")
        self.username = config.get("test_data.users.admin.username", "admin")
        self.password = config.get("test_data.users.admin.password", "123456")
        
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        self.total_iterations = 0
        
    def setup(self):
        """初始化浏览器和登录"""
        logger.info("初始化测试环境...")
        
        self.playwright = sync_playwright().start()
        
        self.browser = self.playwright.chromium.launch(
            headless=False,
            slow_mo=300,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-extensions",
                "--no-sandbox",
            ]
        )
        
        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 720},
            ignore_https_errors=True,
        )
        
        self.page = self.context.new_page()
        self.page.set_default_timeout(30000)
        self.page.set_default_navigation_timeout(30000)
        
        logger.info("执行登录...")
        login_page = LoginPage(self.page)
        login_page.navigate()
        login_page.login(self.username, self.password)
        self.page.wait_for_load_state("networkidle")
        logger.info("登录成功 ✅")
        
    def teardown(self):
        """清理资源"""
        logger.info("清理测试环境...")
        if self.page:
            self.page.close()
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        logger.info("测试环境清理完成 ✅")
        
    def execute_single_conversation(self, iteration: int) -> bool:
        """执行单次对话流程"""
        try:
            print(f"\n{'='*60}")
            print(f"🔄 第 {iteration}/{self.total_iterations} 次对话测试")
            print(f"{'='*60}")
            
            agent_detail_page = AgentDetailPage(self.page, self.agent_id)
            agent_detail_page.navigate_to_agent(self.agent_id)
            self.page.wait_for_load_state("networkidle")
            
            logger.info(f"[第{iteration}次] 点击对话按钮...")
            agent_detail_page.click_chat_button()
            self.page.wait_for_timeout(1000)
            
            logger.info(f"[第{iteration}次] 点击新建会话...")
            agent_detail_page.click_new_session_button()
            self.page.wait_for_timeout(1000)
            
            logger.info(f"[第{iteration}次] 点击技能按钮...")
            agent_detail_page.click_skill_button()
            self.page.wait_for_timeout(1000)
            
            logger.info(f"[第{iteration}次] 选择cdp_skills技能...")
            agent_detail_page.select_skill_from_dropdown("cdp_skills")
            self.page.wait_for_timeout(1000)
            
            message = "搜索商红信息"
            logger.info(f"[第{iteration}次] 输入消息: {message}")
            agent_detail_page.type_chat_message(message)
            self.page.wait_for_timeout(500)
            
            logger.info(f"[第{iteration}次] 点击发送按钮...")
            agent_detail_page.click_send_button()
            self.page.wait_for_timeout(3000)
            
            print(f"✅ 第 {iteration} 次对话成功!")
            return True
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[第{iteration}次] 对话失败 ❌: {error_msg}")
            print(f"❌ 第 {iteration} 次对话失败: {error_msg}")
            
            try:
                screenshot_path = f"reports/screenshots/simple_loop_failure_{iteration}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                self.page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"失败截图已保存: {screenshot_path}")
            except:
                pass
                
            return False
        
    def run(self, total_iterations: int = 200):
        """运行循环测试"""
        self.total_iterations = total_iterations
        success_count = 0
        failure_count = 0
        start_time = datetime.now()
        
        print("\n" + "=" * 80)
        print("🚀 开始简化版循环对话测试")
        print(f"数字员工ID: {self.agent_id}")
        print(f"总次数: {total_iterations}")
        print(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)
        
        try:
            self.setup()
            
            for i in range(1, total_iterations + 1):
                success = self.execute_single_conversation(i)
                
                if success:
                    success_count += 1
                else:
                    failure_count += 1
                
                current_success_rate = (success_count / i) * 100
                print(f"\n📊 当前进度: {i}/{total_iterations} | 成功率: {current_success_rate:.2f}%")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ 用户中断测试执行")
            logger.warning("用户中断测试执行")
            
        except Exception as e:
            print(f"\n\n❌ 测试执行发生严重错误: {str(e)}")
            logger.error(f"测试执行发生严重错误: {str(e)}")
            
        finally:
            self.teardown()
            
        end_time = datetime.now()
        total_duration = (end_time - start_time).total_seconds()
        
        print("\n" + "=" * 80)
        print("📊 测试执行统计摘要")
        print("=" * 80)
        print(f"总执行次数: {total_iterations}")
        print(f"成功次数: {success_count} ✅")
        print(f"失败次数: {failure_count} ❌")
        print(f"成功率: {(success_count/total_iterations)*100:.2f}%")
        print(f"总耗时: {total_duration:.2f} 秒 ({total_duration/60:.2f} 分钟)")
        print(f"平均耗时: {total_duration/total_iterations:.2f} 秒/次")
        print("=" * 80)
        
        return success_count, failure_count


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🔄 简化版循环对话测试脚本")
    print("=" * 80)
    
    total_iterations = 200
    agent_id = "10e8a24f-1eb8-49d9-9220-a51f5d6d7232"
    
    if len(sys.argv) > 1:
        try:
            total_iterations = int(sys.argv[1])
        except ValueError:
            print(f"⚠️ 无效的循环次数参数，使用默认值: {total_iterations}")
    
    if len(sys.argv) > 2:
        agent_id = sys.argv[2]
    
    print(f"循环次数: {total_iterations}")
    print(f"数字员工ID: {agent_id}")
    print("=" * 80 + "\n")
    
    config = ConfigReader()
    executor = SimpleLoopTestExecutor(config, agent_id)
    
    success_count, failure_count = executor.run(total_iterations)
    
    if failure_count == 0:
        print("\n🎉 所有测试全部通过!")
        sys.exit(0)
    else:
        print(f"\n⚠️ 有 {failure_count} 次测试失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
