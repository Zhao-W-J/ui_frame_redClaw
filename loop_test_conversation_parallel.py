"""
并行循环测试脚本 - 同时打开3个页面创建数字员工
功能：使用多线程同时执行3个独立的测试流程
特点：每个线程有独立的浏览器、页面、登录会话
"""

import sys
import os
import time
import threading
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed, Future

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
from utils.config_reader import ConfigReader
from utils.logger import get_logger
from pages.login_page import LoginPage
from pages.create_agent_page import CreateAgentPage
from pages.agent_detail_page import AgentDetailPage

logger = get_logger(__name__)


class ParallelTestResult:
    """单次并行测试结果"""
    def __init__(self, thread_id: int, iteration: int):
        self.thread_id = thread_id
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


class ParallelTestStatistics:
    """并行测试统计信息"""
    def __init__(self, total_iterations: int, parallel_count: int):
        self.total_iterations = total_iterations
        self.parallel_count = parallel_count
        self.success_count = 0
        self.failure_count = 0
        self.results: List[ParallelTestResult] = []
        self.start_time = None
        self.end_time = None
        self.lock = threading.Lock()

    def add_result(self, result: ParallelTestResult):
        with self.lock:
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
        with self.lock:
            print("\n" + "=" * 80)
            print("📊 并行测试执行统计摘要")
            print("=" * 80)
            print(f"并行数量: {self.parallel_count} 个浏览器")
            print(f"总执行次数: {self.total_iterations}")
            print(f"成功次数: {self.success_count} ✅")
            print(f"失败次数: {self.failure_count} ❌")
            print(f"成功率: {self.get_success_rate():.2f}%")
            print(f"平均耗时: {self.get_average_duration():.2f} 秒")
            
            if self.start_time and self.end_time:
                total_time = (self.end_time - self.start_time).total_seconds()
                print(f"总耗时: {total_time:.2f} 秒 ({total_time/60:.2f} 分钟)")
                
                # 计算加速比
                single_thread_estimated = total_time * self.parallel_count
                speedup = single_thread_estimated / total_time if total_time > 0 else 0
                print(f"⚡ 加速比: ~{speedup:.2f}x (相比单线程)")
            
            print("=" * 80)
            
            if self.failure_count > 0:
                print("\n❌ 失败详情:")
                for result in self.results:
                    if not result.success:
                        print(f"  [线程{result.thread_id}] 第{result.iteration}次: {result.error_message}")
                print("=" * 80)


