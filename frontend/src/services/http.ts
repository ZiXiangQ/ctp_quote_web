/*
 * @Author: qiuzx
 * @Date: 2025-01-18
 * @Description: HTTP客户端 - TypeScript版本
 */

import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse } from "axios";

/**
 * HTTP客户端配置
 */
interface HttpClientConfig {
  baseURL: string;
  timeout: number;
  headers: Record<string, string>;
}

/**
 * HTTP响应类型
 */
interface HttpResponse<T = any> {
  data: T;
  status: number;
  statusText: string;
  headers: Record<string, string>;
}

/**
 * HTTP错误类型
 */
interface HttpError extends Error {
  response?: AxiosResponse;
  request?: any;
  config: AxiosRequestConfig;
  code?: string;
}

/**
 * HTTP客户端类
 */
class HttpClient {
  private instance: AxiosInstance;
  private config: HttpClientConfig;

  constructor(config: Partial<HttpClientConfig> = {}) {
    this.config = {
      baseURL: config.baseURL || this.getBackendUrl(),
      timeout: config.timeout || 10000,
      headers: {
        "Content-Type": "application/json",
        ...config.headers
      }
    };

    this.instance = axios.create(this.config);
    this.setupInterceptors();
  }

  /**
   * 获取后端URL
   */
  private getBackendUrl(): string {
    return localStorage.getItem("backendUrl") || "http://172.18.141.54:5004";
  }

  /**
   * 设置拦截器
   */
  private setupInterceptors(): void {
    // 请求拦截器
    this.instance.interceptors.request.use(
      (config) => {
        console.log(`HTTP Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
      },
      (error) => {
        console.error("Request error:", error);
        return Promise.reject(error);
      }
    );

    // 响应拦截器
    this.instance.interceptors.response.use(
      (response) => {
        console.log(`HTTP Response: ${response.status} ${response.config.url}`);
        return response;
      },
      (error: AxiosError) => {
        console.error("Response error:", error);

        if (error.response) {
          // 服务器响应了错误状态码
          console.error("Error status:", error.response.status);
          console.error("Error data:", error.response.data);
        } else if (error.request) {
          // 请求已发出但没有收到响应
          console.error("No response received:", error.request);
        } else {
          // 其他错误
          console.error("Error message:", error.message);
        }

        return Promise.reject(error);
      }
    );
  }

  /**
   * GET请求
   */
  public async get<T = any>(url: string, params?: Record<string, any>): Promise<T> {
    try {
      const response = await this.instance.get<T>(url, { params });
      return response.data;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  /**
   * POST请求
   */
  public async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.instance.post<T>(url, data, config);
      return response.data;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  /**
   * PUT请求
   */
  public async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.instance.put<T>(url, data, config);
      return response.data;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  /**
   * DELETE请求
   */
  public async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    try {
      const response = await this.instance.delete<T>(url, config);
      return response.data;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  /**
   * 上传文件
   */
  public async upload<T = any>(
    url: string,
    formData: FormData,
    config?: AxiosRequestConfig & { onUploadProgress?: (progressEvent: any) => void }
  ): Promise<T> {
    try {
      const response = await this.instance.post<T>(url, formData, {
        headers: {
          "Content-Type": "multipart/form-data"
        },
        ...config
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  /**
   * 下载文件
   */
  public async download(url: string, params?: Record<string, any>): Promise<Blob> {
    try {
      const response = await this.instance.get(url, {
        params,
        responseType: "blob"
      });
      return response.data;
    } catch (error) {
      throw this.handleError(error as AxiosError);
    }
  }

  /**
   * 处理错误
   */
  private handleError(error: AxiosError): HttpError {
    const httpError: HttpError = {
      name: "HttpError",
      message: error.message || "HTTP请求失败",
      response: error.response,
      request: error.request,
      config: error.config!,
      code: error.code
    };

    if (error.response) {
      httpError.message = `HTTP ${error.response.status}: ${error.response.statusText}`;
    } else if (error.request) {
      httpError.message = "网络连接失败，请检查网络设置";
    }

    return httpError;
  }

  /**
   * 更新基础URL
   */
  public updateBaseURL(baseURL: string): void {
    this.instance.defaults.baseURL = baseURL;
  }

  /**
   * 获取Axios实例
   */
  public getInstance(): AxiosInstance {
    return this.instance;
  }
}

// 创建默认实例
const httpClient = new HttpClient();

// 导出实例和类
export { httpClient, HttpClient };
export type { HttpClientConfig, HttpError, HttpResponse };
