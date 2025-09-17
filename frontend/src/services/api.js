import { httpClient } from "./http.js";

// CTP相关API
export const ctpAPI = {
  // 获取CTP状态
  getStatus () {
    return httpClient.get("/api/ctp/status");
  },

  // 连接CTP
  connect () {
    return httpClient.post("/api/ctp/connect");
  },

  // 断开CTP连接
  disconnect () {
    return httpClient.post("/api/ctp/disconnect");
  },

  // 订阅合约
  subscribe (instrumentId) {
    return httpClient.post("/api/subscribe", { instrumentId });
  },

  // 取消订阅合约
  unsubscribe (instrumentId) {
    return httpClient.post("/api/unsubscribe", { instrumentId });
  },

  // 获取已订阅的合约列表
  getSubscriptions () {
    return httpClient.get("/api/subscriptions");
  },

  // 获取行情数据
  getQuotes (instrumentIds = []) {
    const params = instrumentIds.length > 0 ? { instruments: instrumentIds.join(",") } : {};
    return httpClient.get("/api/quotes", params);
  },

  // 获取历史行情数据
  getHistoryQuotes (instrumentId, startDate, endDate) {
    return httpClient.get("/api/quotes/history", {
      instrumentId,
      startDate,
      endDate
    });
  }
};

// 系统相关API
export const systemAPI = {
  // 获取系统信息
  getInfo () {
    return httpClient.get("/api/system/info");
  },

  // 获取服务器状态
  getHealth () {
    return httpClient.get("/api/health");
  },

  // 获取配置信息
  getConfig () {
    return httpClient.get("/api/config");
  },

  // 更新配置
  updateConfig (config) {
    return httpClient.post("/api/config", config);
  },

  // 重启服务
  restart () {
    return httpClient.post("/api/system/restart");
  },

  // 获取日志
  getLogs (level = "info", limit = 100) {
    return httpClient.get("/api/logs", { level, limit });
  }
};

// 用户相关API（如果需要）
export const userAPI = {
  // 用户登录
  login (username, password) {
    return httpClient.post("/api/auth/login", { username, password });
  },

  // 用户登出
  logout () {
    return httpClient.post("/api/auth/logout");
  },

  // 获取用户信息
  getUserInfo () {
    return httpClient.get("/api/user/info");
  },

  // 更新用户信息
  updateUserInfo (userInfo) {
    return httpClient.put("/api/user/info", userInfo);
  }
};

// 文件相关API
export const fileAPI = {
  // 上传文件
  uploadFile (file, onProgress) {
    const formData = new FormData();
    formData.append("file", file);

    return httpClient.upload("/api/files/upload", formData, {
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          onProgress(percentCompleted);
        }
      }
    });
  },

  // 下载文件
  downloadFile (fileId) {
    return httpClient.download("/api/files/download", { fileId });
  },

  // 获取文件列表
  getFileList () {
    return httpClient.get("/api/files/list");
  },

  // 删除文件
  deleteFile (fileId) {
    return httpClient.delete(`/api/files/${fileId}`);
  }
};

// 导出所有API
export default {
  ctp: ctpAPI,
  system: systemAPI,
  user: userAPI,
  file: fileAPI
};
