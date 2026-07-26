/**
 * api.ts
 * Axios service for making HTTP requests to the backend APIs.
 */

import axios from 'axios';
import type { ChatRequest, ChatResponse, Complaint } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  /**
   * Send a chat message (natural language logging or editing).
   */
  async processChat(data: ChatRequest): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>('/api/chat/', data);
    return response.data;
  },

  /**
   * Upload a document for extraction.
   */
  async uploadDocument(file: File): Promise<ChatResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<ChatResponse>('/api/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  /**
   * Fetch all historical complaints.
   */
  async getComplaints(): Promise<Complaint[]> {
    const response = await apiClient.get<Complaint[]>('/api/complaints/');
    return response.data;
  },

  /**
   * Fetch a specific complaint by ID.
   */
  async getComplaintById(id: string): Promise<Complaint> {
    const response = await apiClient.get<Complaint>(`/api/complaints/${id}`);
    return response.data;
  },
};
