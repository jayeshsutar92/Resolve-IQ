/**
 * index.ts
 * TypeScript interfaces mirroring the backend schemas.
 */

export interface RiskAssessment {
  id: string;
  complaint_id: string;
  severity: string;
  priority: string;
  risk_level: string;
  reasoning: string;
  recommended_action?: string;
  created_at: string;
  updated_at: string;
}

export interface Complaint {
  id: string;
  customer_name?: string;
  issue_description?: string;
  product_or_service?: string;
  date_of_incident?: string;
  additional_details?: Record<string, any>;
  original_text?: string;
  created_at: string;
  updated_at: string;
  risk_assessment?: RiskAssessment;
}

export interface ChatRequest {
  message: string;
  complaint_id?: string;
}

export interface ChatResponse {
  status: string;
  message: string;
  intent: string;
  complaint?: Complaint;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'ai';
  content: string;
  timestamp: string;
}
