/*
 * @Author: qiuzx
 * @Date: 2025-01-18
 * @Description: API服务 - TypeScript版本
 */

import type {
  ApiResponse,
  CTPStatus,
  QuoteData
} from "../types/service";
import { httpClient } from "./http";

// 重新导出类型，供其他模块使用
export type {
  ApiResponse,
  CTPStatus,
  QuoteData
} from "../types/service";

// CTP相关API
export const ctpAPI = {
  // 获取CTP状态
  async getStatus(): Promise<CTPStatus> {
    const response = await httpClient.get("/api/ctp/status");
    return response as CTPStatus;
  },

  // 模拟模式下不需要连接/断开方法

  // 订阅合约
  async subscribe(instrumentId: string): Promise<ApiResponse> {
    const response = await httpClient.post("/api/subscribe", { instrumentId });
    return response as ApiResponse;
  },

  // 取消订阅合约
  async unsubscribe(instrumentId: string): Promise<ApiResponse> {
    const response = await httpClient.post("/api/unsubscribe", { instrumentId });
    return response as ApiResponse;
  },

  // 获取已订阅的合约列表
  async getSubscriptions(): Promise<string[]> {
    const response = await httpClient.get("/api/subscriptions");
    return response as string[];
  },

  // 获取行情数据
  async getQuotes(instrumentIds: string[] = []): Promise<QuoteData[]> {
    const params = instrumentIds.length > 0 ? { instruments: instrumentIds.join(",") } : {};
    const response = await httpClient.get("/api/quotes", params);
    return response as QuoteData[];
  },

  // 获取历史行情数据
  async getHistoryQuotes(instrumentId: string, startDate: string, endDate: string): Promise<QuoteData[]> {
    const response = await httpClient.get("/api/quotes/history", {
      instrumentId,
      startDate,
      endDate
    });
    return response as QuoteData[];
  }
};

// 系统相关API
export const systemAPI = {
  // 获取系统信息
  getInfo(): Promise<ApiResponse> {
    return httpClient.get("/api/system/info");
  },

  // 获取服务器状态
  getHealth(): Promise<ApiResponse> {
    return httpClient.get("/api/health");
  },

  // 获取配置信息
  getConfig(): Promise<ApiResponse> {
    return httpClient.get("/api/config");
  },

  // 更新配置
  updateConfig(config: Record<string, any>): Promise<ApiResponse> {
    return httpClient.post("/api/config", config);
  },

  // 重启服务
  restart(): Promise<ApiResponse> {
    return httpClient.post("/api/system/restart");
  },

  // 获取日志
  getLogs(level: string = "info", limit: number = 100): Promise<ApiResponse> {
    return httpClient.get("/api/logs", { level, limit });
  }
};

// 导出所有API
export { api, httpClient };
export default {
  ctp: ctpAPI,
  system: systemAPI
};
