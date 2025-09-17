from __future__ import annotations

import os
import random
import time
from threading import Lock
from typing import Optional

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from pydantic import BaseModel, ValidationError
from loguru import logger

from ctp_mdapi import CTPMarketDataAPI, CTPConfig
from mock_ctp import MockCTPAPI
from config import Config


class SubscribePayload(BaseModel):
    instrumentId: str


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    CORS(app, resources={r"/*": {"origins": "*"}})
    return app


app = create_app()
socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    async_mode="eventlet",
    logger=True,
    engineio_logger=True
)

# 全局变量
_subscribed_instruments: set[str] = set()
_lock = Lock()
_ctp_api: Optional[CTPMarketDataAPI] = None
_mock_api: Optional[MockCTPAPI] = None
_is_ctp_connected = False
_is_mock_mode = False


def init_ctp_api():
    """初始化CTP API"""
    global _ctp_api, _mock_api, _is_ctp_connected, _is_mock_mode
    
    # 验证配置
    is_valid, error_msg = Config.validate_ctp_config()
    if not is_valid:
        logger.error(f"CTP config validation failed: {error_msg}")
        return False
    
    # 检查是否使用模拟模式
    if Config.CTP_USE_MOCK:
        logger.info("Using mock CTP mode")
        return init_mock_api()
    
    try:
        # 获取CTP配置
        ctp_config = CTPConfig.get_config(Config.CTP_IS_SIM)
        
        # 创建CTP API实例
        _ctp_api = CTPMarketDataAPI(
            front_address=ctp_config['front_address'],
            broker_id=ctp_config['broker_id'],
            user_id=Config.CTP_USER_ID,
            password=Config.CTP_PASSWORD
        )
        
        # 添加行情回调
        _ctp_api.add_quote_callback(_on_ctp_quote)
        
        # 连接CTP服务器
        if _ctp_api.connect():
            logger.info("CTP API initialized successfully")
            _is_ctp_connected = True
            _is_mock_mode = False
            return True
        else:
            logger.error("Failed to connect to CTP server")
            return False
            
    except Exception as e:
        logger.error(f"Failed to initialize CTP API: {e}")
        return False


def init_mock_api():
    """初始化模拟CTP API"""
    global _mock_api, _is_ctp_connected, _is_mock_mode
    
    try:
        # 创建模拟API实例
        _mock_api = MockCTPAPI()
        
        # 添加行情回调
        _mock_api.add_quote_callback(_on_ctp_quote)
        
        # 连接模拟服务器
        if _mock_api.connect() and _mock_api.login():
            logger.info("Mock CTP API initialized successfully")
            _is_ctp_connected = True
            _is_mock_mode = True
            return True
        else:
            logger.error("Failed to initialize mock CTP API")
            return False
            
    except Exception as e:
        logger.error(f"Failed to initialize mock CTP API: {e}")
        return False


def _on_ctp_quote(quote: dict):
    """CTP行情回调函数"""
    try:
        # 通过WebSocket发送行情数据
        socketio.emit('quote', quote)
        logger.debug(f"Sent quote: {quote['instrumentId']} = {quote['lastPrice']}")
    except Exception as e:
        logger.error(f"Error sending quote: {e}")


@app.route('/api/health', methods=['GET'])
def health():
    """健康检查接口"""
    ctp_status = "connected" if _is_ctp_connected else "disconnected"
    return jsonify({
        "status": "ok",
        "ctp_status": ctp_status,
        "subscribed_count": len(_subscribed_instruments)
    })


@app.route('/api/ctp/status', methods=['GET'])
def ctp_status():
    """CTP连接状态接口"""
    if _is_mock_mode and _mock_api:
        return jsonify({
            "connected": _is_ctp_connected,
            "logged_in": _mock_api.is_logged_in,
            "subscribed_instruments": list(_mock_api.get_subscribed_instruments()),
            "mode": "mock"
        })
    elif _ctp_api:
        return jsonify({
            "connected": _is_ctp_connected,
            "logged_in": _ctp_api.is_logged_in,
            "subscribed_instruments": list(_ctp_api.get_subscribed_instruments()),
            "mode": "real"
        })
    else:
        return jsonify({"connected": False, "message": "CTP API not initialized"})


