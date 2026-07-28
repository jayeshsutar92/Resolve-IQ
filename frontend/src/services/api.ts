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
  async processChat(data: ChatRequest): Promise<ChatResponse> {
    const response = await apiClient.post<ChatResponse>('/api/chat/', data);
    return response.data;
  },

  async uploadDocument(file: File): Promise<ChatResponse> {
    const formData = new FormData();
    formData.append('file', file);
    const response = await apiClient.post<ChatResponse>('/api/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },

  async getComplaints(): Promise<Complaint[]> {
    const response = await apiClient.get<Complaint[]>('/api/complaints/');
    return response.data;
  },

  async getComplaintById(id: string): Promise<Complaint> {
    const response = await apiClient.get<Complaint>(`/api/complaints/${id}`);
    return response.data;
  },
};
