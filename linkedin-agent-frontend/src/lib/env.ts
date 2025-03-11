/**
 * Environment variable utilities for the LinkedIn AI Agent frontend
 * Provides type-safe access to environment variables with fallbacks
 */

// API Configuration
export const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

// Authentication
export const NEXTAUTH_URL = process.env.NEXTAUTH_URL || 'http://localhost:3000';

// LinkedIn OAuth
export const LINKEDIN_CLIENT_ID = process.env.LINKEDIN_CLIENT_ID || '';
export const LINKEDIN_CLIENT_SECRET = process.env.LINKEDIN_CLIENT_SECRET || '';

// Analytics
export const POSTHOG_KEY = process.env.NEXT_PUBLIC_POSTHOG_KEY || '';
export const POSTHOG_HOST = process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://app.posthog.com';

// Feature Flags
export const ENABLE_NETWORKING_FEATURES = 
  process.env.NEXT_PUBLIC_ENABLE_NETWORKING_FEATURES === 'true';
export const ENABLE_APPLICATION_AUTOMATION = 
  process.env.NEXT_PUBLIC_ENABLE_APPLICATION_AUTOMATION === 'true';

/**
 * Validates that required environment variables are set
 * @returns Array of missing environment variables
 */
export const validateEnv = (): string[] => {
  const requiredEnvVars = [
    'NEXT_PUBLIC_API_URL',
    'NEXTAUTH_URL',
    'NEXTAUTH_SECRET',
    'LINKEDIN_CLIENT_ID',
    'LINKEDIN_CLIENT_SECRET',
  ];
  
  return requiredEnvVars.filter(
    (envVar) => !process.env[envVar]
  );
};

/**
 * Checks if the application is running in production
 */
export const isProduction = process.env.NODE_ENV === 'production';

/**
 * Checks if the application is running in development
 */
export const isDevelopment = process.env.NODE_ENV === 'development';

/**
 * Checks if the application is running in test mode
 */
export const isTest = process.env.NODE_ENV === 'test'; 