@app.route('/api/ctp/connect', methods=['POST'])
def ctp_connect():
    """连接CTP服务器"""
    global _is_ctp_connected
    
    if _is_ctp_connected:
        return jsonify({"success": True, "message": "Already connected"})
    
    success = init_ctp_api()
    if success:
        return jsonify({"success": True, "message": "Connected to CTP server"})
    else:
        return jsonify({"success": False, "message": "Failed to connect to CTP server"}), 500


@app.route('/api/ctp/disconnect', methods=['POST'])
def ctp_disconnect():
    """断开CTP连接"""
    global _ctp_api, _mock_api, _is_ctp_connected, _is_mock_mode
    
    if _is_mock_mode and _mock_api:
        _mock_api.disconnect()
        _mock_api = None
        _is_ctp_connected = False
        _is_mock_mode = False
        logger.info("Disconnected from mock CTP server")
    elif _ctp_api:
        _ctp_api.disconnect()
        _ctp_api = None
        _is_ctp_connected = False
        logger.info("Disconnected from CTP server")
    
    return jsonify({"success": True, "message": "Disconnected from CTP server"})


@app.route('/api/subscriptions', methods=['GET'])
def subscriptions():
    with _lock:
        return jsonify(sorted(list(_subscribed_instruments)))


@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    try:
        data = SubscribePayload.model_validate(request.json or {})
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    instrument_id = data.instrumentId.strip()
    if not instrument_id:
        return jsonify({"error": "instrumentId is required"}), 400

    with _lock:
        _subscribed_instruments.add(instrument_id)

    # 如果CTP已连接，订阅CTP行情
    if _is_mock_mode and _mock_api and _is_ctp_connected:
        try:
            success = _mock_api.subscribe_market_data([instrument_id])
            if not success:
                logger.warning(f"Failed to subscribe mock CTP market data for {instrument_id}")
        except Exception as e:
            logger.error(f"Error subscribing mock CTP market data: {e}")
    elif _ctp_api and _is_ctp_connected:
        try:
            success = _ctp_api.subscribe_market_data([instrument_id])
            if not success:
                logger.warning(f"Failed to subscribe CTP market data for {instrument_id}")
        except Exception as e:
            logger.error(f"Error subscribing CTP market data: {e}")

    return jsonify({"ok": True, "instrumentId": instrument_id})


@app.route('/api/unsubscribe', methods=['POST'])
def unsubscribe():
    instrument_id = (request.json or {}).get('instrumentId', '').strip()
    if not instrument_id:
        return jsonify({"error": "instrumentId is required"}), 400

    with _lock:
        _subscribed_instruments.discard(instrument_id)

    # 如果CTP已连接，取消订阅CTP行情
    if _is_mock_mode and _mock_api and _is_ctp_connected:
        try:
            success = _mock_api.unsubscribe_market_data([instrument_id])
            if not success:
                logger.warning(f"Failed to unsubscribe mock CTP market data for {instrument_id}")
        except Exception as e:
            logger.error(f"Error unsubscribing mock CTP market data: {e}")
    elif _ctp_api and _is_ctp_connected:
        try:
            success = _ctp_api.unsubscribe_market_data([instrument_id])
            if not success:
                logger.warning(f"Failed to unsubscribe CTP market data for {instrument_id}")
        except Exception as e:
            logger.error(f"Error unsubscribing CTP market data: {e}")

    return jsonify({"ok": True, "instrumentId": instrument_id})


