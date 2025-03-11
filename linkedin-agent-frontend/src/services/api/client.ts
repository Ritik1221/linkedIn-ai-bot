import axios, { AxiosError, AxiosInstance, AxiosRequestConfig, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { getSession } from 'next-auth/react';

// API base URL from environment variable
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

/**
 * Create an Axios instance with default configuration
 */
const axiosInstance: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 seconds
});

/**
 * Request interceptor to add authentication token
 */
axiosInstance.interceptors.request.use(
  async (config: InternalAxiosRequestConfig) => {
    // Get the session
    const session = await getSession();
    
    // If session exists and has an access token, add it to the request headers
    if (session?.accessToken) {
      config.headers.set('Authorization', `Bearer ${session.accessToken}`);
    }
    
    return config;
  },
  (error: AxiosError) => {
    return Promise.reject(error);
  }
);

/**
 * Response interceptor to handle common errors
 */
axiosInstance.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  async (error: AxiosError) => {
    const originalRequest = error.config;
    
    // Handle 401 Unauthorized errors (token expired)
    if (error.response?.status === 401 && originalRequest) {
      // Redirect to login page or refresh token logic could be implemented here
      // For now, we'll just reject the promise
      return Promise.reject(error);
    }
    
    // Handle 403 Forbidden errors
    if (error.response?.status === 403) {
      console.error('Forbidden request:', error);
      // Handle forbidden access
    }
    
    // Handle 404 Not Found errors
    if (error.response?.status === 404) {
      console.error('Resource not found:', error);
      // Handle not found
    }
    
    // Handle 500 Internal Server Error
    if (error.response?.status === 500) {
      console.error('Server error:', error);
      // Handle server error
    }
    
    return Promise.reject(error);
  }
);

/**
 * API client for making HTTP requests
 */
export const apiClient = {
  /**
   * Make a GET request
   * @param url URL to request
   * @param config Axios request config
   * @returns Promise with response data
   */
  get: async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosInstance.get<T>(url, config);
    return response.data;
  },
  
  /**
   * Make a POST request
   * @param url URL to request
   * @param data Request body
   * @param config Axios request config
   * @returns Promise with response data
   */
  post: async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosInstance.post<T>(url, data, config);
    return response.data;
  },
  
  /**
   * Make a PUT request
   * @param url URL to request
   * @param data Request body
   * @param config Axios request config
   * @returns Promise with response data
   */
  put: async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosInstance.put<T>(url, data, config);
    return response.data;
  },
  
  /**
   * Make a PATCH request
   * @param url URL to request
   * @param data Request body
   * @param config Axios request config
   * @returns Promise with response data
   */
  patch: async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosInstance.patch<T>(url, data, config);
    return response.data;
  },
  
  /**
   * Make a DELETE request
   * @param url URL to request
   * @param config Axios request config
   * @returns Promise with response data
   */
  delete: async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    const response = await axiosInstance.delete<T>(url, config);
    return response.data;
  },
}; 