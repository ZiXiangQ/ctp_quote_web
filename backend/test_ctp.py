#!/usr/bin/env python3
"""
CTP连接测试脚本
"""

import sys
import time
from ctp_mdapi import CTPMarketDataAPI, CTPConfig
from config import Config
from loguru import logger

def test_ctp_connection():
    """测试CTP连接"""
    logger.info("Testing CTP connection...")
    
    # 验证配置
    is_valid, error_msg = Config.validate_ctp_config()
    if not is_valid:
        logger.error(f"CTP config validation failed: {error_msg}")
        return False
    
    # 获取CTP配置
    ctp_config = CTPConfig.get_config(Config.CTP_IS_SIM)
    
    # 创建CTP API实例
    ctp_api = CTPMarketDataAPI(
        front_address=ctp_config['front_address'],
        broker_id=ctp_config['broker_id'],
        user_id=Config.CTP_USER_ID,
        password=Config.CTP_PASSWORD
    )
    
    # 添加测试回调
    def test_callback(quote):
        logger.info(f"Received quote: {quote}")
    
    ctp_api.add_quote_callback(test_callback)
    
    try:
        # 连接CTP服务器
        logger.info("Connecting to CTP server...")
        if not ctp_api.connect():
            logger.error("Failed to connect to CTP server")
            return False
        
        # 等待连接建立
        logger.info("Waiting for connection...")
        time.sleep(3)
        
        if not ctp_api.is_connected:
            logger.error("CTP connection failed")
            return False
        
        logger.success("✅ CTP connected successfully")
        
        # 测试订阅行情
        test_instruments = ["rb2501", "hc2501", "i2501"]
        logger.info(f"Testing subscription for: {test_instruments}")
        
        if ctp_api.subscribe_market_data(test_instruments):
            logger.success("✅ Subscription successful")
            
            # 等待行情数据
            logger.info("Waiting for market data...")
            time.sleep(10)
            
            # 检查收到的行情
            quotes = ctp_api.get_all_quotes()
            if quotes:
                logger.success(f"✅ Received {len(quotes)} quotes")
                for instrument, quote in quotes.items():
                    logger.info(f"  {instrument}: {quote['lastPrice']} ({quote['change']:+.2f})")
            else:
                logger.warning("⚠️ No quotes received")
        else:
            logger.error("❌ Subscription failed")
        
        # 断开连接
        ctp_api.disconnect()
        logger.info("Disconnected from CTP server")
        
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        return False

def main():
    """主函数"""
    logger.remove()
    logger.add(
        lambda msg: print(msg, end=""),
        level="INFO",
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}"
    )
    
    logger.info("CTP Connection Test")
    logger.info("=" * 30)
    
    success = test_ctp_connection()
    
    if success:
        logger.success("✅ CTP test completed successfully")
        sys.exit(0)
    else:
        logger.error("❌ CTP test failed")
        sys.exit(1)

if __name__ == '__main__':
    main()

