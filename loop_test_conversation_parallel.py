"""
并行循环测试脚本 - 多进程版本（真·并行）
功能：同时启动多个进程，每个进程独立运行完整测试流程
特点：绕过Python GIL限制，实现真正的并行执行
"""

import sys
import os
import time
import multiprocessing
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from multiprocessing import Process, Queue, Value

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 必须在主进程导入配置模块
from utils.config_reader import ConfigReader


class ParallelTestResult:
    """单次并行测试结果"""
    def __init__(self, process_id: int, iteration: int):
        self.process_id = process_id
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

    def to_dict(self) -> dict:
        return {
            "process_id": self.process_id,
            "iteration": self.iteration,
            "success": self.success,
            "error_message": self.error_message,
            "agent_name": self.agent_name,
            "agent_id": self.agent_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration": self.duration
        }


def worker_process(process_id: int, iterations: int, result_queue: Queue, 
                   counter: Value, total_iterations: int):
    """
    工作进程函数 - 每个进程完全独立运行
    
    Args:
        process_id: 进程ID (1, 2, 3)
        iterations: 该进程需要执行的迭代次数
        result_queue: 结果队列（用于收集结果）
        counter: 共享计数器
        total_iterations: 总迭代次数
    """
    # 每个进程重新导入（避免多进程导入问题）
    from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
    from utils.logger import get_logger
    from pages.login_page import LoginPage
    from pages.create_agent_page import CreateAgentPage
    from pages.agent_detail_page import AgentDetailPage
    
    # 设置进程级日志
    logger = get_logger(f"Process-{process_id}")
    
    try:
        logger.info(f"[进程{process_id}] 🚀 启动工作进程")
        
        # ========== 初始化该进程的浏览器 ==========
        logger.info(f"[进程{process_id}] 初始化浏览器环境...")
        
        pw = sync_playwright().start()
        
        browser = pw.chromium.launch(
            headless=False,
            slow_mo=200,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-extensions",
                "--no-sandbox",
                f"--window-position={(process_id-1) * 450},0",  # 窗口位置错开
            ]
        )
        
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            ignore_https_errors=True,
            user_agent=f"ParallelWorker-P{process_id}",
        )
        
        page = context.new_page()
        page.set_default_timeout(30000)
        page.set_default_navigation_timeout(30000)
        
        # ========== 登录 ==========
        config = ConfigReader()
        base_url = config.get("test.base_url", "http://10.11.150.76:10088")
        username = config.get("test_data.users.admin.username", "admin")
        password = config.get("test_data.users.admin.password", "123456")
        
        logger.info(f"[进程{process_id}] 执行登录...")
        login_page = LoginPage(page)
        login_page.navigate()
        login_page.login(username, password)
        page.wait_for_load_state("networkidle")
        logger.info(f"[进程{process_id}] ✅ 登录成功")
        
        # ========== 执行循环测试 ==========
        for i in range(1, iterations + 1):
            result = ParallelTestResult(process_id, i)
            result.start_time = datetime.now()
            
            try:
                print(f"\n[进程{process_id}] {'='*60}")
                print(f"[进程{process_id}] 🔄 执行第 {i}/{iterations} 次")
                print(f"[进程{process_id}] {'='*60}")
                
                # 创建数字员工
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
                agent_name = f"并行P{process_id}_{i}_{timestamp}"
                
                logger.info(f"[进程{process_id}][第{i}次] 创建: {agent_name}")
                
                create_page = CreateAgentPage(page)
                create_page.navigate()
                page.wait_for_load_state("networkidle")
                
                create_page.fill_name(agent_name)
                create_page.fill_role(f"P{process_id}_角色_{i}")
                create_page.select_model()
                
                for _ in range(4):  # 4次下一步
                    create_page.click_next()
                    page.wait_for_timeout(800)
                
                create_page.click_complete()
                page.wait_for_load_state("networkidle")
                page.wait_for_timeout(2500)
                
                current_url = page.url
                if "/agents/" in current_url:
                    agent_id = current_url.split("/agents/")[-1].split("?")[0].split("#")[0]
                    logger.info(f"[进程{process_id}] ✅ 创建成功 ID:{agent_id}")
                    
                    # 对话流程
                    agent_detail = AgentDetailPage(page, agent_id)
                    agent_detail.click_chat_button()
                    page.wait_for_timeout(800)
                    
                    agent_detail.click_new_session_button()
                    page.wait_for_timeout(800)
                    
                    agent_detail.click_skill_button()
                    page.wait_for_timeout(800)
                    
                    agent_detail.select_skill_from_dropdown("cdp_skills")
                    page.wait_for_timeout(800)
                    
                    agent_detail.type_chat_message(f"搜索AI资讯(P{process_id})")
                    page.wait_for_timeout(500)
                    
                    agent_detail.click_send_button()
                    page.wait_for_timeout(1500)
                    
                    print(f"[进程{process_id}] ⏳ 等待5秒...")
                    time.sleep(5)
                    
                    result.set_success(agent_name, agent_id)
                    print(f"[进程{process_id}] ✅ 第{i}次完成!")
                    
                else:
                    raise Exception("未跳转到详情页")
                    
            except Exception as e:
                error_msg = str(e)
                result.set_failure(error_msg)
                logger.error(f"[进程{process_id}] ❌ 第{i}次失败: {error_msg}")
                print(f"[进程{process_id}] ❌ 第{i}次失败: {error_msg}")
                
                try:
                    screenshot_path = f"reports/screenshots/multi_P{process_id}_{i}_{int(time.time())}.png"
                    os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                    page.screenshot(path=screenshot_path, full_page=True)
                except:
                    pass
            
            finally:
                result.end_time = datetime.now()
                result.calculate_duration()
                
                # 将结果放入队列
                result_queue.put(result.to_dict())
                
                # 更新全局计数器
                with counter.get_lock():
                    counter.value += 1
                
                current_total = counter.value
                print(f"\n[进程{process_id}] 📊 当前进度: {i}/{iterations} | "
                      f"总进度: {current_total}/{total_iterations}\n")
        
        # 清理资源
        logger.info(f"[进程{process_id}] 清理资源...")
        page.close()
        context.close()
        browser.close()
        pw.stop()
        logger.info(f"[进程{process_id}] ✅ 进程正常结束")
        
    except Exception as e:
        logger.error(f"[进程{process_id}] ⛔ 进程崩溃: {e}", exc_info=True)
        print(f"\n[进程{process_id}] ⛔ 进程异常退出: {e}\n")


