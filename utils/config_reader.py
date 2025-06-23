import json
import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class ConfigReader:
    """配置文件读取器"""
    
    def __init__(self, config_file: str = "config/test_config.yaml"):
        """
        初始化配置读取器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self._config_data = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        config_path = Path(self.config_file)
        
        if not config_path.exists():
            return {}
        
        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                if config_path.suffix.lower() in ['.yaml', '.yml']:
                    return yaml.safe_load(file) or {}
                elif config_path.suffix.lower() == '.json':
                    return json.load(file) or {}
                else:
                    return {}
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值
        
        Args:
            key: 配置键，支持点号分隔的嵌套键
            default: 默认值
            
        Returns:
            配置值
        """
        # 首先尝试从环境变量获取
        env_key = key.upper().replace('.', '_')
        env_value = os.getenv(env_key)
        if env_value is not None:
            return self._convert_value(env_value)
        
        # 从配置文件获取
        keys = key.split('.')
        value = self._config_data
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def _convert_value(self, value: str) -> Any:
        """转换字符串值为适当的类型"""
        if value.lower() in ['true', 'yes', '1']:
            return True
        elif value.lower() in ['false', 'no', '0']:
            return False
        elif value.isdigit():
            return int(value)
        elif self._is_float(value):
            return float(value)
        else:
            return value
    
    def _is_float(self, value: str) -> bool:
        """检查字符串是否为浮点数"""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def get_browser_config(self) -> Dict[str, Any]:
        """获取浏览器配置"""
        return {
            "headless": self.get("browser.headless", False),
            "slow_mo": self.get("browser.slow_mo", 100),
            "timeout": self.get("browser.timeout", 30000),
            "viewport_width": self.get("browser.viewport.width", 1920),
            "viewport_height": self.get("browser.viewport.height", 1080),
        }
    
    def get_test_config(self) -> Dict[str, Any]:
        """获取测试配置"""
        return {
            "base_url": self.get("test.base_url", "https://example.com"),
            "environment": self.get("test.environment", "dev"),
            "retry_count": self.get("test.retry_count", 2),
            "implicit_wait": self.get("test.implicit_wait", 10),
        } 