import { apiClient } from './api/client';
import type {
  User,
  LoginRequest,
  LoginResponse,
  RegisterRequest,
  RegisterResponse,
  ForgotPasswordRequest,
  ResetPasswordRequest,
  ChangePasswordRequest,
  VerifyEmailRequest,
  UpdateProfileRequest
} from './types';

/**
 * Auth service for handling authentication-related API calls
 */
export const authService = {
  /**
   * Login with email and password
   * @param credentials Login credentials
   * @returns Promise with login response
   */
  async login(credentials: LoginRequest): Promise<LoginResponse> {
    return apiClient.post<LoginResponse>('/auth/login', credentials);
  },

  /**
   * Register a new user
   * @param userData User registration data
   * @returns Promise with registration response
   */
  async register(userData: RegisterRequest): Promise<RegisterResponse> {
    return apiClient.post<RegisterResponse>('/auth/register', userData);
  },

  /**
   * Request password reset
   * @param data Forgot password request data
   * @returns Promise with success status
   */
  async forgotPassword(data: ForgotPasswordRequest): Promise<{ success: boolean }> {
    return apiClient.post<{ success: boolean }>('/auth/forgot-password', data);
  },

  /**
   * Reset password with token
   * @param data Reset password request data
   * @returns Promise with success status
   */
  async resetPassword(data: ResetPasswordRequest): Promise<{ success: boolean }> {
    return apiClient.post<{ success: boolean }>('/auth/reset-password', data);
  },

  /**
   * Change password for logged in user
   * @param data Change password request data
   * @returns Promise with success status
   */
  async changePassword(data: ChangePasswordRequest): Promise<{ success: boolean }> {
    return apiClient.post<{ success: boolean }>('/auth/change-password', data);
  },

  /**
   * Get current user profile
   * @returns Promise with user data
   */
  async getCurrentUser(): Promise<User> {
    return apiClient.get<User>('/auth/me');
  },

  /**
   * Update user profile
   * @param data Profile update data
   * @returns Promise with updated user data
   */
  async updateProfile(data: UpdateProfileRequest): Promise<User> {
    return apiClient.put<User>('/auth/profile', data);
  },

  /**
   * Verify email with token
   * @param data Verify email request data
   * @returns Promise with success status
   */
  async verifyEmail(data: VerifyEmailRequest): Promise<{ success: boolean }> {
    return apiClient.post<{ success: boolean }>('/auth/verify-email', data);
  },

  /**
   * Resend verification email
   * @returns Promise with success status
   */
  async resendVerificationEmail(): Promise<{ success: boolean }> {
    return apiClient.post<{ success: boolean }>('/auth/resend-verification');
  },

  /**
   * Logout current user
   * @returns Promise with success status
   */
  async logout(): Promise<{ success: boolean }> {
    return apiClient.post<{ success: boolean }>('/auth/logout');
  },

  /**
   * Login with LinkedIn
   * @returns Promise with login response
   */
  async loginWithLinkedIn(): Promise<LoginResponse> {
    return apiClient.get<LoginResponse>('/auth/linkedin');
  },

  /**
   * Check if user is authenticated
   * @returns Promise with authentication status
   */
  async isAuthenticated(): Promise<boolean> {
    try {
      await this.getCurrentUser();
      return true;
    } catch (error) {
      return false;
    }
  },
}; 