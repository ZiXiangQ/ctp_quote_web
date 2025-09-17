# Services 服务层

这个文件夹包含了前端的所有服务层代码，包括HTTP请求封装、API接口封装和WebSocket服务。

## 文件结构

```
services/
├── http.js          # HTTP请求封装（基于axios）
├── api.js           # API接口封装
├── socket.js        # WebSocket服务
└── README.md        # 说明文档
```

## 使用方法

### 1. HTTP客户端 (http.js)

```javascript
import { httpClient } from '@/services/http.js';

// GET请求
const data = await httpClient.get('/api/users', { page: 1, limit: 10 });

// POST请求
const result = await httpClient.post('/api/users', { name: 'John', email: 'john@example.com' });

// 上传文件
const formData = new FormData();
formData.append('file', file);
const uploadResult = await httpClient.upload('/api/files/upload', formData);
```

### 2. API服务 (api.js)

```javascript
import { ctpAPI, systemAPI } from '@/services/api.js';

// CTP相关操作
const status = await ctpAPI.getStatus();
const result = await ctpAPI.subscribe('rb2501');
const subscriptions = await ctpAPI.getSubscriptions();

// 系统相关操作
const systemInfo = await systemAPI.getInfo();
const health = await systemAPI.getHealth();
```

### 3. WebSocket服务 (socket.js)

```javascript
import { connectSocket, subscribeInstrument } from '@/services/socket.js';

// 连接WebSocket
const socket = connectSocket();

// 监听行情数据
socket.on('quote', (data) => {
  console.log('收到行情数据:', data);
});

// 订阅合约
await subscribeInstrument('rb2501');
```

## 配置说明

### 后端URL配置

所有服务都会从localStorage中读取`backendUrl`配置，如果没有配置则使用默认值：

```javascript
// 设置后端URL
localStorage.setItem('backendUrl', 'http://192.168.1.100:5005');

// 获取后端URL
const url = localStorage.getItem('backendUrl');
```

### 错误处理

HTTP请求会自动处理常见错误：
- 401: 未授权
- 403: 禁止访问
- 404: 资源不存在
- 500: 服务器错误
- 网络错误

### 请求拦截器

- 自动添加认证token（如果存在）
- 动态更新baseURL
- 请求日志记录

### 响应拦截器

- 统一错误处理
- 响应日志记录
- 自动解析响应数据

## 扩展说明

### 添加新的API接口

在`api.js`中添加新的API方法：

```javascript
export const newAPI = {
  // 新接口
  newMethod(params) {
    return httpClient.get('/api/new-endpoint', params);
  }
};
```

### 添加新的HTTP方法

在`http.js`的`httpClient`对象中添加新方法：

```javascript
// 自定义请求方法
customRequest(url, method, data, config) {
  return http({
    url,
    method,
    data,
    ...config
  });
}
```

## 注意事项

1. 所有API调用都是异步的，需要使用`await`或`.then()`
2. 错误会被自动捕获和处理，但建议在调用处也添加错误处理
3. WebSocket连接会自动重连，无需手动处理
4. 文件上传支持进度回调
5. 所有请求都会自动添加Content-Type头
