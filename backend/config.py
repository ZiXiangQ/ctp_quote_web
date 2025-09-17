'''
Author: qiuzx
Date: 2025-09-13 20:00:58
LastEditors: qiuzx
Description: description
'''
"""
配置管理模块
"""

import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class Config:
    """应用配置类"""
    
    # Flask配置
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    PORT = int(os.getenv('PORT', '5005'))
    
    # CTP配置
    CTP_IS_SIM = os.getenv('CTP_IS_SIM', 'true').lower() == 'true'
    CTP_USER_ID = os.getenv('CTP_USER_ID', '')
    CTP_PASSWORD = os.getenv('CTP_PASSWORD', '')
    CTP_USE_MOCK = os.getenv('CTP_USE_MOCK', 'false').lower() == 'true'  # 模拟数据模式
    
    # 日志配置
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate_ctp_config(cls) -> tuple[bool, str]:
        """验证CTP配置"""
        if cls.CTP_USE_MOCK:
            return True, "Using mock data mode"
        if not cls.CTP_USER_ID:
            return False, "CTP_USER_ID is required"
        if not cls.CTP_PASSWORD:
            return False, "CTP_PASSWORD is required"
        return True, "CTP config is valid"

