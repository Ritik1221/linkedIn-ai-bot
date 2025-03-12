import axios, { AxiosError, AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { Session } from 'next-auth';
import { getSession, signOut } from 'next-auth/react';
import { getEnvVar } from '@/utils/env';

// Extend Session type to include our custom properties
declare module 'next-auth' {
  interface Session {
    accessToken?: string;
    refreshToken?: string;
  }
}

// Extend AxiosRequestConfig to include retry flag
interface CustomInternalAxiosRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean;
}

// API Response type
interface APIResponse<T = any> {
  code: string;
  message: string;
  data: T;
}

// Create axios instance with default config
const api: AxiosInstance = axios.create({
  baseURL: getEnvVar('NEXT_PUBLIC_API_URL'),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  async (config) => {
    const session = await getSession();
    if (session?.accessToken) {
      config.headers.Authorization = `Bearer ${session.accessToken}`;
    }
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config as CustomInternalAxiosRequestConfig;
    
    // Handle 401 Unauthorized errors
    if (error.response?.status === 401 && originalRequest) {
      try {
        // Try to refresh the token
        const session = await getSession();
        if (session?.refreshToken) {
          const response = await axios.post<APIResponse<{ accessToken: string }>>('/api/auth/refresh', {
            refreshToken: session.refreshToken,
          });
          
          if (response.data.data.accessToken) {
            // Update the original request with new token
            originalRequest.headers.Authorization = `Bearer ${response.data.data.accessToken}`;
            // Retry the original request
            return api(originalRequest);
          }
        }
      } catch (refreshError) {
        // If refresh fails, sign out the user
        await signOut({ callbackUrl: '/login' });
        return Promise.reject(refreshError);
      }
    }

    // Handle network errors with retry logic
    if (!error.response && originalRequest && !originalRequest._retry) {
      originalRequest._retry = true;
      return new Promise((resolve) => {
        // Retry after 1 second
        setTimeout(() => {
          resolve(api(originalRequest));
        }, 1000);
      });
    }

    return Promise.reject(error);
  }
);

// API error handler
export class APIError extends Error {
  constructor(
    public status: number,
    public code: string,
    message: string,
    public data?: any
  ) {
    super(message);
    this.name = 'APIError';
  }

  static from(error: AxiosError<APIResponse>): APIError {
    const response = error.response?.data;
    return new APIError(
      error.response?.status || 500,
      response?.code || 'UNKNOWN_ERROR',
      response?.message || error.message,
      response?.data
    );
  }
}

// Generic request wrapper with error handling
async function request<T>(
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' | 'PATCH',
  url: string,
  data?: any,
  config?: Partial<CustomInternalAxiosRequestConfig>
): Promise<T> {
  try {
    const response = await api.request<APIResponse<T>>({
      method,
      url,
      data,
      ...config,
    });
    return response.data.data;
  } catch (error) {
    if (error instanceof AxiosError) {
      throw APIError.from(error);
    }
    throw error;
  }
}

// API methods
export const apiClient = {
  get: <T>(url: string, config?: Partial<CustomInternalAxiosRequestConfig>) => request<T>('GET', url, undefined, config),
  post: <T>(url: string, data?: any, config?: Partial<CustomInternalAxiosRequestConfig>) => request<T>('POST', url, data, config),
  put: <T>(url: string, data?: any, config?: Partial<CustomInternalAxiosRequestConfig>) => request<T>('PUT', url, data, config),
  patch: <T>(url: string, data?: any, config?: Partial<CustomInternalAxiosRequestConfig>) => request<T>('PATCH', url, data, config),
  delete: <T>(url: string, config?: Partial<CustomInternalAxiosRequestConfig>) => request<T>('DELETE', url, undefined, config),
}; 