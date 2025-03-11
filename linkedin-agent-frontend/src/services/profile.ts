import { apiClient } from './api/client';
import type {
  Profile,
  ProfileUpdateRequest,
  Education,
  Experience,
  Skill,
  Language,
  Certification,
  Project,
  ProfileAnalysis
} from './types';

/**
 * Profile service for handling profile-related API calls
 */
export const profileService = {
  /**
   * Get current user's profile
   * @returns Promise with profile data
   */
  async getProfile(): Promise<Profile> {
    return apiClient.get<Profile>('/profile');
  },

  /**
   * Update user profile
   * @param profileData Profile data to update
   * @returns Promise with updated profile data
   */
  async updateProfile(profileData: ProfileUpdateRequest): Promise<Profile> {
    return apiClient.put<Profile>('/profile', profileData);
  },

  /**
   * Sync profile with LinkedIn
   * @returns Promise with synced profile data
   */
  async syncWithLinkedIn(): Promise<Profile> {
    return apiClient.post<Profile>('/profile/sync-linkedin');
  },

  /**
   * Add education entry
   * @param education Education data
   * @returns Promise with created education data
   */
  async addEducation(education: Omit<Education, 'id'>): Promise<Education> {
    return apiClient.post<Education>('/profile/education', education);
  },

  /**
   * Update education entry
   * @param id Education ID
   * @param education Education data to update
   * @returns Promise with updated education data
   */
  async updateEducation(id: string, education: Partial<Omit<Education, 'id'>>): Promise<Education> {
    return apiClient.put<Education>(`/profile/education/${id}`, education);
  },

  /**
   * Delete education entry
   * @param id Education ID
   * @returns Promise with success status
   */
  async deleteEducation(id: string): Promise<{ success: boolean }> {
    return apiClient.delete<{ success: boolean }>(`/profile/education/${id}`);
  },

  /**
   * Add experience entry
   * @param experience Experience data
   * @returns Promise with created experience data
   */
  async addExperience(experience: Omit<Experience, 'id'>): Promise<Experience> {
    return apiClient.post<Experience>('/profile/experience', experience);
  },

  /**
   * Update experience entry
   * @param id Experience ID
   * @param experience Experience data to update
   * @returns Promise with updated experience data
   */
  async updateExperience(id: string, experience: Partial<Omit<Experience, 'id'>>): Promise<Experience> {
    return apiClient.put<Experience>(`/profile/experience/${id}`, experience);
  },

  /**
   * Delete experience entry
   * @param id Experience ID
   * @returns Promise with success status
   */
  async deleteExperience(id: string): Promise<{ success: boolean }> {
    return apiClient.delete<{ success: boolean }>(`/profile/experience/${id}`);
  },

  /**
   * Add skill
   * @param skill Skill data
   * @returns Promise with created skill data
   */
  async addSkill(skill: Omit<Skill, 'id' | 'endorsements'>): Promise<Skill> {
    return apiClient.post<Skill>('/profile/skills', skill);
  },

  /**
   * Update skill
   * @param id Skill ID
   * @param skill Skill data to update
   * @returns Promise with updated skill data
   */
  async updateSkill(id: string, skill: Partial<Omit<Skill, 'id' | 'endorsements'>>): Promise<Skill> {
    return apiClient.put<Skill>(`/profile/skills/${id}`, skill);
  },

  /**
   * Delete skill
   * @param id Skill ID
   * @returns Promise with success status
   */
  async deleteSkill(id: string): Promise<{ success: boolean }> {
    return apiClient.delete<{ success: boolean }>(`/profile/skills/${id}`);
  },

  /**
   * Get profile analysis
   * @returns Promise with profile analysis data
   */
  async getProfileAnalysis(): Promise<ProfileAnalysis> {
    return apiClient.get<ProfileAnalysis>('/profile/analysis');
  },

  /**
   * Get profile strength
   * @returns Promise with profile strength score
   */
  async getProfileStrength(): Promise<{ score: number; maxScore: number }> {
    return apiClient.get<{ score: number; maxScore: number }>('/profile/strength');
  },

  /**
   * Add language
   * @param language Language data
   * @returns Promise with created language data
   */
  async addLanguage(language: Omit<Language, 'id'>): Promise<Language> {
    return apiClient.post<Language>('/profile/languages', language);
  },

  /**
   * Update language
   * @param id Language ID
   * @param language Language data to update
   * @returns Promise with updated language data
   */
  async updateLanguage(id: string, language: Partial<Omit<Language, 'id'>>): Promise<Language> {
    return apiClient.put<Language>(`/profile/languages/${id}`, language);
  },

  /**
   * Delete language
   * @param id Language ID
   * @returns Promise with success status
   */
  async deleteLanguage(id: string): Promise<{ success: boolean }> {
    return apiClient.delete<{ success: boolean }>(`/profile/languages/${id}`);
  },

  /**
   * Add certification
   * @param certification Certification data
   * @returns Promise with created certification data
   */
  async addCertification(certification: Omit<Certification, 'id'>): Promise<Certification> {
    return apiClient.post<Certification>('/profile/certifications', certification);
  },

  /**
   * Update certification
   * @param id Certification ID
   * @param certification Certification data to update
   * @returns Promise with updated certification data
   */
  async updateCertification(
    id: string,
    certification: Partial<Omit<Certification, 'id'>>
  ): Promise<Certification> {
    return apiClient.put<Certification>(`/profile/certifications/${id}`, certification);
  },

  /**
   * Delete certification
   * @param id Certification ID
   * @returns Promise with success status
   */
  async deleteCertification(id: string): Promise<{ success: boolean }> {
    return apiClient.delete<{ success: boolean }>(`/profile/certifications/${id}`);
  },

  /**
   * Add project
   * @param project Project data
   * @returns Promise with created project data
   */
  async addProject(project: Omit<Project, 'id'>): Promise<Project> {
    return apiClient.post<Project>('/profile/projects', project);
  },

  /**
   * Update project
   * @param id Project ID
   * @param project Project data to update
   * @returns Promise with updated project data
   */
  async updateProject(id: string, project: Partial<Omit<Project, 'id'>>): Promise<Project> {
    return apiClient.put<Project>(`/profile/projects/${id}`, project);
  },

  /**
   * Delete project
   * @param id Project ID
   * @returns Promise with success status
   */
  async deleteProject(id: string): Promise<{ success: boolean }> {
    return apiClient.delete<{ success: boolean }>(`/profile/projects/${id}`);
  },
}; 