class ParallelTestExecutor:
    """并行测试执行器（多进程版）"""
    
    def __init__(self, parallel_count: int = 3):
        self.parallel_count = parallel_count
        
    def run(self, total_iterations: int = 200):
        """
        运行并行测试
        
        Args:
            total_iterations: 总测试次数
            
        Returns:
            统计信息字典
        """
        start_time = datetime.now()
        
        print("\n" + "=" * 80)
        print("🚀 并行循环测试执行器 (多进程·真并行)")
        print("=" * 80)
        print(f"⚡ 并行进程数: {self.parallel_count} (真正的并行!)")
        print(f"🎯 总测试次数: {total_iterations}")
        print(f"⏰ 启动时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 任务分配
        base_iters = total_iterations // self.parallel_count
        remainder = total_iterations % self.parallel_count
        iterations_list = []
        
        for i in range(self.parallel_count):
            iters = base_iters + (1 if i < remainder else 0)
            iterations_list.append(iters)
            
        print(f"\n📊 任务分配:")
        for pid, iters in enumerate(iterations_list, 1):
            print(f"   进程{pid}: {iters} 次")
        
        # 预估时间（相比单线程快N倍）
        estimated_seconds = (base_iters * 15)  # 单次约15秒
        print(f"\n⏱️ 预估总耗时: ~{estimated_seconds}秒 ({estimated_seconds/60:.1f}分钟)")
        print(f"(加速比约: ~{self.parallel_count}x)\n")
        print("=" * 80)
        
        # 创建共享对象
        result_queue = multiprocessing.Queue()
        counter = Value('i', 0)  # 共享计数器
        
        # 启动多个进程
        processes = []
        print(f"\n🚀 正在启动 {self.parallel_count} 个并行进程...\n")
        
        for proc_id in range(1, self.parallel_count + 1):
            p = Process(
                target=worker_process,
                args=(proc_id, iterations_list[proc_id-1], result_queue, counter, total_iterations),
                name=f"Worker-Process-{proc_id}"
            )
            p.start()
            processes.append(p)
            print(f"   ✅ 进程{proc_id} 已启动 (PID: {p.pid})")
            time.sleep(1)  # 错开启动时间
        
        print(f"\n{'='*80}")
        print(f"✨ 所有 {self.parallel_count} 个进程已启动，开始并行执行...")
        print(f"{'='*80}\n")
        
        # 等待所有进程完成
        try:
            for p in processes:
                p.join(timeout=3600)  # 最长等1小时
                
        except KeyboardInterrupt:
            print("\n\n⚠️ 用户中断，正在终止所有进程...")
            for p in processes:
                p.terminate()
                p.join(timeout=5)
        
        # 收集结果
        results = []
        while not result_queue.empty():
            try:
                results.append(result_queue.get_nowait())
            except:
                break
        
        end_time = datetime.now()
        
        # 统计信息
        success_count = sum(1 for r in results if r["success"])
        fail_count = len(results) - success_count
        
        # 打印报告
        self._print_report(start_time, end_time, total_iterations, 
                          success_count, fail_count, results)
        
        # 保存报告
        self._save_report(start_time, end_time, total_iterations,
                         success_count, fail_count, results)
        
        return {
            "success": success_count == total_iterations,
            "success_count": success_count,
            "fail_count": fail_count,
            "results": results
        }
    
    def _print_report(self, start_time, end_time, total, success, fail, results):
        """打印统计报告"""
        total_time = (end_time - start_time).total_seconds()
        success_rate = (success / total * 100) if total > 0 else 0
        
        print(f"\n{'='*80}")
        print("📊 并行测试最终报告")
        print(f"{'='*80}")
        print(f"并行进程数: {self.parallel_count}")
        print(f"总执行次数: {total}")
        print(f"成功次数: {success} ✅")
        print(f"失败次数: {fail} ❌")
        print(f"成功率: {success_rate:.2f}%")
        print(f"实际耗时: {total_time:.2f}秒 ({total_time/60:.2f}分钟)")
        
        if total > 0 and self.parallel_count > 0:
            speedup = (total_time * self.parallel_count) / total_time
            print(f"⚡ 加速比: ~{speedup:.2f}x")
        
        print(f"{'='*80}")
        
        if fail > 0:
            print("\n❌ 失败详情:")
            for r in sorted(results, key=lambda x: (x['process_id'], x['iteration'])):
                if not r['success']:
                    print(f"  [进程{r['process_id']}] 第{r['iteration']}次: {r['error_message'][:50]}")
    
    def _save_report(self, start_time, end_time, total, success, fail, results):
        """保存详细报告"""
        report_dir = Path("reports/parallel_test_reports")
        report_dir.mkdir(parents=True, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = report_dir / f"parallel_test_report_{timestamp}.txt"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("=" * 80 + "\n")
            f.write("并行测试报告 (多进程版)\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"并行进程数: {self.parallel_count}\n")
            f.write(f"时间范围: {start_time} ~ {end_time}\n")
            f.write(f"总次数: {total} | 成功: {success} | 失败: {fail}\n")
            f.write(f"成功率: {(success/total*100):.2f}%\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("详细结果:\n")
            f.write("=" * 80 + "\n\n")
            
            from collections import defaultdict
            by_process = defaultdict(list)
            for r in results:
                by_process[r['process_id']].append(r)
            
            for pid in sorted(by_process.keys()):
                f.write(f"【进程{pid}】\n")
                for r in sorted(by_process[pid], key=lambda x: x['iteration']):
                    status = "✅" if r['success'] else "❌"
                    f.write(f"  第{r['iteration']:3d}次 {status} ")
                    if r['success']:
                        f.write(f"| 名称: {r['agent_name'][:30]} | 耗时: {r['duration']:.1f}s\n")
                    else:
                        f.write(f"| 错误: {r['error_message'][:60]}\n")
                f.write("\n")
        
        print(f"\n📄 报告已保存: {report_file}")


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("🔄 并行循环测试脚本 (多进程·真并行)")
    print("   特点: 绕过GIL限制，真正的并行处理!")
    print("=" * 80)
    
    total_iterations = 200
    parallel_count = 3
    
    # 解析参数
    if len(sys.argv) > 1:
        try:
            total_iterations = int(sys.argv[1])
        except ValueError:
            pass
    
    if len(sys.argv) > 2:
        try:
            parallel_count = int(sys.argv[2])
            parallel_count = max(1, min(parallel_count, 10))  # 限制1-10
        except ValueError:
            pass
    
    print(f"\n配置:")
    print(f"  📌 总次数: {total_iterations}")
    print(f"  🔢 进程数: {parallel_count}")
    print(f"{'='*80}\n")
    
    executor = ParallelTestExecutor(parallel_count)
    result = executor.run(total_iterations)
    
    if result['success']:
        print("\n🎉 全部通过!")
        sys.exit(0)
    else:
        print(f"\n⚠️ 有 {result['fail_count']} 次失败")
        sys.exit(1)


if __name__ == "__main__":
    main()
