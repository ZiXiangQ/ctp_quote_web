# CTP真实连接配置指南

## 📋 前置条件

1. **CTP账号**: 已注册CTP网站用户账号
2. **期货公司**: 已开通期货账户
3. **行情权限**: 已开通行情数据权限

## 🔧 配置步骤

### 1. 运行配置向导

```bash
python3 scripts/configure_ctp.py
```

### 2. 手动配置（可选）

编辑 `backend/.env` 文件：

```env
# CTP配置
CTP_IS_SIM=true                    # true=模拟环境, false=生产环境
CTP_USE_MOCK=false                 # false=使用真实CTP, true=使用模拟数据
CTP_USER_ID=your_user_id          # 你的CTP用户ID
CTP_PASSWORD=your_password        # 你的CTP密码

# Flask配置
SECRET_KEY=dev-secret-key
PORT=5005

# 日志配置
LOG_LEVEL=INFO
```

## 🌐 CTP环境说明

### 模拟环境 (CTP_IS_SIM=true)
- **用途**: 测试和开发
- **数据**: 真实行情数据
- **风险**: 无交易风险
- **推荐**: 开发阶段使用

### 生产环境 (CTP_IS_SIM=false)
- **用途**: 真实交易
- **数据**: 真实行情数据
- **风险**: 有交易风险
- **注意**: 需要谨慎使用

## 🚀 启动服务

```bash
# 启动服务
python3 scripts/start_server.py

# 检查连接状态
curl http://172.18.141.52:5005/api/ctp/status
```

## 📊 验证连接

### 1. 检查CTP状态
```bash
curl http://172.18.141.52:5005/api/ctp/status
```

期望返回：
```json
{
  "connected": true,
  "logged_in": true,
  "mode": "real",
  "subscribed_instruments": []
}
```

### 2. 测试订阅
```bash
# 订阅一个合约
curl -X POST http://172.18.141.52:5005/api/subscribe \
  -H "Content-Type: application/json" \
  -d '{"instrumentId": "rb2501"}'
```

### 3. 查看行情数据
访问前端页面，应该能看到实时行情数据更新。

## ⚠️ 注意事项

1. **账号安全**: 不要将密码提交到代码仓库
2. **网络连接**: 确保网络能访问CTP服务器
3. **权限检查**: 确认账号有行情数据权限
4. **环境选择**: 建议先在模拟环境测试

## 🔍 故障排除

### 连接失败
1. 检查网络连接
2. 验证账号密码
3. 确认CTP服务器地址
4. 检查防火墙设置

### 登录失败
1. 验证用户ID和密码
2. 检查账号是否被锁定
3. 确认账号权限

### 行情数据异常
1. 检查合约代码格式
2. 确认合约是否有效
3. 验证订阅权限

## 📞 技术支持

如果遇到问题，可以：
1. 查看日志文件 `backend/logs/`
2. 检查CTP官网文档
3. 联系期货公司技术支持
