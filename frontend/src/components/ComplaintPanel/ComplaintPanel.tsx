/**
 * ComplaintPanel.tsx
 * The left panel displaying auto-populated complaint data.
 */

import React from 'react';
import { FileText, AlertTriangle } from 'lucide-react';
import { useAppSelector } from '../../hooks/reduxHooks';

const ComplaintPanel: React.FC = () => {
  const { activeComplaint, error } = useAppSelector((state) => state.complaint);

  const getBadgeClass = (level: string = '') => {
    const lower = level.toLowerCase();
    if (lower.includes('high') || lower.includes('p1')) return 'high';
    if (lower.includes('medium') || lower.includes('p2')) return 'medium';
    if (lower.includes('low') || lower.includes('p3')) return 'low';
    return '';
  };

  return (
    <div className="left-panel">
      <h1 style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '2rem' }}>
        Complaint Details
      </h1>

      {error && (
        <div style={{ backgroundColor: '#fee2e2', color: '#991b1b', padding: '1rem', borderRadius: '0.5rem', marginBottom: '1.5rem' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      <div className="card">
        <div className="card-title">
          <FileText size={20} color="var(--primary-color)" />
          Extracted Information
        </div>
        
        <div className="form-group">
          <label className="form-label">Customer Name</label>
          <input className="form-input" value={activeComplaint?.customer_name || ''} readOnly placeholder="Auto-populated by AI" />
        </div>
        
        <div className="form-group">
          <label className="form-label">Product / Service</label>
          <input className="form-input" value={activeComplaint?.product_or_service || ''} readOnly placeholder="Auto-populated by AI" />
        </div>
        
        <div className="form-group">
          <label className="form-label">Date of Incident</label>
          <input className="form-input" value={activeComplaint?.date_of_incident || ''} readOnly placeholder="Auto-populated by AI" />
        </div>
        
        <div className="form-group">
          <label className="form-label">Issue Description</label>
          <textarea className="form-input" value={activeComplaint?.issue_description || ''} readOnly placeholder="Auto-populated by AI" />
        </div>
      </div>

      <div className="card">
        <div className="card-title">
          <AlertTriangle size={20} color="#f59e0b" />
          AI Risk Assessment
        </div>
        
        {activeComplaint?.risk_assessment ? (
          <>
            <div style={{ display: 'flex', gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <span className="form-label">Severity</span>
                <span className={`badge ${getBadgeClass(activeComplaint.risk_assessment.severity)}`}>
                  {activeComplaint.risk_assessment.severity}
                </span>
              </div>
              <div>
                <span className="form-label">Priority</span>
                <span className={`badge ${getBadgeClass(activeComplaint.risk_assessment.priority)}`}>
                  {activeComplaint.risk_assessment.priority}
                </span>
              </div>
              <div>
                <span className="form-label">Risk Level</span>
                <span className={`badge ${getBadgeClass(activeComplaint.risk_assessment.risk_level)}`}>
                  {activeComplaint.risk_assessment.risk_level}
                </span>
              </div>
            </div>
            
            <div className="form-group">
              <label className="form-label">Reasoning</label>
              <textarea className="form-input" value={activeComplaint.risk_assessment.reasoning} readOnly />
            </div>
            
            {activeComplaint.risk_assessment.recommended_action && (
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label className="form-label">Recommended Action</label>
                <textarea className="form-input" value={activeComplaint.risk_assessment.recommended_action} readOnly />
              </div>
            )}
          </>
        ) : (
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
            Submit a complaint via chat or document upload to generate a risk assessment.
          </p>
        )}
      </div>
    </div>
  );
};

export default ComplaintPanel;
