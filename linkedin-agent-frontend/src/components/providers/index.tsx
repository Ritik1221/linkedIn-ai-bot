'use client';

import React from 'react';
import { SessionProvider } from 'next-auth/react';
import { ThemeProvider } from 'next-themes';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';
import { Provider as ReduxProvider } from 'react-redux';
import { store } from '@/store';
import { AuthProvider } from '@/contexts/AuthContext';

// Create a client for React Query
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 60 * 1000, // 1 minute
      refetchOnWindowFocus: false,
    },
  },
});

/**
 * Providers component to wrap the application with all necessary providers
 * @param props Component props
 * @returns JSX element
 */
export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <SessionProvider session={null}>
      <QueryClientProvider client={queryClient}>
        <ReduxProvider store={store}>
          <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
            <AuthProvider>{children}</AuthProvider>
            <ReactQueryDevtools initialIsOpen={false} />
          </ThemeProvider>
        </ReduxProvider>
      </QueryClientProvider>
    </SessionProvider>
  );
} 