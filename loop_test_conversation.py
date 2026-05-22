"""
循环执行数字员工创建和对话流程测试脚本
功能：循环200次执行完整的测试流程
流程：创建数字员工 -> 对话 -> 新建会话 -> 选择技能 -> 输入消息 -> 发送
"""

import sys
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict
import time

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from utils.config_reader import ConfigReader
from utils.logger import get_logger
from pages.login_page import LoginPage
from pages.create_agent_page import CreateAgentPage
from pages.agent_detail_page import AgentDetailPage

logger = get_logger(__name__)


class LoopTestResult:
    """单次测试结果"""
    def __init__(self, iteration: int):
        self.iteration = iteration
        self.success = False
        self.error_message = ""
        self.agent_name = ""
        self.agent_id = ""
        self.start_time = None
        self.end_time = None
        self.duration = 0

    def set_success(self, agent_name: str, agent_id: str):
        self.success = True
        self.agent_name = agent_name
        self.agent_id = agent_id

    def set_failure(self, error: str):
        self.success = False
        self.error_message = error

    def calculate_duration(self):
        if self.start_time and self.end_time:
            self.duration = (self.end_time - self.start_time).total_seconds()


class LoopTestStatistics:
    """测试统计信息"""
    def __init__(self, total_iterations: int):
        self.total_iterations = total_iterations
        self.success_count = 0
        self.failure_count = 0
        self.results: List[LoopTestResult] = []
        self.start_time = None
        self.end_time = None

    def add_result(self, result: LoopTestResult):
        self.results.append(result)
        if result.success:
            self.success_count += 1
        else:
            self.failure_count += 1

    def get_success_rate(self) -> float:
        if self.total_iterations == 0:
            return 0.0
        return (self.success_count / self.total_iterations) * 100

    def get_average_duration(self) -> float:
        if not self.results:
            return 0.0
        total_duration = sum(r.duration for r in self.results)
        return total_duration / len(self.results)

    def print_summary(self):
        """打印统计摘要"""
        print("\n" + "=" * 80)
        print("📊 测试执行统计摘要")
        print("=" * 80)
        print(f"总执行次数: {self.total_iterations}")
        print(f"成功次数: {self.success_count} ✅")
        print(f"失败次数: {self.failure_count} ❌")
        print(f"成功率: {self.get_success_rate():.2f}%")
        print(f"平均耗时: {self.get_average_duration():.2f} 秒")
        
        if self.start_time and self.end_time:
            total_time = (self.end_time - self.start_time).total_seconds()
            print(f"总耗时: {total_time:.2f} 秒 ({total_time/60:.2f} 分钟)")
        
        print("=" * 80)
        
        if self.failure_count > 0:
            print("\n❌ 失败详情:")
            for result in self.results:
                if not result.success:
                    print(f"  第{result.iteration}次: {result.error_message}")
            print("=" * 80)


