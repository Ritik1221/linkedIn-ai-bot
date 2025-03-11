import { apiClient } from './api/client';
import type {
  Job,
  JobSearchParams,
  JobSearchResponse,
  JobMatchAnalysis
} from './types';

/**
 * Job service for handling job-related API calls
 */
export const jobService = {
  /**
   * Search for jobs
   * @param params Search parameters
   * @returns Promise with job search results
   */
  async searchJobs(params: JobSearchParams): Promise<JobSearchResponse> {
    return apiClient.get<JobSearchResponse>('/jobs/search', { params });
  },

  /**
   * Get job by ID
   * @param id Job ID
   * @returns Promise with job data
   */
  async getJob(id: string): Promise<Job> {
    return apiClient.get<Job>(`/jobs/${id}`);
  },

  /**
   * Save job
   * @param id Job ID
   * @returns Promise with saved job data
   */
  async saveJob(id: string): Promise<Job> {
    return apiClient.post<Job>(`/jobs/${id}/save`);
  },

  /**
   * Unsave job
   * @param id Job ID
   * @returns Promise with unsaved job data
   */
  async unsaveJob(id: string): Promise<Job> {
    return apiClient.post<Job>(`/jobs/${id}/unsave`);
  },

  /**
   * Get saved jobs
   * @param page Page number
   * @param limit Items per page
   * @returns Promise with saved jobs
   */
  async getSavedJobs(page = 1, limit = 10): Promise<JobSearchResponse> {
    return apiClient.get<JobSearchResponse>('/jobs/saved', { params: { page, limit } });
  },

  /**
   * Get job recommendations
   * @param page Page number
   * @param limit Items per page
   * @returns Promise with job recommendations
   */
  async getJobRecommendations(page = 1, limit = 10): Promise<JobSearchResponse> {
    return apiClient.get<JobSearchResponse>('/jobs/recommendations', { params: { page, limit } });
  },

  /**
   * Get job match analysis
   * @param id Job ID
   * @returns Promise with job match analysis
   */
  async getJobMatchAnalysis(id: string): Promise<JobMatchAnalysis> {
    return apiClient.get<JobMatchAnalysis>(`/jobs/${id}/match-analysis`);
  },

  /**
   * Generate cover letter for job
   * @param id Job ID
   * @returns Promise with generated cover letter
   */
  async generateCoverLetter(id: string): Promise<{ coverLetter: string }> {
    return apiClient.post<{ coverLetter: string }>(`/jobs/${id}/generate-cover-letter`);
  },

  /**
   * Generate tailored resume for job
   * @param id Job ID
   * @returns Promise with tailored resume suggestions
   */
  async generateTailoredResume(id: string): Promise<{ suggestions: string }> {
    return apiClient.post<{ suggestions: string }>(`/jobs/${id}/generate-resume-suggestions`);
  },
}; 