'use client';

import React, { useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import Link from 'next/link';
import Image from 'next/image';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { useAuth } from '@/contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';

// Reset password form schema
const resetPasswordSchema = z
  .object({
    password: z.string().min(8, 'Password must be at least 8 characters'),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: 'Passwords do not match',
    path: ['confirmPassword'],
  });

// Reset password form values type
type ResetPasswordFormValues = z.infer<typeof resetPasswordSchema>;

/**
 * Reset password page component
 * @returns JSX element
 */
export default function ResetPasswordPage() {
  const { resetPassword } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const token = searchParams.get('token');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Initialize form
  const form = useForm<ResetPasswordFormValues>({
    resolver: zodResolver(resetPasswordSchema),
    defaultValues: {
      password: '',
      confirmPassword: '',
    },
  });

  /**
   * Handle form submission
   * @param values Form values
   */
  const onSubmit = async (values: ResetPasswordFormValues) => {
    if (!token) {
      setError('Invalid or missing reset token. Please request a new password reset link.');
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      
      await resetPassword(token, values.password);
      
      router.push('/auth/login?reset=success');
    } catch (error: any) {
      setError(error.message || 'Failed to reset password. Please try again.');
      console.error('Password reset error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // If no token is provided, show an error
  if (!token) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background px-4 py-12 sm:px-6 lg:px-8">
        <Card className="w-full max-w-md">
          <CardHeader className="space-y-1">
            <div className="flex justify-center mb-6">
              <Image
                src="/logo.svg"
                alt="LinkedIn AI Agent Logo"
                width={64}
                height={64}
                className="h-16 w-auto"
              />
            </div>
            <CardTitle className="text-2xl font-bold text-center">
              Invalid Reset Link
            </CardTitle>
            <CardDescription className="text-center">
              The password reset link is invalid or has expired
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="mb-4 rounded-md bg-destructive/15 p-3 text-sm text-destructive">
              Invalid or missing reset token. Please request a new password reset link.
            </div>
            <Button
              className="w-full"
              onClick={() => router.push('/auth/forgot-password')}
            >
              Request New Reset Link
            </Button>
          </CardContent>
          <CardFooter className="flex justify-center">
            <p className="text-sm text-muted-foreground">
              Remember your password?{' '}
              <Link
                href="/auth/login"
                className="font-medium text-primary hover:underline"
              >
                Back to login
              </Link>
            </p>
          </CardFooter>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4 py-12 sm:px-6 lg:px-8">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-1">
          <div className="flex justify-center mb-6">
            <Image
              src="/logo.svg"
              alt="LinkedIn AI Agent Logo"
              width={64}
              height={64}
              className="h-16 w-auto"
            />
          </div>
          <CardTitle className="text-2xl font-bold text-center">
            Reset your password
          </CardTitle>
          <CardDescription className="text-center">
            Enter your new password below
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 rounded-md bg-destructive/15 p-3 text-sm text-destructive">
              {error}
            </div>
          )}
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="password"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>New Password</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="••••••••"
                        type="password"
                        autoComplete="new-password"
                        disabled={isLoading}
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="confirmPassword"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Confirm New Password</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="••••••••"
                        type="password"
                        autoComplete="new-password"
                        disabled={isLoading}
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <Button
                type="submit"
                className="w-full"
                disabled={isLoading}
              >
                {isLoading ? 'Resetting...' : 'Reset Password'}
              </Button>
            </form>
          </Form>
        </CardContent>
        <CardFooter className="flex justify-center">
          <p className="text-sm text-muted-foreground">
            Remember your password?{' '}
            <Link
              href="/auth/login"
              className="font-medium text-primary hover:underline"
            >
              Back to login
            </Link>
          </p>
        </CardFooter>
      </Card>
    </div>
  );
} 