# WebSocket 事件处理
@socketio.on('connect')
def handle_connect():
    """客户端连接事件"""
    logger.info(f"Client connected: {request.sid}")
    # 发送欢迎消息
    socketio.emit('server_info', {
        "message": "connected",
        "timestamp": int(time.time() * 1000),
        "subscribed_count": len(_subscribed_instruments)
    })
    
    # 如果有订阅的合约，发送当前行情
    if _subscribed_instruments:
        with _lock:
            instruments = list(_subscribed_instruments)
        for instrument in instruments:
            if _is_mock_mode and _mock_api:
                quote = _mock_api.get_last_quote(instrument)
            elif _ctp_api:
                quote = _ctp_api.get_last_quote(instrument)
            else:
                continue
                
            if quote:
                socketio.emit('quote', quote)


@socketio.on('disconnect')
def handle_disconnect():
    """客户端断开连接事件"""
    logger.info(f"Client disconnected: {request.sid}")


@socketio.on('ping')
def handle_ping():
    """心跳检测"""
    socketio.emit('pong', {'timestamp': int(time.time() * 1000)})


def _mock_quote_stream():
    last_price_map: dict[str, float] = {}
    while True:
        with _lock:
            instruments = list(_subscribed_instruments)
        # 若没有订阅，降低频率
        sleep_seconds = 0.9 if not instruments else 0.4

        for instrument in instruments:
            base = last_price_map.get(instrument)
            if base is None:
                # 随机初始价
                base = random.uniform(1000.0, 5000.0)

            delta = random.uniform(-5.0, 5.0)
            price = max(0.01, round(base + delta, 2))
            change = round(price - base, 2)
            change_percent = round((change / base) * 100.0, 2) if base else 0.0

            last_price_map[instrument] = price

            socketio.emit('quote', {
                'instrumentId': instrument,
                'lastPrice': price,
                'change': change,
                'changePercent': change_percent,
                'ts': int(time.time() * 1000)
            })

        socketio.sleep(sleep_seconds)


def setup_logging():
    """设置日志配置"""
    logger.remove()  # 移除默认处理器
    logger.add(
        "logs/ctp_quote_{time}.log",
        rotation="1 day",
        retention="7 days",
        level=Config.LOG_LEVEL,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}"
    )
    logger.add(
        lambda msg: print(msg, end=""),
        level=Config.LOG_LEVEL,
        format="<green>{time:HH:mm:ss}</green> | <level>{level}</level> | {message}"
    )


def start_mock_quote_stream():
    """启动模拟行情推送（当CTP未连接时使用）"""
    if not _is_ctp_connected:
        logger.info("Starting mock quote stream (CTP not connected)")
        socketio.start_background_task(_mock_quote_stream)


def main():
    """主函数"""
    # 设置日志
    setup_logging()
    
    # 创建日志目录
    os.makedirs("logs", exist_ok=True)
    
    logger.info("=" * 50)
    logger.info("CTP Quote App Server Starting...")
    logger.info("=" * 50)
    logger.info(f"CTP Simulation Mode: {Config.CTP_IS_SIM}")
    logger.info(f"CTP User ID: {Config.CTP_USER_ID}")
    logger.info(f"Server Port: {Config.PORT}")
    
    # 检查CTP配置
    is_valid, error_msg = Config.validate_ctp_config()
    if not is_valid:
        logger.warning(f"CTP config invalid: {error_msg}")
        logger.warning("Will use mock data instead")
    else:
        logger.info("CTP config is valid")
    
    # 尝试连接CTP
    if is_valid:
        logger.info("Attempting to connect to CTP server...")
        if init_ctp_api():
            logger.success("✅ CTP API connected successfully")
        else:
            logger.warning("❌ Failed to connect to CTP server, using mock data")
            start_mock_quote_stream()
    else:
        logger.warning("❌ CTP credentials not provided, using mock data")
        start_mock_quote_stream()
    
    # 启动服务器
    logger.info(f"🚀 Starting Flask server on port {Config.PORT}")
    logger.info("=" * 50)
    
    try:
        socketio.run(app, host='0.0.0.0', port=Config.PORT, debug=False)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
