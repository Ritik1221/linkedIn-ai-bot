import { apiClient } from './api/client';
import type {
  Connection,
  Interaction,
  InteractionType,
  ConnectionCreateRequest,
  ConnectionUpdateRequest,
  InteractionCreateRequest,
  InteractionUpdateRequest,
  ConnectionSearchParams,
  ConnectionSearchResponse,
  NetworkingStats,
  MessageTemplate,
  MessageTemplateCreateRequest,
  MessageTemplateUpdateRequest
} from './types';

/**
 * Networking service for handling networking-related API calls
 */
export const networkingService = {
  /**
   * Get all connections
   * @param params Search parameters
   * @returns Promise with connection search results
   */
  async getConnections(params: ConnectionSearchParams): Promise<ConnectionSearchResponse> {
    return apiClient.get<ConnectionSearchResponse>('/networking/connections', { params });
  },

  /**
   * Get connection by ID
   * @param id Connection ID
   * @returns Promise with connection data
   */
  async getConnection(id: string): Promise<Connection> {
    return apiClient.get<Connection>(`/networking/connections/${id}`);
  },

  /**
   * Create a new connection
   * @param connection Connection data
   * @returns Promise with created connection data
   */
  async createConnection(connection: ConnectionCreateRequest): Promise<Connection> {
    return apiClient.post<Connection>('/networking/connections', connection);
  },

  /**
   * Update a connection
   * @param id Connection ID
   * @param connection Connection data to update
   * @returns Promise with updated connection data
   */
  async updateConnection(id: string, connection: ConnectionUpdateRequest): Promise<Connection> {
    return apiClient.put<Connection>(`/networking/connections/${id}`, connection);
  },

  /**
   * Delete a connection
   * @param id Connection ID
   * @returns Promise with success status
   */
  async deleteConnection(id: string): Promise<{ success: boolean }> {
    return apiClient.delete<{ success: boolean }>(`/networking/connections/${id}`);
  },

  /**
   * Get interactions for a connection
   * @param connectionId Connection ID
   * @returns Promise with interactions data
   */
  async getInteractions(connectionId: string): Promise<Interaction[]> {
    return apiClient.get<Interaction[]>(`/networking/connections/${connectionId}/interactions`);
  },

  /**
   * Create a new interaction
   * @param interaction Interaction data
   * @returns Promise with created interaction data
   */
  async createInteraction(interaction: InteractionCreateRequest): Promise<Interaction> {
    return apiClient.post<Interaction>('/networking/interactions', interaction);
  },

  /**
   * Update an interaction
   * @param id Interaction ID
   * @param interaction Interaction data to update
   * @returns Promise with updated interaction data
   */
  async updateInteraction(id: string, interaction: InteractionUpdateRequest): Promise<Interaction> {
    return apiClient.put<Interaction>(`/networking/interactions/${id}`, interaction);
  },

  /**
   * Delete an interaction
   * @param id Interaction ID
   * @returns Promise with success status
   */
  async deleteInteraction(id: string): Promise<{ success: boolean }> {
    return apiClient.delete<{ success: boolean }>(`/networking/interactions/${id}`);
  },

  /**
   * Get networking statistics
   * @returns Promise with networking statistics
   */
  async getStats(): Promise<NetworkingStats> {
    return apiClient.get<NetworkingStats>('/networking/stats');
  },

  /**
   * Get connection suggestions
   * @param limit Number of suggestions to get
   * @returns Promise with connection suggestions
   */
  async getConnectionSuggestions(limit = 5): Promise<Connection[]> {
    return apiClient.get<Connection[]>('/networking/suggestions', { params: { limit } });
  },

  /**
   * Import connections from LinkedIn
   * @returns Promise with import result
   */
  async importFromLinkedIn(): Promise<{ success: boolean; imported: number }> {
    return apiClient.post<{ success: boolean; imported: number }>('/networking/import-linkedin');
  },

  /**
   * Get message templates
   * @returns Promise with message templates
   */
  async getMessageTemplates(): Promise<MessageTemplate[]> {
    return apiClient.get<MessageTemplate[]>('/networking/message-templates');
  },

  /**
   * Get message template by ID
   * @param id Template ID
   * @returns Promise with message template data
   */
  async getMessageTemplate(id: string): Promise<MessageTemplate> {
    return apiClient.get<MessageTemplate>(`/networking/message-templates/${id}`);
  },

  /**
   * Create a new message template
   * @param template Template data
   * @returns Promise with created template data
   */
  async createMessageTemplate(template: MessageTemplateCreateRequest): Promise<MessageTemplate> {
    return apiClient.post<MessageTemplate>('/networking/message-templates', template);
  },

  /**
   * Update a message template
   * @param id Template ID
   * @param template Template data to update
   * @returns Promise with updated template data
   */
  async updateMessageTemplate(
    id: string,
    template: MessageTemplateUpdateRequest
  ): Promise<MessageTemplate> {
    return apiClient.put<MessageTemplate>(`/networking/message-templates/${id}`, template);
  },

  /**
   * Delete a message template
   * @param id Template ID
   * @returns Promise with success status
   */
  async deleteMessageTemplate(id: string): Promise<{ success: boolean }> {
    return apiClient.delete<{ success: boolean }>(`/networking/message-templates/${id}`);
  },

  /**
   * Generate personalized message for a connection
   * @param connectionId Connection ID
   * @param purpose Message purpose
   * @returns Promise with generated message
   */
  async generateMessage(
    connectionId: string,
    purpose: 'introduction' | 'follow-up' | 'thank-you' | 'request'
  ): Promise<{ subject: string; body: string }> {
    return apiClient.post<{ subject: string; body: string }>(
      `/networking/connections/${connectionId}/generate-message`,
      { purpose }
    );
  },
}; 