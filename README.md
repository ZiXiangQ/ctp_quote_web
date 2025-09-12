# ctp-quote-app

一个基于 Vue3 + Vite + Quasar 的前端与 Flask + Socket.IO 的后端，演示如何接入（当前为模拟）CTP 行情并在页面实时展示。

## 架构
- 前端：Vue3 + Vite，UI 使用 Quasar（`@quasar/extras` 图标 + `quasar` 样式），Router 管理导航，Pinia 预留状态管理，`socket.io-client` 接收行情推送。
- 后端：Flask + Flask-SocketIO（eventlet），CORS 开放跨域，REST 提供订阅接口，后台任务模拟行情并通过 Socket 推送。

## 目录结构
```
ctp-quote-app/
  frontend/
    src/
      pages/             # 页面：Quotes/Subscribe/Settings/About
      router/            # 路由
      services/          # 前端服务: socket.js
      quasar-variables.sass
      App.vue            # Quasar 布局（侧边栏 + 路由视图）
      main.js
    vite.config.js       # 集成 Quasar 插件
  backend/
    app.py               # Flask + Socket.IO + 模拟行情
    requirements.txt
  scripts/
    run_frontend.sh
    run_backend.sh
```

## 页面设计
- 行情（Quotes）：
  - 使用 `q-table` 展示 `instrumentId / lastPrice / change / changePercent`。
  - 通过 Socket 实时接收推送并更新表格，涨跌颜色区分。
- 订阅（Subscribe）：
  - 表单提交合约代码，请求后端 `/api/subscribe`，下方展示已订阅列表。
- 设置（Settings）：
  - 可配置后端地址（默认 `http://127.0.0.1:5000`），支持切换深色模式。
- 关于（About）：
  - 简要说明项目。

## 运行
1) 后端
```
./scripts/run_backend.sh
```
或手动：
```
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```
健康检查：`GET http://127.0.0.1:5000/api/health`

2) 前端
```
./scripts/run_frontend.sh
```
或手动：
```
cd frontend
npm i
npm run dev -- --port 5173
```
访问：`http://localhost:5173`

> 如需修改后端地址，请在“设置”页调整（会存入 localStorage）。

## 数据流（模拟）
- Subscribe 页面调用 `POST /api/subscribe` 订阅一个合约。
- 后端将合约加入内存集合，后台任务周期生成价格并通过 `SocketIO.emit('quote', { ... })` 推送给前端。
- 前端 `src/services/socket.js` 建立与后端的 Socket 连接，Quotes 页面监听 `quote` 事件并执行 upsert 更新表格。

## 后续对接真实 CTP
- 在后端替换 `_mock_quote_stream`，改为集成 CTP 行情 API（如上期技术的 CTP MdApi）。
- 将订阅接口 `/api/subscribe` 连接至真实 MdApi 的订阅调用，并在回调中 `socketio.emit('quote', ...)`。
- 可考虑 Redis/Kafka 缓存与消息队列、鉴权、日志与持久化等。
