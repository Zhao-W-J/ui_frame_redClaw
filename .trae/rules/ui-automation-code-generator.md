---
alwaysApply: false
---
# UI自动化代码生成规则

## 规则概述
基于 @doc/test-case.md 中的测试计划，自动生成完整的UI自动化测试代码，包括页面对象、测试用例和测试数据。

## 触发条件
- 用户要求"生成自动化代码"
- 用户提到"实现测试用例"
- 用户上传或引用测试计划文档
- 存在 @doc/test-case.md 文件

## 代码生成规范

### 1. 页面对象生成
基于 @pages/base_page.py 模板：

```python
from playwright.sync_api import Page
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger(__name__)

class [PageName]Page(BasePage):
    """[页面描述]页面对象"""
    
    # 页面元素定位器
    [ELEMENT_NAME]_INPUT = "[selector]"
    [BUTTON_NAME]_BUTTON = "[selector]"
    
    # 页面加载指示器
    page_loaded_indicator = "[main_element_selector]"
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.page_url = f"{self.base_url}/[page_path]"
    
    def navigate(self) -> None:
        """导航到[页面名称]页面"""
        logger.info(f"导航到[页面名称]页面: {self.page_url}")
        self.page.goto(self.page_url)
        self.wait_for_page_load()
    
    def is_loaded(self) -> bool:
        """检查页面是否加载完成"""
        return self.is_element_visible(self.page_loaded_indicator)
    
    # 业务操作方法
    def @action_method:
        """[操作描述]"""
        logger.info(f"执行[操作描述]: {param1}")
        # 实现具体操作
        pass
```

### 2. 测试用例生成
基于 @tests/test_demo.py 模板：

```python
import pytest
from playwright.sync_api import Page
from pages.[page_name]_page import [PageName]Page
from utils.data_manager import DataManager
from utils.logger import get_logger

logger = get_logger(__name__)

class Test[PageName]:
    """[页面名称]功能测试类"""
    
    @pytest.fixture(autouse=True)
    def setup(self, page: Page):
        """测试前置设置"""
        self.page = page
        self.[page_name]_page = [PageName]Page(page)
        self.test_data = DataManager.get_test_data("[data_file]", "[test_case]")
    
    @pytest.mark.smoke
    @pytest.mark.ui
    def test_@test_case_name:
        """[测试用例描述]"""
        logger.info("开始测试[测试用例描述]")
        
        # 测试步骤实现
        self.[page_name]_page.navigate()
        assert self.[page_name]_page.is_loaded(), "页面未正确加载"
        
        # 更多测试步骤...
        
        logger.info("[测试用例描述]测试通过")
    
    @pytest.mark.parametrize("test_data", [
        {"field1": "value1", "field2": "value2"},
        {"field1": "value3", "field2": "value4"},
    ])
    def test_[test_case_name]_with_data(self, test_data):
        """数据驱动测试"""
        logger.info(f"使用数据执行测试: {test_data}")
        # 实现数据驱动测试逻辑
        pass
```

### 3. 测试数据生成
基于 @test_data/login_data.json 格式：

```json
{
  "[test_case_group]": [
    {
      "test_case": "[test_name]",
      "description": "[测试描述]",
      "data": {
        "field1": "valid_value1",
        "field2": "valid_value2"
      },
      "expected_result": "success"
    }
  ],
  "boundary_data": [
    {
      "test_case": "boundary_test",
      "data": {
        "field1": "",
        "field2": "max_length_string"
      },
      "expected_result": "validation_error"
    }
  ],
  "invalid_data": [
    {
      "test_case": "invalid_input",
      "data": {
        "field1": "invalid_format",
        "field2": null
      },
      "expected_result": "error"
    }
  ]
}
```

## 生成流程

### 1. 分析测试计划
从 @doc/test-case.md 提取：
- 页面基本信息
- 元素定位器列表
- 测试用例列表
- 测试数据结构

### 2. 生成页面对象
- 解析页面元素映射表
- 生成元素定位器常量
- 实现基础页面操作方法
- 添加业务逻辑封装

### 3. 生成测试用例
- 为每个测试场景创建测试方法
- 添加适当的pytest标记
- 实现断言和验证逻辑
- 集成数据驱动测试

### 4. 生成测试数据
- 创建有效数据集
- 创建边界数据集
- 创建异常数据集
- 按测试用例分组

### 5. 更新配置文件
更新 @config/test_config.yaml：
```yaml
# 新增页面配置
pages:
  [page_name]:
    url: "/[page_path]"
    timeout: 30000
    elements:
      load_indicator: "[selector]"

# 新增测试数据配置  
test_data:
  [page_name]:
    data_file: "[page_name]_data.json"
    test_cases:
      - "[test_case1]"
      - "[test_case2]"
```

## 文件组织规范

### 页面对象文件
- 文件名：`pages/[page_name]_page.py`
- 类名：`[PageName]Page`
- 继承：`BasePage`

### 测试用例文件
- 文件名：`tests/test_[page_name].py`
- 类名：`Test[PageName]`
- 方法命名：`test_[功能]_[场景]`

### 测试数据文件
- 文件名：`test_data/[page_name]_data.json`
- 格式：JSON
- 结构：按测试类型分组

### 辅助文件
- 如需要，生成页面专用的工具类
- 更新 @conftest.py 中的fixture
- 添加页面专用的配置

## 质量保证

### 1. 代码规范
- 遵循PEP 8编码规范
- 使用类型提示
- 添加完整的文档字符串
- 合理的异常处理

### 2. 测试覆盖
- 确保所有关键路径覆盖
- 包含正向和负向测试
- 添加边界条件测试
- 考虑并发和性能测试

### 3. 可维护性
- 清晰的命名约定
- 合理的代码注释
- 模块化设计
- 易于扩展和修改

## 集成指南

### 1. 框架集成
- 利用现有的 @utils/ 工具类
- 遵循 @conftest.py 中的配置
- 使用统一的日志和报告系统

### 2. 执行验证
生成代码后执行以下验证：
```bash
# 语法检查
python -m py_compile pages/[page_name]_page.py
python -m py_compile tests/test_[page_name].py

# 运行测试
python run_tests.py --tests tests/test_[page_name].py --verbose

# 生成报告
python run_tests.py --tests tests/test_[page_name].py --html-report
```

### 3. 文档更新
- 更新 @README.md 中的使用说明
- 在 @使用指南.md 中添加新页面的使用方法
- 更新项目文档中的测试覆盖情况

## 输出要求
1. 生成完整的页面对象文件
2. 生成对应的测试用例文件
3. 生成测试数据文件
4. 更新相关配置文件
5. 提供执行和验证建议
6. 生成代码使用说明
