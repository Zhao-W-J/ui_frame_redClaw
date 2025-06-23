# Python + Playwright 自动化 UI 测试框架

这是一个基于 Python 和 Playwright 的现代化 UI 自动化测试框架，采用页面对象模式(POM)设计，提供了完整的测试基础设施。

## 🚀 特性

- **现代化技术栈**: 基于 Playwright 的稳定、快速的浏览器自动化
- **页面对象模式**: 清晰的代码结构，易于维护
- **多浏览器支持**: 支持 Chromium、Firefox、WebKit
- **丰富的报告**: HTML 报告、Allure 报告、视频录制、截图
- **数据驱动测试**: 支持 JSON、YAML、CSV、Excel 等多种数据格式
- **并行执行**: 支持多进程并行测试执行
- **灵活配置**: 环境变量和配置文件双重配置支持
- **完善的日志**: 分级日志记录，便于调试

## 📦 项目结构

```
ui_frame/
├── pages/                 # 页面对象
│   ├── __init__.py
│   ├── base_page.py      # 基础页面类
│   └── login_page.py     # 登录页面示例
├── tests/                # 测试用例
│   ├── __init__.py
│   └── test_login.py     # 登录测试示例
├── utils/                # 工具类
│   ├── __init__.py
│   ├── logger.py         # 日志工具
│   ├── config_reader.py  # 配置读取
│   ├── page_utils.py     # 页面操作工具
│   └── data_manager.py   # 数据管理
├── config/               # 配置文件
│   └── test_config.yaml  # 测试配置
├── test_data/           # 测试数据
│   └── login_data.json   # 登录测试数据
├── reports/             # 测试报告（自动生成）
├── logs/               # 日志文件（自动生成）
├── conftest.py         # pytest全局配置
├── playwright.config.py # Playwright配置
├── pytest.ini          # pytest配置
├── requirements.txt     # 依赖包
├── .env.example        # 环境变量示例
└── README.md           # 项目说明
```

## 🛠️ 安装和设置

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd ui_frame
```

### 2. 创建虚拟环境

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install -r requirements.txt
```

### 4. 安装浏览器

```bash
playwright install
```

### 5. 配置环境变量

```bash
cp .env.example .env
# 根据实际环境修改 .env 文件中的配置
```

## 🎯 快速开始

### 运行示例测试

```bash
# 运行所有测试
pytest

# 运行指定测试文件
pytest tests/test_login.py

# 运行指定标记的测试
pytest -m smoke

# 并行运行测试
pytest -n 2
```

### 生成测试报告

```bash
# 生成HTML报告
pytest --html=reports/report.html

# 生成Allure报告
pytest --alluredir=reports/allure-results
allure serve reports/allure-results
```

## 📝 编写测试用例

### 1. 创建页面对象

```python
from pages.base_page import BasePage
from playwright.sync_api import Page

class YourPage(BasePage):
    # 定义页面元素
    ELEMENT_SELECTOR = "#your-element"

    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = f"{self.base_url}/your-page"

    def navigate(self):
        self.page.goto(self.page_url)
        self.wait_for_page_load()

    def is_loaded(self) -> bool:
        return self.is_element_visible(self.ELEMENT_SELECTOR)

    def your_action(self):
        # 实现页面操作
        pass
```

### 2. 创建测试用例

```python
import pytest
from pages.your_page import YourPage

class TestYourFeature:
    @pytest.fixture(autouse=True)
    def setup(self, page):
        self.page = page
        self.your_page = YourPage(page)

    @pytest.mark.smoke
    def test_your_feature(self):
        self.your_page.navigate()
        assert self.your_page.is_loaded()
        # 执行测试步骤
```

## ⚙️ 配置说明

### 环境变量配置

在 `.env` 文件中配置：

- `BASE_URL`: 测试基础 URL
- `BROWSER_HEADLESS`: 是否无头模式
- `BROWSER_TIMEOUT`: 浏览器超时时间

### 测试配置

在 `config/test_config.yaml` 中配置：

- 测试环境设置
- 浏览器配置
- 报告配置

## 🏷️ 测试标记

- `@pytest.mark.smoke`: 冒烟测试
- `@pytest.mark.regression`: 回归测试
- `@pytest.mark.critical`: 关键功能测试
- `@pytest.mark.ui`: UI 界面测试
- `@pytest.mark.api`: API 接口测试
- `@pytest.mark.slow`: 慢速测试

## 📊 测试数据管理

### 支持的数据格式

- JSON: `test_data/login_data.json`
- YAML: `test_data/user_data.yaml`
- CSV: `test_data/product_data.csv`
- Excel: `test_data/test_data.xlsx`

### 使用数据驱动测试

```python
from utils.data_manager import DataManager

# 加载测试数据
test_data = DataManager.get_test_data("login_data.json", "login_test")

# 参数化测试
@pytest.mark.parametrize("data", test_data)
def test_with_data(self, data):
    # 使用数据执行测试
    pass
```

## 🔧 高级功能

### 自定义断言

```python
# 断言元素可见
self.page.assert_element_visible("#element")

# 断言文本内容
self.page.assert_element_text("#element", "Expected Text")

# 断言页面URL
self.page.assert_page_url("https://example.com/page")
```

### 截图和录制

- 失败时自动截图
- 视频录制功能
- 自定义截图 `self.page.take_screenshot("custom_name.png")`

### 并行执行

```bash
# 使用pytest-xdist并行执行
pytest -n auto  # 自动检测CPU核心数
pytest -n 4     # 指定并行进程数
```

## 🐛 调试技巧

### 调试模式

```bash
# 开启调试模式
pytest --headed --slowmo=1000

# 显示浏览器
pytest --browser chromium --headed

# 详细日志
pytest -v -s
```

### 暂停调试

```python
# 在代码中添加暂停点
page.pause()
```

## 📈 最佳实践

1. **页面对象模式**: 将页面元素和操作封装在页面类中
2. **数据驱动**: 使用外部数据文件管理测试数据
3. **标记分类**: 合理使用 pytest 标记对测试进行分类
4. **等待策略**: 使用显式等待而非固定延时
5. **断言清晰**: 提供清晰的断言错误信息
6. **日志记录**: 在关键步骤添加日志记录

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 创建 Pull Request

## 📄 许可证

MIT License

## 📞 联系方式

如有问题或建议，请提交 Issue 或联系项目维护者。
