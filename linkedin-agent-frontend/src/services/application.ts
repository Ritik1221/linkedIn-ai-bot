import { apiClient } from './api/client';
import type {
  Application,
  ApplicationStatus,
  ApplicationCreateRequest,
  ApplicationUpdateRequest,
  ApplicationSearchParams,
  ApplicationSearchResponse,
  ApplicationStats,
  StatusHistoryItem,
  Job
} from './types';

/**
 * Application service for handling job application-related API calls
 */
export const applicationService = {
  /**
   * Get all applications
   * @param params Search parameters
   * @returns Promise with application search results
   */
  async getApplications(params: ApplicationSearchParams): Promise<ApplicationSearchResponse> {
    return apiClient.get<ApplicationSearchResponse>('/applications', { params });
  },

  /**
   * Get application by ID
   * @param id Application ID
   * @returns Promise with application data
   */
  async getApplication(id: string): Promise<Application> {
    return apiClient.get<Application>(`/applications/${id}`);
  },

  /**
   * Create a new application
   * @param application Application data
   * @returns Promise with created application data
   */
  async createApplication(application: ApplicationCreateRequest): Promise<Application> {
    return apiClient.post<Application>('/applications', application);
  },

  /**
   * Update an application
   * @param id Application ID
   * @param application Application data to update
   * @returns Promise with updated application data
   */
  async updateApplication(id: string, application: ApplicationUpdateRequest): Promise<Application> {
    return apiClient.put<Application>(`/applications/${id}`, application);
  },

  /**
   * Delete an application
   * @param id Application ID
   * @returns Promise with success status
   */
  async deleteApplication(id: string): Promise<{ success: boolean }> {
    return apiClient.delete<{ success: boolean }>(`/applications/${id}`);
  },

  /**
   * Update application status
   * @param id Application ID
   * @param status New status
   * @param notes Optional notes about the status change
   * @returns Promise with updated application data
   */
  async updateStatus(id: string, status: ApplicationStatus, notes?: string): Promise<Application> {
    return apiClient.put<Application>(`/applications/${id}/status`, { status, notes });
  },

  /**
   * Add a note to an application
   * @param id Application ID
   * @param note Note text
   * @returns Promise with updated application data
   */
  async addNote(id: string, note: string): Promise<Application> {
    return apiClient.post<Application>(`/applications/${id}/notes`, { note });
  },

  /**
   * Get application statistics
   * @returns Promise with application statistics
   */
  async getStats(): Promise<ApplicationStats> {
    return apiClient.get<ApplicationStats>('/applications/stats');
  },

  /**
   * Upload resume for an application
   * @param id Application ID
   * @param file Resume file
   * @returns Promise with updated application data
   */
  async uploadResume(id: string, file: File): Promise<Application> {
    const formData = new FormData();
    formData.append('resume', file);
    
    return apiClient.post<Application>(`/applications/${id}/resume`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },

  /**
   * Upload cover letter for an application
   * @param id Application ID
   * @param file Cover letter file
   * @returns Promise with updated application data
   */
  async uploadCoverLetter(id: string, file: File): Promise<Application> {
    const formData = new FormData();
    formData.append('coverLetter', file);
    
    return apiClient.post<Application>(`/applications/${id}/cover-letter`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
}; 