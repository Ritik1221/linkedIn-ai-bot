/**
 * Validation utilities for the LinkedIn AI Agent.
 * This module provides Zod validation schemas for common form inputs.
 */

import { z } from 'zod';

// Basic validation constants
const MIN_PASSWORD_LENGTH = 8;
const MAX_PASSWORD_LENGTH = 72; // Bcrypt limitation
const MIN_NAME_LENGTH = 2;
const MAX_NAME_LENGTH = 100;
const MAX_HEADLINE_LENGTH = 120;
const MAX_SUMMARY_LENGTH = 2000;
const MAX_URL_LENGTH = 255;

// Basic validation messages
const VALIDATION_MESSAGES = {
  required: 'This field is required',
  email: 'Please enter a valid email address',
  password: `Password must be between ${MIN_PASSWORD_LENGTH} and ${MAX_PASSWORD_LENGTH} characters`,
  passwordRequirements: 'Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character',
  name: `Name must be between ${MIN_NAME_LENGTH} and ${MAX_NAME_LENGTH} characters`,
  phone: 'Please enter a valid phone number',
  url: 'Please enter a valid URL',
};

/**
 * Email validation schema
 */
export const emailSchema = z
  .string()
  .min(1, { message: VALIDATION_MESSAGES.required })
  .email({ message: VALIDATION_MESSAGES.email });

/**
 * Password validation schema
 */
export const passwordSchema = z
  .string()
  .min(MIN_PASSWORD_LENGTH, { message: VALIDATION_MESSAGES.password })
  .max(MAX_PASSWORD_LENGTH, { message: VALIDATION_MESSAGES.password })
  .refine(
    (password) => {
      // At least one uppercase letter, one lowercase letter, one number, and one special character
      const hasUppercase = /[A-Z]/.test(password);
      const hasLowercase = /[a-z]/.test(password);
      const hasNumber = /[0-9]/.test(password);
      const hasSpecial = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]+/.test(password);
      return hasUppercase && hasLowercase && hasNumber && hasSpecial;
    },
    { message: VALIDATION_MESSAGES.passwordRequirements }
  );

/**
 * Name validation schema
 */
export const nameSchema = z
  .string()
  .min(MIN_NAME_LENGTH, { message: VALIDATION_MESSAGES.name })
  .max(MAX_NAME_LENGTH, { message: VALIDATION_MESSAGES.name });

/**
 * Phone validation schema
 */
export const phoneSchema = z
  .string()
  .refine(
    (phone) => {
      // Allow various phone formats with optional country code
      return /^\+?[0-9]{10,15}$/.test(phone.replace(/[\s\-\(\)]/g, ''));
    },
    { message: VALIDATION_MESSAGES.phone }
  );

/**
 * URL validation schema
 */
export const urlSchema = z
  .string()
  .url({ message: VALIDATION_MESSAGES.url })
  .max(MAX_URL_LENGTH);

/**
 * Profile headline validation schema
 */
export const headlineSchema = z
  .string()
  .max(MAX_HEADLINE_LENGTH, { message: `Headline cannot exceed ${MAX_HEADLINE_LENGTH} characters` });

/**
 * Profile summary validation schema
 */
export const summarySchema = z
  .string()
  .max(MAX_SUMMARY_LENGTH, { message: `Summary cannot exceed ${MAX_SUMMARY_LENGTH} characters` });

/**
 * Profile schema
 */
export const ProfileSchema = z.object({
  firstName: nameSchema,
  lastName: nameSchema,
  headline: headlineSchema,
  summary: summarySchema,
  email: emailSchema,
  phone: phoneSchema.optional(),
  location: z.string().optional(),
  photoUrl: urlSchema.optional().or(z.literal('')),
});

/**
 * Login schema
 */
export const LoginSchema = z.object({
  email: emailSchema,
  password: z.string().min(1, { message: VALIDATION_MESSAGES.required }),
  rememberMe: z.boolean().optional(),
});

/**
 * Registration schema
 */
export const RegisterSchema = z.object({
  firstName: nameSchema,
  lastName: nameSchema,
  email: emailSchema,
  password: passwordSchema,
  confirmPassword: z.string(),
  acceptTerms: z.boolean().refine((val) => val === true, {
    message: 'You must accept the terms and conditions',
  }),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

/**
 * Job search schema
 */
export const JobSearchSchema = z.object({
  keywords: z.string().optional(),
  location: z.string().optional(),
  radius: z.number().optional(),
  jobType: z.string().optional(),
  experienceLevel: z.string().optional(),
  datePosted: z.string().optional(),
  remoteOnly: z.boolean().optional(),
  page: z.number().optional(),
  limit: z.number().optional(),
});

/**
 * Job application schema
 */
export const JobApplicationSchema = z.object({
  jobId: z.string(),
  coverLetter: z.string().min(50, { message: 'Cover letter must be at least 50 characters' }),
  resumeUrl: urlSchema.optional(),
  phoneNumber: phoneSchema.optional(),
  availability: z.string().optional(),
  additionalInformation: z.string().optional(),
});

export default {
  emailSchema,
  passwordSchema,
  nameSchema,
  phoneSchema,
  urlSchema,
  headlineSchema,
  summarySchema,
  ProfileSchema,
  LoginSchema,
  RegisterSchema,
  JobSearchSchema,
  JobApplicationSchema,
}; 