# CTP行情服务配置指南

## 概述

本服务集成了CTP（中国期货市场监控中心）仿真环境，可以获取实时期货行情数据。

## 配置步骤

### 1. 注册CTP仿真账户

1. 访问 [CTP仿真环境](http://simnow.com.cn/)
2. 注册免费账户
3. 获取用户代码和密码

### 2. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件：

```env
# CTP配置
CTP_IS_SIM=true
CTP_USER_ID=你的用户代码
CTP_PASSWORD=你的密码

# Flask配置
SECRET_KEY=your_secret_key
PORT=5005

# 日志配置
LOG_LEVEL=INFO
```

### 4. 启动服务

```bash
python run_server.py
```

## API接口

### 健康检查
- `GET /api/health` - 检查服务状态

### CTP管理
- `GET /api/ctp/status` - 获取CTP连接状态
- `POST /api/ctp/connect` - 连接CTP服务器
- `POST /api/ctp/disconnect` - 断开CTP连接

### 行情订阅
- `GET /api/subscriptions` - 获取已订阅合约列表
- `POST /api/subscribe` - 订阅合约行情
- `POST /api/unsubscribe` - 取消订阅合约行情

## WebSocket事件

### 客户端连接
- `connect` - 客户端连接

### 服务端推送
- `quote` - 行情数据推送
- `server_info` - 服务器信息

## 行情数据格式

```json
{
  "instrumentId": "rb2501",
  "lastPrice": 3500.0,
  "change": 50.0,
  "changePercent": 1.45,
  "volume": 12000,
  "updateTime": "14:30:00",
  "updateMillisec": 500,
  "ts": 1691234567890
}
```

## 常见问题

### 1. CTP连接失败
- 检查网络连接
- 验证用户代码和密码
- 确认仿真环境地址正确

### 2. 行情数据不更新
- 检查合约代码是否正确
- 确认已成功订阅
- 查看日志文件排查问题

### 3. 服务启动失败
- 检查端口是否被占用
- 验证Python依赖是否正确安装
- 查看错误日志

## 日志文件

日志文件保存在 `logs/` 目录下：
- `ctp_quote_YYYY-MM-DD.log` - 每日日志文件
- 保留7天的历史日志

## 开发模式

如果需要开发调试，可以设置环境变量：

```bash
export LOG_LEVEL=DEBUG
python run_server.py
```

## 生产部署

1. 设置生产环境配置
2. 使用进程管理器（如supervisor）
3. 配置反向代理（如nginx）
4. 设置日志轮转和监控

