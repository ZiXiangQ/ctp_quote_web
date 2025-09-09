from __future__ import annotations

import os
import random
import time
from threading import Lock

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO
from pydantic import BaseModel, ValidationError


class SubscribePayload(BaseModel):
    instrumentId: str


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret')
    CORS(app, resources={r"/*": {"origins": "*"}})
    return app


app = create_app()
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="eventlet")

_subscribed_instruments: set[str] = set()
_lock = Lock()


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"})


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

    return jsonify({"ok": True, "instrumentId": instrument_id})


@app.route('/api/unsubscribe', methods=['POST'])
def unsubscribe():
    instrument_id = (request.json or {}).get('instrumentId', '').strip()
    if not instrument_id:
        return jsonify({"error": "instrumentId is required"}), 400

    with _lock:
        _subscribed_instruments.discard(instrument_id)

    return jsonify({"ok": True, "instrumentId": instrument_id})


# 模拟 CTP 行情推送
@socketio.on('connect')
def handle_connect():
    # 可在此发送欢迎消息或当前订阅状态
    socketio.emit('server_info', {"message": "connected"})


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


if __name__ == '__main__':
    # 启动后台行情推送任务
    socketio.start_background_task(_mock_quote_stream)
    socketio.run(app, host='0.0.0.0', port=int(os.getenv('PORT', '5000')))
