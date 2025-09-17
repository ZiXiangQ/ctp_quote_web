"""
CTP行情接口类
用于连接CTP仿真环境并获取实时行情数据
"""

import threading
import time
from typing import Callable, Dict, Optional, Set

from ctp import CThostFtdcMdSpi
from loguru import logger


class CTPMarketDataAPI(CThostFtdcMdSpi):
    """CTP行情接口类"""

    def __init__(self, front_address: str, broker_id: str, user_id: str, password: str):
        """
        初始化CTP行情接口

        Args:
            front_address: CTP前置地址
            broker_id: 期货公司代码
            user_id: 用户代码
            password: 密码
        """
        super().__init__()
        self.front_address = front_address
        self.broker_id = broker_id
        self.user_id = user_id
        self.password = password

        self.is_connected = False
        self.is_logged_in = False
        self.subscribed_instruments: Set[str] = set()
        self.quote_callbacks: list[Callable] = []

        # 行情数据缓存
        self.last_quotes: Dict[str, dict] = {}
        self.lock = threading.Lock()

        logger.info(f"CTP Market Data API initialized for user: {user_id}")

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
        """连接到CTP服务器"""
        try:
            logger.info(f"Connecting to CTP server: {self.front_address}")
            self.RegisterFront(self.front_address)
            self.Init()
            return True
        except Exception as e:
            logger.error(f"Failed to connect to CTP server: {e}")
            return False

    def login(self) -> bool:
        """登录CTP服务器"""
        try:
            logger.info(f"Logging in to CTP server: {self.user_id}")
            req = {
                "BrokerID": self.broker_id,
                "UserID": self.user_id,
                "Password": self.password,
            }
            self.ReqUserLogin(req, 1)
            return True
        except Exception as e:
            logger.error(f"Failed to login to CTP server: {e}")
            return False

    def subscribe_market_data(self, instruments: list[str]) -> bool:
        """订阅行情数据"""
        try:
            if not instruments:
                return True

            logger.info(f"Subscribing to market data: {instruments}")
            self.SubscribeMarketData(instruments)

            with self.lock:
                self.subscribed_instruments.update(instruments)

            return True
        except Exception as e:
            logger.error(f"Failed to subscribe market data: {e}")
            return False

    def unsubscribe_market_data(self, instruments: list[str]) -> bool:
        """取消订阅行情数据"""
        try:
            if not instruments:
                return True

            logger.info(f"Unsubscribing from market data: {instruments}")
            self.UnSubscribeMarketData(instruments)

            with self.lock:
                for instrument in instruments:
                    self.subscribed_instruments.discard(instrument)
                    self.last_quotes.pop(instrument, None)

            return True
        except Exception as e:
            logger.error(f"Failed to unsubscribe market data: {e}")
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

    # CTP回调函数
    def OnFrontConnected(self):
        """前置机连接成功"""
        logger.info("CTP front connected successfully")
        self.is_connected = True
        self.login()

    def OnFrontDisconnected(self, reason: int):
        """前置机连接断开"""
        logger.warning(f"CTP front disconnected, reason: {reason}")
        self.is_connected = False
        self.is_logged_in = False

    def OnRspUserLogin(self, data, error, nRequestID, isLast):
        """用户登录响应"""
        if error and error['ErrorID'] != 0:
            logger.error(f"Login failed: {error['ErrorMsg']}")
            self.is_logged_in = False
        else:
            logger.info("Login successful")
            self.is_logged_in = True

    def OnRspSubMarketData(self, data, error, nRequestID, isLast):
        """订阅行情响应"""
        if error and error['ErrorID'] != 0:
            logger.error(f"Subscribe market data failed: {error['ErrorMsg']}")
        else:
            logger.info(f"Subscribe market data successful: {data}")

    def OnRspUnSubMarketData(self, data, error, nRequestID, isLast):
        """取消订阅行情响应"""
        if error and error['ErrorID'] != 0:
            logger.error(f"Unsubscribe market data failed: {error['ErrorMsg']}")
        else:
            logger.info(f"Unsubscribe market data successful: {data}")

    def OnRtnDepthMarketData(self, data):
        """行情数据推送"""
        try:
            # 解析行情数据
            quote = self._parse_market_data(data)
            if not quote:
                return

            # 更新缓存
            with self.lock:
                self.last_quotes[quote['instrumentId']] = quote

            # 调用回调函数
            for callback in self.quote_callbacks:
                try:
                    callback(quote)
                except Exception as e:
                    logger.error(f"Error in quote callback: {e}")

        except Exception as e:
            logger.error(f"Error processing market data: {e}")

    def _parse_market_data(self, data) -> Optional[dict]:
        """解析行情数据"""
        try:
            instrument_id = data.get('InstrumentID', '')
            if not instrument_id:
                return None

            # 获取价格数据
            last_price = float(data.get('LastPrice', 0))
            pre_settlement_price = float(data.get('PreSettlementPrice', 0))
            pre_close_price = float(data.get('PreClosePrice', 0))

            # 计算涨跌
            if pre_settlement_price > 0:
                change = last_price - pre_settlement_price
                change_percent = (change / pre_settlement_price) * 100
            elif pre_close_price > 0:
                change = last_price - pre_close_price
                change_percent = (change / pre_close_price) * 100
            else:
                change = 0
                change_percent = 0

            # 获取成交量
            volume = int(data.get('Volume', 0))

            # 获取时间
            update_time = data.get('UpdateTime', '')
            update_millisec = int(data.get('UpdateMillisec', 0))

            quote = {
                'instrumentId': instrument_id,
                'lastPrice': round(last_price, 2),
                'change': round(change, 2),
                'changePercent': round(change_percent, 2),
                'volume': volume,
                'updateTime': update_time,
                'updateMillisec': update_millisec,
                'ts': int(time.time() * 1000)
            }

            return quote

        except Exception as e:
            logger.error(f"Error parsing market data: {e}")
            return None

    def disconnect(self):
        """断开连接"""
        try:
            logger.info("Disconnecting from CTP server")
            self.Release()
            self.is_connected = False
            self.is_logged_in = False
        except Exception as e:
            logger.error(f"Error disconnecting from CTP server: {e}")


class CTPConfig:
    """CTP配置类"""

    # CTP仿真环境配置
    SIM_FRONT_ADDRESS = "tcp://180.168.146.187:10131"  # 仿真环境前置地址
    SIM_BROKER_ID = "9999"  # 仿真环境期货公司代码

    # 生产环境配置（需要真实账户）
    PROD_FRONT_ADDRESS = "tcp://180.168.146.187:10110"
    PROD_BROKER_ID = "9999"

    @classmethod
    def get_config(cls, is_sim: bool = True) -> dict:
        """获取CTP配置"""
        if is_sim:
            return {
                'front_address': cls.SIM_FRONT_ADDRESS,
                'broker_id': cls.SIM_BROKER_ID,
            }
        else:
            return {
                'front_address': cls.PROD_FRONT_ADDRESS,
                'broker_id': cls.PROD_BROKER_ID,
            }
