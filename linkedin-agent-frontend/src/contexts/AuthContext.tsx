'use client';

import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useSession, signOut } from 'next-auth/react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth';

// Define the authentication context type
interface AuthContextType {
  isAuthenticated: boolean;
  isLoading: boolean;
  user: any | null;
  login: (email: string, password: string) => Promise<any>;
  loginWithLinkedIn: () => Promise<any>;
  register: (userData: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
  }) => Promise<any>;
  logout: () => Promise<void>;
  requestPasswordReset: (email: string) => Promise<any>;
  resetPassword: (token: string, newPassword: string) => Promise<any>;
}

// Create the authentication context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Authentication context provider props
interface AuthProviderProps {
  children: ReactNode;
}

/**
 * Authentication context provider component
 * @param props Component props
 * @returns JSX element
 */
export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const { data: session, status } = useSession();
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const router = useRouter();

  // Check if the user is authenticated
  const isAuthenticated = status === 'authenticated' && !!session;

  // Set loading state based on session status
  useEffect(() => {
    setIsLoading(status === 'loading');
  }, [status]);

  /**
   * Login with email and password
   * @param email User email
   * @param password User password
   * @returns Promise with login result
   */
  const login = async (email: string, password: string) => {
    try {
      setIsLoading(true);
      const result = await authService.login(email, password);
      
      if (result?.error) {
        throw new Error(result.error);
      }
      
      return result;
    } catch (error) {
      console.error('Login error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Login with LinkedIn OAuth
   * @returns Promise with login result
   */
  const loginWithLinkedIn = async () => {
    try {
      setIsLoading(true);
      return await authService.loginWithLinkedIn();
    } catch (error) {
      console.error('LinkedIn login error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Register a new user
   * @param userData User registration data
   * @returns Promise with registration result
   */
  const register = async (userData: {
    email: string;
    password: string;
    firstName: string;
    lastName: string;
  }) => {
    try {
      setIsLoading(true);
      return await authService.register(userData);
    } catch (error) {
      console.error('Registration error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Logout the current user
   * @returns Promise with logout result
   */
  const logout = async () => {
    try {
      setIsLoading(true);
      await signOut({ redirect: false });
      router.push('/');
    } catch (error) {
      console.error('Logout error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Request password reset
   * @param email User email
   * @returns Promise with password reset request result
   */
  const requestPasswordReset = async (email: string) => {
    try {
      setIsLoading(true);
      return await authService.requestPasswordReset(email);
    } catch (error) {
      console.error('Password reset request error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Reset password with token
   * @param token Reset token
   * @param newPassword New password
   * @returns Promise with password reset result
   */
  const resetPassword = async (token: string, newPassword: string) => {
    try {
      setIsLoading(true);
      return await authService.resetPassword(token, newPassword);
    } catch (error) {
      console.error('Password reset error:', error);
      throw error;
    } finally {
      setIsLoading(false);
    }
  };

  // Context value
  const value: AuthContextType = {
    isAuthenticated,
    isLoading,
    user: session?.user || null,
    login,
    loginWithLinkedIn,
    register,
    logout,
    requestPasswordReset,
    resetPassword,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

/**
 * Hook to use the authentication context
 * @returns Authentication context
 * @throws Error if used outside of AuthProvider
 */
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
}; 