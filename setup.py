#!/usr/bin/env python3
"""
项目安装和初始化脚本
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def run_command(cmd, check=True):
    """执行命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    if result.stderr and check:
        print(f"错误: {result.stderr}")
    
    if check and result.returncode != 0:
        print(f"命令执行失败: {cmd}")
        sys.exit(1)
    
    return result.returncode == 0

def install_dependencies():
    """安装依赖包"""
    print("🔧 安装Python依赖包...")
    
    # 升级pip
    run_command(f"{sys.executable} -m pip install --upgrade pip")
    
    # 安装依赖
    run_command(f"{sys.executable} -m pip install -r requirements.txt")
    
    print("✅ Python依赖包安装完成")

def install_browsers():
    """安装浏览器"""
    print("🌐 安装Playwright浏览器...")
    
    run_command("playwright install")
    run_command("playwright install-deps", check=False)  # 系统依赖可能失败，不强制检查
    
    print("✅ 浏览器安装完成")

def create_env_file():
    """创建环境变量文件"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_example.exists() and not env_file.exists():
        print("📝 创建环境变量文件...")
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ 已创建 .env 文件，请根据需要修改配置")
    elif env_file.exists():
        print("ℹ️  .env 文件已存在")
    else:
        print("⚠️  未找到 .env.example 文件")

def create_directories():
    """创建必要的目录"""
    print("📁 创建项目目录...")
    
    directories = [
        "reports",
        "reports/screenshots",
        "reports/videos",
        "reports/allure-results",
        "logs",
        "test_data",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ 项目目录创建完成")

def check_python_version():
    """检查Python版本"""
    print("🐍 检查Python版本...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ 需要Python 3.8或更高版本")
        sys.exit(1)
    
    print(f"✅ Python版本: {version.major}.{version.minor}.{version.micro}")

def setup_project():
    """项目初始化"""
    print("🚀 开始初始化Python + Playwright自动化测试框架...")
    print("=" * 60)
    
    # 检查Python版本
    check_python_version()
    
    # 创建目录
    create_directories()
    
    # 安装依赖
    install_dependencies()
    
    # 安装浏览器
    install_browsers()
    
    # 创建环境文件
    create_env_file()
    
    print("=" * 60)
    print("🎉 项目初始化完成！")
    print()
    print("📚 快速开始:")
    print("   1. 修改 .env 文件中的配置")
    print("   2. 运行示例测试: pytest tests/test_login.py")
    print("   3. 生成HTML报告: pytest --html=reports/report.html")
    print("   4. 使用运行脚本: python run_tests.py --help")
    print()
    print("📖 更多信息请查看 README.md")

if __name__ == "__main__":
    try:
        setup_project()
    except KeyboardInterrupt:
        print("\n❌ 安装被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 安装过程中出现错误: {e}")
        sys.exit(1) 