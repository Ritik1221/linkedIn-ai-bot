'use client';

import { useQuery } from '@tanstack/react-query';
import { useCallback } from 'react';
import { profileService, jobService, applicationService, analyticsService } from '@/services';

/**
 * Custom hook to fetch all dashboard data in parallel with proper caching
 * @returns Object containing all dashboard data and loading states
 */
export const useDashboardData = () => {
  // Fetch profile data
  const profileQuery = useQuery({
    queryKey: ['profile'],
    queryFn: () => profileService.getProfile(),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 60 * 60 * 1000, // 1 hour
  });

  // Fetch recent jobs
  const recentJobsQuery = useQuery({
    queryKey: ['jobs', 'recent'],
    queryFn: () => jobService.getRecentJobs({ limit: 5 }),
    staleTime: 2 * 60 * 1000, // 2 minutes
    gcTime: 30 * 60 * 1000, // 30 minutes
  });

  // Fetch applications
  const applicationsQuery = useQuery({
    queryKey: ['applications', 'recent'],
    queryFn: () => applicationService.getApplications({ limit: 10 }),
    staleTime: 5 * 60 * 1000, // 5 minutes
    gcTime: 60 * 60 * 1000, // 1 hour
  });

  // Fetch analytics data
  const analyticsQuery = useQuery({
    queryKey: ['analytics', 'dashboard'],
    queryFn: () => analyticsService.getDashboardAnalytics(),
    staleTime: 15 * 60 * 1000, // 15 minutes
    gcTime: 60 * 60 * 1000, // 1 hour
  });

  // Method to refetch all data
  const refetchAll = useCallback(() => {
    return Promise.all([
      profileQuery.refetch(),
      recentJobsQuery.refetch(),
      applicationsQuery.refetch(),
      analyticsQuery.refetch(),
    ]);
  }, [profileQuery, recentJobsQuery, applicationsQuery, analyticsQuery]);

  // Determine if any query is loading
  const isLoading = 
    profileQuery.isLoading || 
    recentJobsQuery.isLoading || 
    applicationsQuery.isLoading || 
    analyticsQuery.isLoading;

  // Determine if any query has errored
  const isError =
    profileQuery.isError ||
    recentJobsQuery.isError ||
    applicationsQuery.isError ||
    analyticsQuery.isError;

  // Combine all error messages
  const errorMessages = [
    profileQuery.error,
    recentJobsQuery.error,
    applicationsQuery.error,
    analyticsQuery.error,
  ]
    .filter(Boolean)
    .map(error => error instanceof Error ? error.message : 'Unknown error');

  return {
    // Data from queries
    profile: profileQuery.data,
    recentJobs: recentJobsQuery.data,
    applications: applicationsQuery.data,
    analytics: analyticsQuery.data,
    
    // Status information
    isLoading,
    isError,
    errorMessages,
    
    // Individual query statuses
    profileStatus: {
      isLoading: profileQuery.isLoading,
      isError: profileQuery.isError,
      error: profileQuery.error,
    },
    jobsStatus: {
      isLoading: recentJobsQuery.isLoading,
      isError: recentJobsQuery.isError,
      error: recentJobsQuery.error,
    },
    applicationsStatus: {
      isLoading: applicationsQuery.isLoading,
      isError: applicationsQuery.isError,
      error: applicationsQuery.error,
    },
    analyticsStatus: {
      isLoading: analyticsQuery.isLoading,
      isError: analyticsQuery.isError,
      error: analyticsQuery.error,
    },
    
    // Actions
    refetchAll,
  };
}; 