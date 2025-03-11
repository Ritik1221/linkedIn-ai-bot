import { apiClient } from './api/client';
import type {
  DashboardStats,
  ActivityLog,
  ActivityLogSearchParams,
  ActivityLogSearchResponse,
  GoalType,
  Goal,
  GoalCreateRequest,
  GoalUpdateRequest,
  MarketReport
} from './types';

/**
 * Analytics service for handling analytics-related API calls
 */
export const analyticsService = {
  /**
   * Get dashboard statistics
   * @returns Promise with dashboard statistics
   */
  async getDashboardStats(): Promise<DashboardStats> {
    return apiClient.get<DashboardStats>('/analytics/dashboard');
  },

  /**
   * Get activity logs
   * @param params Search parameters
   * @returns Promise with activity logs
   */
  async getActivityLogs(params: ActivityLogSearchParams): Promise<ActivityLogSearchResponse> {
    return apiClient.get<ActivityLogSearchResponse>('/analytics/activity-logs', { params });
  },

  /**
   * Get available goal types
   * @returns Promise with goal types
   */
  async getGoalTypes(): Promise<GoalType[]> {
    return apiClient.get<GoalType[]>('/analytics/goal-types');
  },

  /**
   * Get user goals
   * @param status Optional status filter
   * @returns Promise with goals
   */
  async getGoals(status?: 'active' | 'completed' | 'failed'): Promise<Goal[]> {
    return apiClient.get<Goal[]>('/analytics/goals', { params: { status } });
  },

  /**
   * Get goal by ID
   * @param id Goal ID
   * @returns Promise with goal data
   */
  async getGoal(id: string): Promise<Goal> {
    return apiClient.get<Goal>(`/analytics/goals/${id}`);
  },

  /**
   * Create a new goal
   * @param goal Goal data
   * @returns Promise with created goal
   */
  async createGoal(goal: GoalCreateRequest): Promise<Goal> {
    return apiClient.post<Goal>('/analytics/goals', goal);
  },

  /**
   * Update a goal
   * @param id Goal ID
   * @param goal Goal data to update
   * @returns Promise with updated goal
   */
  async updateGoal(id: string, goal: GoalUpdateRequest): Promise<Goal> {
    return apiClient.put<Goal>(`/analytics/goals/${id}`, goal);
  },

  /**
   * Delete a goal
   * @param id Goal ID
   * @returns Promise with success status
   */
  async deleteGoal(id: string): Promise<{ success: boolean }> {
    return apiClient.delete<{ success: boolean }>(`/analytics/goals/${id}`);
  },

  /**
   * Get job market reports
   * @param industry Optional industry filter
   * @param region Optional region filter
   * @returns Promise with market reports
   */
  async getMarketReports(industry?: string, region?: string): Promise<MarketReport[]> {
    return apiClient.get<MarketReport[]>('/analytics/market-reports', {
      params: { industry, region },
    });
  },

  /**
   * Get market report by ID
   * @param id Report ID
   * @returns Promise with market report
   */
  async getMarketReport(id: string): Promise<MarketReport> {
    return apiClient.get<MarketReport>(`/analytics/market-reports/${id}`);
  },

  /**
   * Generate custom market report
   * @param params Report parameters
   * @returns Promise with generated market report
   */
  async generateMarketReport(params: {
    industry: string;
    region?: string;
    jobTitle?: string;
  }): Promise<MarketReport> {
    return apiClient.post<MarketReport>('/analytics/generate-market-report', params);
  },

  /**
   * Get application performance metrics
   * @param startDate Optional start date filter
   * @param endDate Optional end date filter
   * @returns Promise with application performance metrics
   */
  async getApplicationPerformance(
    startDate?: string,
    endDate?: string
  ): Promise<{
    totalApplications: number;
    responseRate: number;
    interviewRate: number;
    offerRate: number;
    averageTimeToResponse: number;
    applicationsBySource: Record<string, number>;
    applicationsByJobType: Record<string, number>;
  }> {
    return apiClient.get('/analytics/application-performance', {
      params: { startDate, endDate },
    });
  },

  /**
   * Get networking performance metrics
   * @param startDate Optional start date filter
   * @param endDate Optional end date filter
   * @returns Promise with networking performance metrics
   */
  async getNetworkingPerformance(
    startDate?: string,
    endDate?: string
  ): Promise<{
    totalConnections: number;
    connectionGrowthRate: number;
    interactionRate: number;
    responseRate: number;
    averageResponseTime: number;
    connectionsByIndustry: Record<string, number>;
    connectionsByCompany: Record<string, number>;
  }> {
    return apiClient.get('/analytics/networking-performance', {
      params: { startDate, endDate },
    });
  },
}; 