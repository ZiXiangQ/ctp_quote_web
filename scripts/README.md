# 启动脚本说明

## 脚本列表

### 1. `start_server.py` - 完整启动脚本
**功能**：
- 自动创建虚拟环境
- 安装依赖包
- 创建配置文件
- 启动服务

**使用方法**：
```bash
# 从项目根目录运行
python3 scripts/start_server.py

# 或者直接运行
./scripts/start_server.py
```

**适用场景**：
- 首次部署
- 生产环境
- 需要完整环境设置

### 2. `dev_start.py` - 开发环境快速启动
**功能**：
- 快速启动服务
- 假设环境已配置好

**使用方法**：
```bash
# 从项目根目录运行
python3 scripts/dev_start.py

# 或者直接运行
./scripts/dev_start.py
```

**适用场景**：
- 日常开发
- 环境已配置好
- 快速启动测试

### 3. `start_ctp_server.sh` - 原始Bash脚本（保留）
**功能**：
- 传统的Bash启动脚本
- 兼容性更好

**使用方法**：
```bash
./scripts/start_ctp_server.sh
```

## 推荐使用方式

### 首次使用
```bash
python3 scripts/start_server.py
```

### 日常开发
```bash
python3 scripts/dev_start.py
```

## 环境要求

- Python 3.8+
- 网络连接（用于安装依赖）

## 故障排除

### 虚拟环境问题
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### 权限问题
```bash
chmod +x scripts/*.py
```

### 依赖安装失败
```bash
cd backend
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