class ParallelTestWorker:
    """单个并行工作线程"""
    
    def __init__(self, config: ConfigReader, thread_id: int):
        self.config = config
        self.thread_id = thread_id
        self.base_url = config.get("test.base_url", "http://10.11.150.76:10088")
        self.username = config.get("test_data.users.admin.username", "admin")
        self.password = config.get("test_data.users.admin.password", "123456")
        
        self.browser: Browser = None
        self.context: BrowserContext = None
        self.page: Page = None
        
    def setup(self):
        """初始化该线程的浏览器和登录"""
        logger.info(f"[线程{self.thread_id}] 初始化测试环境...")
        
        # 每个线程创建独立的 Playwright 实例
        self.playwright_instance = sync_playwright().start()
        
        self.browser = self.playwright_instance.chromium.launch(
            headless=False,
            slow_mo=300,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-extensions",
                "--no-sandbox",
                f"--window-position={self.thread_id * 400},0",  # 窗口位置错开
            ]
        )
        
        self.context = self.browser.new_context(
            viewport={"width": 1280, "height": 720},
            ignore_https_errors=True,
            user_agent=f"ParallelTestBot-Thread-{self.thread_id}",  # 不同UA避免冲突
        )
        
        self.page = self.context.new_page()
        self.page.set_default_timeout(30000)
        self.page.set_default_navigation_timeout(30000)
        
        logger.info(f"[线程{self.thread_id}] 执行登录...")
        login_page = LoginPage(self.page)
        login_page.navigate()
        login_page.login(self.username, self.password)
        self.page.wait_for_load_state("networkidle")
        logger.info(f"[线程{self.thread_id}] 登录成功 ✅")
        
    def teardown(self):
        """清理该线程的资源"""
        logger.info(f"[线程{self.thread_id}] 清理测试环境...")
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if hasattr(self, 'playwright_instance') and self.playwright_instance:
                self.playwright_instance.stop()
        except Exception as e:
            logger.warning(f"[线程{self.thread_id}] 清理资源时出错: {e}")
        logger.info(f"[线程{self.thread_id}] 测试环境清理完成 ✅")
        
    def create_agent(self, iteration: int) -> tuple:
        """创建数字员工"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        agent_name = f"并行测试_T{self.thread_id}_{iteration}_{timestamp}"
        
        logger.info(f"[线程{self.thread_id}][第{iteration}次] 创建数字员工: {agent_name}")
        
        create_page = CreateAgentPage(self.page)
        create_page.navigate()
        self.page.wait_for_load_state("networkidle")
        
        create_page.fill_name(agent_name)
        create_page.fill_role(f"并行角色_T{self.thread_id}_{iteration}")
        create_page.select_model()
        
        for _ in range(4):  # 点击4次下一步
            create_page.click_next()
            self.page.wait_for_timeout(1000)
        
        create_page.click_complete()
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(3000)
        
        current_url = self.page.url
        if "/agents/" in current_url:
            agent_id = current_url.split("/agents/")[-1].split("?")[0].split("#")[0]
            logger.info(f"[线程{self.thread_id}][第{iteration}次] 数字员工创建成功 ✅ - ID: {agent_id}")
            return agent_name, agent_id
        else:
            raise Exception("创建数字员工后未跳转到详情页")
            
    def execute_conversation_flow(self, iteration: int, agent_id: str):
        """执行对话流程"""
        logger.info(f"[线程{self.thread_id}][第{iteration}次] 执行对话流程...")
        
        agent_detail_page = AgentDetailPage(self.page, agent_id)
        
        agent_detail_page.click_chat_button()
        self.page.wait_for_timeout(1000)
        
        agent_detail_page.click_new_session_button()
        self.page.wait_for_timeout(1000)
        
        agent_detail_page.click_skill_button()
        self.page.wait_for_timeout(1000)
        
        agent_detail_page.select_skill_from_dropdown("cdp_skills")
        self.page.wait_for_timeout(1000)
        
        message = f"搜索最新AI资讯 (线程{self.thread_id})"
        agent_detail_page.type_chat_message(message)
        self.page.wait_for_timeout(500)
        
        agent_detail_page.click_send_button()
        self.page.wait_for_timeout(2000)
        
        logger.info(f"[线程{self.thread_id}][第{iteration}次] 消息已发送，等待5秒...")
        
        time.sleep(5)  # 等待AI响应
        
        logger.info(f"[线程{self.thread_id}][第{iteration}次] 对话流程完成 ✅")
        
    def execute_single_iteration(self, iteration: int) -> ParallelTestResult:
        """执行单次测试"""
        result = ParallelTestResult(self.thread_id, iteration)
        result.start_time = datetime.now()
        
        try:
            print(f"\n[线程{self.thread_id}] {'='*60}")
            print(f"[线程{self.thread_id}] 🔄 开始第 {iteration} 次测试")
            print(f"[线程{self.thread_id}] {'='*60}")
            
            agent_name, agent_id = self.create_agent(iteration)
            
            self.execute_conversation_flow(iteration, agent_id)
            
            result.set_success(agent_name, agent_id)
            print(f"[线程{self.thread_id}] ✅ 第 {iteration} 次测试成功!")
            
        except Exception as e:
            error_msg = str(e)
            result.set_failure(error_msg)
            logger.error(f"[线程{self.thread_id}][第{iteration}次] 测试失败 ❌: {error_msg}")
            print(f"[线程{self.thread_id}] ❌ 第 {iteration} 次测试失败: {error_msg}")
            
            try:
                screenshot_path = f"reports/screenshots/parallel_test_T{self.thread_id}_failure_{iteration}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                self.page.screenshot(path=screenshot_path, full_page=True)
                logger.info(f"[线程{self.thread_id}] 失败截图已保存: {screenshot_path}")
            except:
                pass
                
        result.end_time = datetime.now()
        result.calculate_duration()
        
        return result


def worker_task(thread_id: int, iterations_per_thread: int, config: ConfigReader, 
                statistics: ParallelTestStatistics) -> List[ParallelTestResult]:
    """
    工作线程任务函数
    
    Args:
        thread_id: 线程ID (1, 2, 3)
        iterations_per_thread: 该线程需要执行的迭代次数
        config: 配置对象
        statistics: 共享统计对象
        
    Returns:
        该线程的所有测试结果列表
    """
    worker = ParallelTestWorker(config, thread_id)
    results = []
    
    try:
        worker.setup()
        
        for i in range(1, iterations_per_thread + 1):
            result = worker.execute_single_iteration(i)
            results.append(result)
            statistics.add_result(result)
            
            success_rate = statistics.get_success_rate()
            total_done = len(statistics.results)
            print(f"\n[线程{thread_id}] 📊 进度: {i}/{iterations_per_thread} | "
                  f"总进度: {total_done}/{statistics.total_iterations} | "
                  f"成功率: {success_rate:.2f}%\n")
            
    except Exception as e:
        logger.error(f"[线程{thread_id}] 工作线程发生严重错误: {e}", exc_info=True)
        print(f"\n[线程{thread_id}] ⛔ 工作线程崩溃: {e}\n")
        
    finally:
        worker.teardown()
    
    return results


class ParallelTestExecutor:
    """并行测试执行器"""
    
    def __init__(self, config: ConfigReader, parallel_count: int = 3):
        self.config = config
        self.parallel_count = parallel_count
        
    def run(self, total_iterations: int = 200) -> ParallelTestStatistics:
        """
        运行并行测试
        
        Args:
            total_iterations: 总测试次数
            
        Returns:
            统计信息对象
        """
        statistics = ParallelTestStatistics(total_iterations, self.parallel_count)
        statistics.start_time = datetime.now()
        
        print("\n" + "=" * 80)
        print("🚀 并行循环测试执行器启动")
        print("=" * 80)
        print(f"🔢 并行线程数: {self.parallel_count}")
        print(f"🎯 总测试次数: {total_iterations}")
        print(f"⏰ 启动时间: {statistics.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 计算每个线程的迭代次数
        base_iterations = total_iterations // self.parallel_count
        remainder = total_iterations % self.parallel_count
        
        iterations_list = []
        for i in range(self.parallel_count):
            iterations = base_iterations + (1 if i < remainder else 0)
            iterations_list.append(iterations)
            
        print(f"\n📊 任务分配:")
        for i, iters in enumerate(iterations_list, 1):
            print(f"   线程{i}: {iters} 次")
        
        # 预估时间
        estimated_single_time = 15  # 单次预估时间（秒）
        estimated_total = (total_iterations // self.parallel_count) * estimated_single_time
        estimated_minutes = estimated_total / 60
        
        print(f"\n⏱️ 预估总耗时: ~{estimated_total}秒 ({estimated_minutes:.1f}分钟)")
        print(f"(相比单线程提速约{self.parallel_count}倍)\n")
        print("=" * 80)
        
        try:
            # 使用线程池执行并行任务
            with ThreadPoolExecutor(max_workers=self.parallel_count) as executor:
                futures = {}
                
                for thread_id in range(1, self.parallel_count + 1):
                    future = executor.submit(
                        worker_task,
                        thread_id,
                        iterations_list[thread_id - 1],
                        self.config,
                        statistics
                    )
                    futures[future] = thread_id
                
                # 等待所有线程完成
                for future in as_completed(futures):
                    thread_id = futures[future]
                    try:
                        future.result()  # 获取结果或抛出异常
                    except Exception as e:
                        logger.error(f"线程{thread_id}执行异常: {e}")
                        
        except KeyboardInterrupt:
            print("\n\n⚠️ 用户中断测试执行")
            logger.warning("用户中断测试执行")
            
        except Exception as e:
            print(f"\n\n❌ 测试执行发生严重错误: {str(e)}")
            logger.error(f"测试执行发生严重错误: {str(e)}")
            
        finally:
            statistics.end_time = datetime.now()
            statistics.print_summary()
            self.save_report(statistics)
            
        return statistics
        
    def save_report(self, statistics: ParallelTestStatistics):
        """保存测试报告"""
        report_dir = Path("reports/parallel_test_reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"parallel_test_report_{timestamp}.txt"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("并行循环测试执行报告\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"并行线程数: {statistics.parallel_count}\n")
            f.write(f"执行时间: {statistics.start_time.strftime('%Y-%m-%d %H:%M:%S')} - {statistics.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"总执行次数: {statistics.total_iterations}\n")
            f.write(f"成功次数: {statistics.success_count}\n")
            f.write(f"失败次数: {statistics.failure_count}\n")
            f.write(f"成功率: {statistics.get_success_rate():.2f}%\n")
            f.write(f"平均耗时: {statistics.get_average_duration():.2f} 秒\n\n")
            
            if statistics.start_time and statistics.end_time:
                total_time = (statistics.end_time - statistics.start_time).total_seconds()
                f.write(f"总实际耗时: {total_time:.2f} 秒 ({total_time/60:.2f} 分钟)\n")
                f.write(f"理论单线程耗时: ~{total_time * statistics.parallel_count:.2f} 秒\n")
                f.write(f"加速比: ~{statistics.parallel_count:.2f}x\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("详细结果:\n")
            f.write("=" * 80 + "\n\n")
            
            # 按线程分组显示结果
            from collections import defaultdict
            by_thread = defaultdict(list)
            for result in statistics.results:
                by_thread[result.thread_id].append(result)
            
            for thread_id in sorted(by_thread.keys()):
                f.write(f"【线程{thread_id}】\n")
                for result in by_thread[thread_id]:
                    status = "✅ 成功" if result.success else "❌ 失败"
                    f.write(f"  第{result.iteration}次: {status}\n")
                    if result.success:
                        f.write(f"    数字员工名称: {result.agent_name}\n")
                        f.write(f"    数字员工ID: {result.agent_id}\n")
                    else:
                        f.write(f"    错误信息: {result.error_message}\n")
                    f.write(f"    耗时: {result.duration:.2f} 秒\n\n")
                    
        print(f"\n📄 测试报告已保存: {report_file}")
        logger.info(f"测试报告已保存: {report_file}")


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🔄 并行循环测试执行脚本")
    print("   特点：同时打开3个浏览器窗口并行执行测试")
    print("=" * 80)
    
    total_iterations = 200
    parallel_count = 3  # 默认3个并行
    
    # 解析命令行参数
    if len(sys.argv) > 1:
        try:
            total_iterations = int(sys.argv[1])
        except ValueError:
            print(f"⚠️ 无效的总次数参数，使用默认值: {total_iterations}")
    
    if len(sys.argv) > 2:
        try:
            parallel_count = int(sys.argv[2])
            if not (1 <= parallel_count <= 10):
                raise ValueError("并行数必须在1-10之间")
        except ValueError as e:
            print(f"⚠️ 无效的并行数参数: {e}，使用默认值: {parallel_count}")
    
    print(f"\n配置信息:")
    print(f"  📌 总测试次数: {total_iterations}")
    print(f"  🔢 并行线程数: {parallel_count}")
    print(f"  📊 每线程约: {total_iterations // parallel_count} 次")
    print(f"{'='*80}\n")
    
    config = ConfigReader()
    executor = ParallelTestExecutor(config, parallel_count)
    
    statistics = executor.run(total_iterations)
    
    if statistics.success_count == statistics.total_iterations:
        print("\n🎉 所有测试全部通过!")
        sys.exit(0)
    else:
        print(f"\n⚠️ 有 {statistics.failure_count} 次测试失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