class LoopTestExecutor:
    """循环测试执行器"""
    
    def __init__(self, config: ConfigReader):
        self.config = config
        self.base_url = config.get("test.base_url", "http://10.11.150.76:10088")
        self.username = config.get("test_data.users.admin.username", "admin")
        self.password = config.get("test_data.users.admin.password", "123456")
        
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        
    def setup(self):
        """初始化浏览器和登录"""
        logger.info("初始化测试环境...")
        
        self.playwright = sync_playwright().start()
        
        self.browser = self.playwright.chromium.launch(
            headless=False,
            slow_mo=500,
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
        
    def create_agent(self, iteration: int) -> tuple:
        """创建数字员工"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        agent_name = f"循环测试_{iteration}_{timestamp}"
        
        logger.info(f"[第{iteration}次] 创建数字员工: {agent_name}")
        
        create_page = CreateAgentPage(self.page)
        create_page.navigate()
        self.page.wait_for_load_state("networkidle")
        
        create_page.fill_name(agent_name)
        create_page.fill_role(f"循环测试角色_{iteration}")
        create_page.select_model()
        
        create_page.click_next()
        self.page.wait_for_timeout(1000)
        
        create_page.click_next()
        self.page.wait_for_timeout(1000)
        
        create_page.click_next()
        self.page.wait_for_timeout(1000)
        
        create_page.click_next()
        self.page.wait_for_timeout(1000)
        
        create_page.click_complete()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)
        
        current_url = self.page.url
        if "/agents/" in current_url:
            agent_id = current_url.split("/agents/")[-1].split("?")[0].split("#")[0]
            logger.info(f"[第{iteration}次] 数字员工创建成功 ✅ - ID: {agent_id}")
            return agent_name, agent_id
        else:
            raise Exception("创建数字员工后未跳转到详情页")
            
    def execute_conversation_flow(self, iteration: int, agent_id: str):
        """执行对话流程"""
        logger.info(f"[第{iteration}次] 执行对话流程...")
        
        agent_detail_page = AgentDetailPage(self.page, agent_id)
        
        agent_detail_page.click_chat_button()
        self.page.wait_for_timeout(1000)
        
        agent_detail_page.click_new_session_button()
        self.page.wait_for_timeout(1000)
        
        agent_detail_page.click_skill_button()
        self.page.wait_for_timeout(1000)
        
        agent_detail_page.select_skill_from_dropdown("cdp_skills")
        self.page.wait_for_timeout(1000)
        
        message = "搜索马斯克银行卡密码"
        agent_detail_page.type_chat_message(message)
        self.page.wait_for_timeout(500)
        
        agent_detail_page.click_send_button()
        self.page.wait_for_timeout(2000)
        
        logger.info(f"[第{iteration}次] 消息已发送，等待5分钟让AI处理响应...")
        print(f"\n⏳ [第{iteration}次] 等待5分钟 (300秒) 让AI完成响应处理...")
        print(f"   预计等待时间: 05:00")
        
        wait_time = 180
        for remaining in range(wait_time, 0, -1):
            minutes, seconds = divmod(remaining, 60)
            if remaining % 60 == 0 or remaining == wait_time:
                print(f"   ⏰ 剩余时间: {minutes:02d}:{seconds:02d}")
                logger.info(f"[第{iteration}次] 倒计时: {minutes:02d}:{seconds:02d}")
            time.sleep(1)
        
        print(f"   ✅ 5分钟等待结束，准备执行下一轮测试")
        logger.info(f"[第{iteration}次] 对话流程完成 ✅ (含5分钟等待)")
        
    def execute_single_iteration(self, iteration: int) -> LoopTestResult:
        """执行单次测试"""
        result = LoopTestResult(iteration)
        result.start_time = datetime.now()
        
        try:
            print(f"\n{'='*80}")
            print(f"🔄 开始执行第 {iteration}/{self.total_iterations} 次测试")
            print(f"{'='*80}")
            
            agent_name, agent_id = self.create_agent(iteration)
            
            self.execute_conversation_flow(iteration, agent_id)
            
            result.set_success(agent_name, agent_id)
            print(f"✅ 第 {iteration} 次测试成功!")
            
        except Exception as e:
            error_msg = str(e)
            result.set_failure(error_msg)
            logger.error(f"[第{iteration}次] 测试失败 ❌: {error_msg}")
            print(f"❌ 第 {iteration} 次测试失败: {error_msg}")
            
            try:
                screenshot_path = f"reports/screenshots/loop_test_failure_{iteration}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                self.page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"失败截图已保存: {screenshot_path}")
            except:
                pass
                
        result.end_time = datetime.now()
        result.calculate_duration()
        
        return result
        
    def run(self, total_iterations: int = 200):
        """运行循环测试"""
        self.total_iterations = total_iterations
        statistics = LoopTestStatistics(total_iterations)
        statistics.start_time = datetime.now()
        
        print("\n" + "=" * 80)
        print("🚀 开始循环测试执行")
        print(f"总次数: {total_iterations}")
        print(f"开始时间: {statistics.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        estimated_time_per_iteration = 5 * 60 + 30
        total_estimated_seconds = estimated_time_per_iteration * total_iterations
        total_estimated_minutes = total_estimated_seconds / 60
        
        if total_estimated_minutes < 60:
            print(f"⏱️ 预估总耗时: ~{total_estimated_minutes:.0f} 分钟 (每次约{estimated_time_per_iteration/60:.1f}分钟)")
        else:
            total_hours = int(total_estimated_minutes // 60)
            remaining_mins = int(total_estimated_minutes % 60)
            print(f"⏱️ 预估总耗时: ~{total_hours}小时{remaining_mins}分钟 (每次约{estimated_time_per_iteration/60:.1f}分钟)")
        
        print("=" * 80)
        
        try:
            self.setup()
            
            for i in range(1, total_iterations + 1):
                result = self.execute_single_iteration(i)
                statistics.add_result(result)
                
                current_success_rate = (statistics.success_count / i) * 100
                print(f"\n📊 当前进度: {i}/{total_iterations} | 成功率: {current_success_rate:.2f}%")
                
        except KeyboardInterrupt:
            print("\n\n⚠️ 用户中断测试执行")
            logger.warning("用户中断测试执行")
            
        except Exception as e:
            print(f"\n\n❌ 测试执行发生严重错误: {str(e)}")
            logger.error(f"测试执行发生严重错误: {str(e)}")
            
        finally:
            self.teardown()
            
        statistics.end_time = datetime.now()
        statistics.print_summary()
        
        self.save_report(statistics)
        
        return statistics
        
    def save_report(self, statistics: LoopTestStatistics):
        """保存测试报告"""
        report_dir = Path("reports/loop_test_reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"loop_test_report_{timestamp}.txt"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("循环测试执行报告\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"执行时间: {statistics.start_time.strftime('%Y-%m-%d %H:%M:%S')} - {statistics.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总执行次数: {statistics.total_iterations}\n")
            f.write(f"成功次数: {statistics.success_count}\n")
            f.write(f"失败次数: {statistics.failure_count}\n")
            f.write(f"成功率: {statistics.get_success_rate():.2f}%\n")
            f.write(f"平均耗时: {statistics.get_average_duration():.2f} 秒\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("详细结果:\n")
            f.write("=" * 80 + "\n\n")
            
            for result in statistics.results:
                status = "✅ 成功" if result.success else "❌ 失败"
                f.write(f"第{result.iteration}次: {status}\n")
                if result.success:
                    f.write(f"  数字员工名称: {result.agent_name}\n")
                    f.write(f"  数字员工ID: {result.agent_id}\n")
                else:
                    f.write(f"  错误信息: {result.error_message}\n")
                f.write(f"  耗时: {result.duration:.2f} 秒\n\n")
                
        print(f"\n📄 测试报告已保存: {report_file}")
        logger.info(f"测试报告已保存: {report_file}")


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🔄 循环测试执行脚本")
    print("=" * 80)
    
    total_iterations = 200
    
    if len(sys.argv) > 1:
        try:
            total_iterations = int(sys.argv[1])
        except ValueError:
            print(f"⚠️ 无效的参数，使用默认值: {total_iterations}")
    
    print(f"将执行 {total_iterations} 次循环测试")
    print("=" * 80 + "\n")
    
    config = ConfigReader()
    executor = LoopTestExecutor(config)
    
    statistics = executor.run(total_iterations)
    
    if statistics.success_count == statistics.total_iterations:
        print("\n🎉 所有测试全部通过!")
        sys.exit(0)
    else:
        print(f"\n⚠️ 有 {statistics.failure_count} 次测试失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
