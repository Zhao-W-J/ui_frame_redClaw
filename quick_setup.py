#!/usr/bin/env python3
"""
快速安装脚本 - 简化版本
"""
import subprocess
import sys
import os

def install_packages():
    """安装Python包"""
    print("🔧 安装依赖包...")
    packages = [
        "playwright==1.40.0",
        "pytest==7.4.3", 
        "pytest-playwright==0.4.3",
        "pytest-html==4.1.1",
        "python-dotenv==1.0.0",
        "pyyaml==6.0.1",
        "openpyxl==3.1.2"
    ]
    
    for package in packages:
        try:
            print(f"安装 {package}...")
            result = subprocess.run([sys.executable, "-m", "pip", "install", package], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {package} 安装成功")
            else:
                print(f"⚠️  {package} 安装可能有问题")
        except Exception as e:
            print(f"❌ 安装 {package} 时出错: {e}")

def install_browsers():
    """安装浏览器"""
    print("\n🌐 安装浏览器...")
    try:
        result = subprocess.run(["playwright", "install"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ 浏览器安装成功")
        else:
            print("⚠️  浏览器安装可能有问题，请手动运行: playwright install")
    except Exception as e:
        print(f"❌ 浏览器安装失败: {e}")
        print("请手动运行: playwright install")

def create_env_file():
    """创建环境文件"""
    print("\n📝 创建 .env 文件...")
    env_content = """# 环境变量配置
BASE_URL=https://example.com
TEST_ENV=dev
BROWSER_HEADLESS=false
BROWSER_SLOW_MO=100
BROWSER_TIMEOUT=30000
"""
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ .env 文件创建成功")
    except Exception as e:
        print(f"❌ 创建 .env 文件失败: {e}")

if __name__ == "__main__":
    print("🚀 快速初始化 Python + Playwright 自动化测试框架")
    print("=" * 50)
    
    install_packages()
    install_browsers() 
    create_env_file()
    
    print("\n" + "=" * 50)
    print("🎉 初始化完成!")
    print("\n📚 下一步:")
    print("1. 运行测试验证: python -m pytest tests/test_login.py -v")
    print("2. 查看帮助: python run_tests.py --help")
    print("3. 阅读文档: README.md") 