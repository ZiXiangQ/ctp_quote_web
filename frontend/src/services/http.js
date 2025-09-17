import axios from "axios";

// 获取后端URL
const getBackendUrl = () => {
  return localStorage.getItem("backendUrl") || "http://172.18.141.52:5005";
};

// 创建axios实例
const http = axios.create({
  baseURL: getBackendUrl(),
  timeout: 10000,
  headers: {
    "Content-Type": "application/json"
  }
});

// 请求拦截器
http.interceptors.request.use(
  (config) => {
    config.baseURL = getBackendUrl();

    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    console.log("HTTP Request:", config.method?.toUpperCase(), config.url, config.data);
    return config;
  },
  (error) => {
    console.error("Request Error:", error);
    return Promise.reject(error);
  }
);

// 响应拦截器
http.interceptors.response.use(
  (response) => {
    console.log("HTTP Response:", response.status, response.data);
    return response.data;
  },
  (error) => {
    console.error("Response Error:", error.response?.status, error.response?.data || error.message);

    // 统一错误处理
    if (error.response) {
      // 服务器响应了错误状态码
      const { status, data } = error.response;
      switch (status) {
        case 401:
          console.error("未授权，请重新登录");
          // 可以在这里处理登录过期逻辑
          break;
        case 403:
          console.error("禁止访问");
          break;
        case 404:
          console.error("请求的资源不存在");
          break;
        case 500:
          console.error("服务器内部错误");
          break;
        default:
          console.error(`请求失败: ${status}`);
      }
      return Promise.reject(data || error);
    } else if (error.request) {
      console.error("网络错误，请检查网络连接");
      return Promise.reject(new Error("网络错误，请检查网络连接"));
    } else {
      console.error("请求配置错误:", error.message);
      return Promise.reject(error);
    }
  }
);

// HTTP请求方法
export const httpClient = {
  // GET请求
  get(url, params = {}, config = {}) {
    return http.get(url, { params, ...config });
  },

  // POST请求
  post(url, data = {}, config = {}) {
    return http.post(url, data, config);
  },

  // PUT请求
  put(url, data = {}, config = {}) {
    return http.put(url, data, config);
  },

  // DELETE请求
  delete(url, config = {}) {
    return http.delete(url, config);
  },

  // PATCH请求
  patch(url, data = {}, config = {}) {
    return http.patch(url, data, config);
  },

  // 上传文件
  upload(url, formData, config = {}) {
    return http.post(url, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      },
      ...config
    });
  },

  // 下载文件
  download(url, params = {}, config = {}) {
    return http.get(url, {
      params,
      responseType: "blob",
      ...config
    });
  }
};

// 导出axios实例
export default http;
