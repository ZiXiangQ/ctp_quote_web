
/**
 * API响应类型
 */
export interface ApiResponse<T = any> {
  success?: boolean;
  ok?: boolean;
  data?: T;
  message?: string;
  error?: string;
}
