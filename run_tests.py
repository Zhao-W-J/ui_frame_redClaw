#!/usr/bin/env python3
"""
测试执行脚本
提供便捷的测试执行方式和参数配置
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

def run_command(cmd):
    """执行命令并实时输出结果"""
    print(f"执行命令: {cmd}")
    process = subprocess.Popen(
        cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        encoding='utf-8'
    )
    
    # 实时输出
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    return process.poll()

def main():
    parser = argparse.ArgumentParser(description='Playwright测试执行脚本')
    
    # 基本参数
    parser.add_argument('--browser', choices=['chromium', 'firefox', 'webkit'], 
                       default='chromium', help='指定浏览器类型')
    parser.add_argument('--headless', action='store_true', 
                       help='无头模式运行')
    parser.add_argument('--headed', action='store_true', 
                       help='有头模式运行(显示浏览器)')
    
    # 测试选择
    parser.add_argument('--tests', type=str, 
                       help='指定测试文件或测试用例')
    parser.add_argument('--markers', type=str, 
                       help='指定测试标记 (如: smoke, regression)')
    parser.add_argument('--keywords', type=str, 
                       help='根据关键字过滤测试')
    
    # 执行控制
    parser.add_argument('--parallel', '-n', type=int, 
                       help='并行执行进程数')
    parser.add_argument('--maxfail', type=int, default=0,
                       help='最大失败数，达到后停止执行')
    parser.add_argument('--reruns', type=int, default=0,
                       help='失败重试次数')
    
    # 报告和调试
    parser.add_argument('--html-report', action='store_true',
                       help='生成HTML报告')
    parser.add_argument('--allure', action='store_true',
                       help='生成Allure报告')
    parser.add_argument('--video', action='store_true',
                       help='录制视频')
    parser.add_argument('--screenshot', action='store_true',
                       help='失败时截图')
    parser.add_argument('--slowmo', type=int, default=0,
                       help='操作间隔时间(毫秒)')
    parser.add_argument('--debug', action='store_true',
                       help='调试模式')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='详细输出')
    
    # 环境配置
    parser.add_argument('--env', type=str, default='dev',
                       help='测试环境 (dev, test, prod)')
    parser.add_argument('--base-url', type=str,
                       help='基础URL')
    
    args = parser.parse_args()
    
    # 构建pytest命令
    cmd_parts = ['pytest']
    
    # 添加测试文件或标记
    if args.tests:
        cmd_parts.append(args.tests)
    
    if args.markers:
        cmd_parts.extend(['-m', args.markers])
    
    if args.keywords:
        cmd_parts.extend(['-k', args.keywords])
    
    # 添加浏览器配置
    cmd_parts.extend(['--browser', args.browser])
    
    if args.headless:
        cmd_parts.append('--headless')
    elif args.headed:
        cmd_parts.append('--headed')
    
    if args.slowmo > 0:
        cmd_parts.extend(['--slowmo', str(args.slowmo)])
    
    # 添加并行执行
    if args.parallel:
        cmd_parts.extend(['-n', str(args.parallel)])
    
    # 添加失败控制
    if args.maxfail > 0:
        cmd_parts.extend(['--maxfail', str(args.maxfail)])
    
    if args.reruns > 0:
        cmd_parts.extend(['--reruns', str(args.reruns)])
    
    # 添加报告配置
    if args.html_report:
        cmd_parts.extend(['--html', 'reports/report.html', '--self-contained-html'])
    
    if args.allure:
        cmd_parts.extend(['--alluredir', 'reports/allure-results'])
    
    if args.video:
        cmd_parts.append('--video=on')
    
    if args.screenshot:
        cmd_parts.append('--screenshot=only-on-failure')
    
    # 添加调试和详细输出
    if args.debug:
        cmd_parts.extend(['-s', '--tb=short'])
    
    if args.verbose:
        cmd_parts.append('-v')
    
    # 设置环境变量
    env = os.environ.copy()
    if args.env:
        env['TEST_ENV'] = args.env
    if args.base_url:
        env['BASE_URL'] = args.base_url
    
    # 确保必要的目录存在
    Path('reports').mkdir(exist_ok=True)
    Path('logs').mkdir(exist_ok=True)
    
    # 执行命令
    cmd = ' '.join(cmd_parts)
    print(f"开始执行测试...")
    print(f"环境: {args.env}")
    print(f"浏览器: {args.browser}")
    print(f"命令: {cmd}")
    print("-" * 50)
    
    # 设置环境变量并执行
    old_env = os.environ
    os.environ.update(env)
    
    try:
        exit_code = run_command(cmd)
    finally:
        os.environ = old_env
    
    print("-" * 50)
    if exit_code == 0:
        print("✅ 测试执行完成")
        
        # 如果生成了Allure报告，提示查看
        if args.allure and Path('reports/allure-results').exists():
            print("📊 生成Allure报告命令:")
            print("   allure serve reports/allure-results")
            
        if args.html_report and Path('reports/report.html').exists():
            print("📊 HTML报告已生成: reports/report.html")
            
    else:
        print(f"❌ 测试执行失败，退出码: {exit_code}")
    
    return exit_code

if __name__ == '__main__':
    sys.exit(main()) 