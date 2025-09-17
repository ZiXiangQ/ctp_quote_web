"""
CTP模拟数据生成器
当无法连接真实CTP服务器时，使用此模块生成模拟行情数据
"""

import time
import random
import threading
from typing import Dict, Set, Callable, Optional
from loguru import logger


class MockCTPAPI:
    """CTP模拟数据API类"""
    
    def __init__(self):
        self.is_connected = False
        self.is_logged_in = False
        self.subscribed_instruments: Set[str] = set()
        self.quote_callbacks: list[Callable] = []
        
        # 行情数据缓存
        self.last_quotes: Dict[str, dict] = {}
        self.lock = threading.Lock()
        
        # 模拟数据生成线程
        self.mock_thread = None
        self.stop_mock = False
        
        # 基础价格数据（用于生成模拟数据）
        self.base_prices = {
            'rb2501': 3500.0,  # 螺纹钢
            'hc2501': 3600.0,  # 热卷
            'i2501': 800.0,    # 铁矿石
            'j2501': 2500.0,   # 焦炭
            'jm2501': 1800.0,  # 焦煤
            'cu2501': 70000.0, # 铜
            'al2501': 18000.0, # 铝
            'zn2501': 25000.0, # 锌
            'ag2501': 6000.0,  # 白银
            'au2501': 500.0,   # 黄金
        }
        
        logger.info("Mock CTP API initialized")
    
    def add_quote_callback(self, callback: Callable):
        """添加行情回调函数"""
        self.quote_callbacks.append(callback)
        logger.info(f"Added quote callback, total callbacks: {len(self.quote_callbacks)}")
    
    def remove_quote_callback(self, callback: Callable):
        """移除行情回调函数"""
        if callback in self.quote_callbacks:
            self.quote_callbacks.remove(callback)
            logger.info(f"Removed quote callback, total callbacks: {len(self.quote_callbacks)}")
    
    def connect(self) -> bool:
        """模拟连接到CTP服务器"""
        try:
            logger.info("Connecting to mock CTP server")
            time.sleep(0.5)  # 模拟连接延迟
            self.is_connected = True
            logger.info("Mock CTP server connected successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to connect to mock CTP server: {e}")
            return False
    
    def login(self) -> bool:
        """模拟登录CTP服务器"""
        try:
            logger.info("Logging in to mock CTP server")
            time.sleep(0.3)  # 模拟登录延迟
            self.is_logged_in = True
            logger.info("Mock CTP server login successful")
            return True
        except Exception as e:
            logger.error(f"Failed to login to mock CTP server: {e}")
            return False
    
    def subscribe_market_data(self, instruments: list[str]) -> bool:
        """订阅行情数据"""
        try:
            if not instruments:
                return True
                
            logger.info(f"Subscribing to mock market data: {instruments}")
            
            with self.lock:
                self.subscribed_instruments.update(instruments)
                # 为每个合约初始化基础价格
                for instrument in instruments:
                    if instrument not in self.base_prices:
                        self.base_prices[instrument] = 1000.0  # 默认价格
            
            # 启动模拟数据生成线程
            if not self.mock_thread or not self.mock_thread.is_alive():
                self.stop_mock = False
                self.mock_thread = threading.Thread(target=self._generate_mock_data, daemon=True)
                self.mock_thread.start()
            
            return True
        except Exception as e:
            logger.error(f"Failed to subscribe mock market data: {e}")
            return False
    
    def unsubscribe_market_data(self, instruments: list[str]) -> bool:
        """取消订阅行情数据"""
        try:
            if not instruments:
                return True
                
            logger.info(f"Unsubscribing from mock market data: {instruments}")
            
            with self.lock:
                for instrument in instruments:
                    self.subscribed_instruments.discard(instrument)
                    self.last_quotes.pop(instrument, None)
            
            # 如果没有订阅的合约了，停止模拟数据生成
            if not self.subscribed_instruments:
                self.stop_mock = True
            
            return True
        except Exception as e:
            logger.error(f"Failed to unsubscribe mock market data: {e}")
            return False
    
    def get_subscribed_instruments(self) -> Set[str]:
        """获取已订阅的合约列表"""
        with self.lock:
            return self.subscribed_instruments.copy()
    
    def get_last_quote(self, instrument_id: str) -> Optional[dict]:
        """获取指定合约的最新行情"""
        with self.lock:
            return self.last_quotes.get(instrument_id)
    
    def get_all_quotes(self) -> Dict[str, dict]:
        """获取所有合约的最新行情"""
        with self.lock:
            return self.last_quotes.copy()
    
    def _generate_mock_data(self):
        """生成模拟行情数据"""
        logger.info("Starting mock data generation")
        logger.info(f"Subscribed instruments: {self.subscribed_instruments}")
        
        while not self.stop_mock:
            try:
                with self.lock:
                    instruments = list(self.subscribed_instruments)
                
                if not instruments:
                    time.sleep(1)
                    continue
                
                # 为每个订阅的合约生成行情数据
                for instrument in instruments:
                    quote = self._create_mock_quote(instrument)
                    if quote:
                        with self.lock:
                            self.last_quotes[instrument] = quote
                        
                        logger.debug(f"Generated quote for {instrument}: {quote}")
                        
                        # 调用回调函数
                        for callback in self.quote_callbacks:
                            try:
                                callback(quote)
                                logger.debug(f"Callback executed for {instrument}")
                            except Exception as e:
                                logger.error(f"Error in mock quote callback: {e}")
                
                # 每500ms更新一次数据
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error generating mock data: {e}")
                time.sleep(1)
        
        logger.info("Mock data generation stopped")
    
    def _create_mock_quote(self, instrument_id: str) -> Optional[dict]:
        """创建模拟行情数据"""
        try:
            # 获取基础价格
            base_price = self.base_prices.get(instrument_id, 1000.0)
            
            # 生成价格波动（-2% 到 +2%）
            change_percent = random.uniform(-2.0, 2.0)
            price_change = base_price * (change_percent / 100)
            last_price = base_price + price_change
            
            # 更新基础价格（模拟价格趋势）
            self.base_prices[instrument_id] = last_price
            
            # 生成成交量
            volume = random.randint(100, 10000)
            
            # 生成时间
            current_time = time.time()
            update_time = time.strftime("%H:%M:%S", time.localtime(current_time))
            update_millisec = int((current_time % 1) * 1000)
            
            quote = {
                'instrumentId': instrument_id,
                'lastPrice': round(last_price, 2),
                'change': round(price_change, 2),
                'changePercent': round(change_percent, 2),
                'volume': volume,
                'updateTime': update_time,
                'updateMillisec': update_millisec,
                'ts': int(current_time * 1000)
            }
            
            return quote
            
        except Exception as e:
            logger.error(f"Error creating mock quote for {instrument_id}: {e}")
            return None
    
    def disconnect(self):
        """断开连接"""
        try:
            logger.info("Disconnecting from mock CTP server")
            self.stop_mock = True
            if self.mock_thread and self.mock_thread.is_alive():
                self.mock_thread.join(timeout=2)
            self.is_connected = False
            self.is_logged_in = False
            logger.info("Mock CTP server disconnected")
        except Exception as e:
            logger.error(f"Error disconnecting from mock CTP server: {e}")
