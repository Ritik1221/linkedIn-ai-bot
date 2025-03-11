'use client';

import React, { useState } from 'react';
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

// Forgot password form schema
const forgotPasswordSchema = z.object({
  email: z.string().email('Please enter a valid email address'),
});

// Forgot password form values type
type ForgotPasswordFormValues = z.infer<typeof forgotPasswordSchema>;

/**
 * Forgot password page component
 * @returns JSX element
 */
export default function ForgotPasswordPage() {
  const { requestPasswordReset } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Initialize form
  const form = useForm<ForgotPasswordFormValues>({
    resolver: zodResolver(forgotPasswordSchema),
    defaultValues: {
      email: '',
    },
  });

  /**
   * Handle form submission
   * @param values Form values
   */
  const onSubmit = async (values: ForgotPasswordFormValues) => {
    try {
      setIsLoading(true);
      setError(null);
      setSuccess(null);
      
      await requestPasswordReset(values.email);
      
      setSuccess('Password reset instructions have been sent to your email.');
      form.reset();
    } catch (error: any) {
      setError(error.message || 'Failed to request password reset. Please try again.');
      console.error('Password reset request error:', error);
    } finally {
      setIsLoading(false);
    }
  };

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
            Forgot your password?
          </CardTitle>
          <CardDescription className="text-center">
            Enter your email address and we'll send you a link to reset your password
          </CardDescription>
        </CardHeader>
        <CardContent>
          {error && (
            <div className="mb-4 rounded-md bg-destructive/15 p-3 text-sm text-destructive">
              {error}
            </div>
          )}
          {success && (
            <div className="mb-4 rounded-md bg-green-500/15 p-3 text-sm text-green-600">
              {success}
            </div>
          )}
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Email</FormLabel>
                    <FormControl>
                      <Input
                        placeholder="name@example.com"
                        type="email"
                        autoComplete="email"
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
                {isLoading ? 'Sending...' : 'Send reset link'}
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