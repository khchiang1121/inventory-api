import axios from 'axios';
import type { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { API_CONFIG, STORAGE_KEYS, ERROR_MESSAGES } from '../../constants';
import type { ApiError, AuthTokens } from '../../types';

class ApiClient {
  private client: AxiosInstance;
  private isRefreshing = false;
  private failedQueue: Array<{
    resolve: (value: string) => void;
    reject: (error: any) => void;
  }> = [];

  constructor() {
    this.client = axios.create({
      baseURL: API_CONFIG.BASE_URL,
      timeout: API_CONFIG.TIMEOUT,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor to add auth token
    this.client.interceptors.request.use(
      (config) => {
        const token = this.getAccessToken();
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor to handle token refresh and errors
    this.client.interceptors.response.use(
      (response) => response,
      async (error: AxiosError) => {
        const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };

        // Handle 401 errors and token refresh
        if (error.response?.status === 401 && !originalRequest._retry) {
          if (this.isRefreshing) {
            // If already refreshing, queue the request
            return new Promise((resolve, reject) => {
              this.failedQueue.push({ resolve, reject });
            }).then((token) => {
              if (originalRequest.headers) {
                originalRequest.headers.Authorization = `Bearer ${token}`;
              }
              return this.client(originalRequest);
            }).catch((err) => {
              return Promise.reject(err);
            });
          }

          originalRequest._retry = true;
          this.isRefreshing = true;

          try {
            const refreshToken = this.getRefreshToken();
            if (refreshToken) {
              const response = await axios.post(`${API_CONFIG.BASE_URL}/auth/refresh/`, {
                refresh: refreshToken,
              });

              const { access } = response.data;
              this.setTokens({ access, refresh: refreshToken });

              // Process the failed queue
              this.processQueue(null, access);

              if (originalRequest.headers) {
                originalRequest.headers.Authorization = `Bearer ${access}`;
              }
              return this.client(originalRequest);
            }
          } catch (refreshError) {
            this.processQueue(refreshError, null);
            this.clearTokens();
            window.location.href = '/login';
            return Promise.reject(refreshError);
          } finally {
            this.isRefreshing = false;
          }
        }

        return Promise.reject(this.handleError(error));
      }
    );
  }

  private processQueue(error: any, token: string | null) {
    this.failedQueue.forEach(({ resolve, reject }) => {
      if (error) {
        reject(error);
      } else {
        resolve(token!);
      }
    });

    this.failedQueue = [];
  }

  private handleError(error: AxiosError): ApiError {
    if (!error.response) {
      return {
        message: ERROR_MESSAGES.NETWORK_ERROR,
        status: 0,
      };
    }

    const { status, data } = error.response;
    let message = ERROR_MESSAGES.UNKNOWN_ERROR;

    switch (status) {
      case 400:
        message = ERROR_MESSAGES.VALIDATION_ERROR;
        break;
      case 401:
        message = ERROR_MESSAGES.UNAUTHORIZED;
        break;
      case 403:
        message = ERROR_MESSAGES.FORBIDDEN;
        break;
      case 404:
        message = ERROR_MESSAGES.NOT_FOUND;
        break;
      case 500:
        message = ERROR_MESSAGES.SERVER_ERROR;
        break;
      default:
        message = ERROR_MESSAGES.UNKNOWN_ERROR;
    }

    return {
      message: (data as any)?.message || message,
      status,
      details: (data as any)?.errors || (data as any)?.detail,
    };
  }

  // Token management methods
  private getAccessToken(): string | null {
    return localStorage.getItem(STORAGE_KEYS.AUTH_TOKEN);
  }

  private getRefreshToken(): string | null {
    return localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
  }

  public setTokens(tokens: AuthTokens): void {
    localStorage.setItem(STORAGE_KEYS.AUTH_TOKEN, tokens.access);
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, tokens.refresh);
  }

  public clearTokens(): void {
    localStorage.removeItem(STORAGE_KEYS.AUTH_TOKEN);
    localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
  }

  public isAuthenticated(): boolean {
    return !!this.getAccessToken();
  }

  // HTTP methods
  public async get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.get(url, config);
    return response.data;
  }

  public async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.post(url, data, config);
    return response.data;
  }

  public async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.put(url, data, config);
    return response.data;
  }

  public async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.patch(url, data, config);
    return response.data;
  }

  public async delete<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response: AxiosResponse<T> = await this.client.delete(url, config);
    return response.data;
  }

  // Utility methods for handling paginated responses
  public async getPaginated<T>(
    url: string,
    params?: Record<string, any>
  ): Promise<{ results: T[]; count: number; next: string | null; previous: string | null }> {
    const response = await this.get<{
      results: T[];
      count: number;
      next: string | null;
      previous: string | null;
    }>(url, { params });
    return response;
  }

  // File upload method
  public async uploadFile<T>(
    url: string,
    file: File,
    onProgress?: (progressEvent: any) => void
  ): Promise<T> {
    const formData = new FormData();
    formData.append('file', file);

    const response: AxiosResponse<T> = await this.client.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      onUploadProgress: onProgress,
    });

    return response.data;
  }

  // Bulk operation methods
  public async bulkCreate<T>(url: string, data: any[]): Promise<T[]> {
    const response: AxiosResponse<T[]> = await this.client.post(`${url}bulk_create/`, data);
    return response.data;
  }

  public async bulkUpdate<T>(url: string, data: any[]): Promise<T[]> {
    const response: AxiosResponse<T[]> = await this.client.patch(`${url}bulk_update/`, data);
    return response.data;
  }

  public async bulkDelete(url: string, ids: number[]): Promise<void> {
    await this.client.delete(`${url}bulk_delete/`, { data: { ids } });
  }

  // Health check method
  public async healthCheck(): Promise<{ status: string; timestamp: string }> {
    return this.get('/health/');
  }

  // Method to get raw axios instance for custom requests
  public getClient(): AxiosInstance {
    return this.client;
  }
}

// Create and export a singleton instance
export const apiClient = new ApiClient();
export default apiClient;