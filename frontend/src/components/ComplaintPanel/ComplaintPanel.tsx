import React from 'react';
import { FileText, AlertTriangle, Package, UserCheck, Loader2 } from 'lucide-react';
import { useAppSelector } from '../../hooks/reduxHooks';

const ComplaintPanel: React.FC = () => {
  const { activeComplaint, isLoading, error } = useAppSelector((state) => state.complaint);

  const formatVal = (val?: string | null): string => {
    if (!val || val === 'null' || val === 'undefined') return '';
    return val;
  };

  const getBadgeClass = (level: string = '') => {
    const lower = level.toLowerCase();
    if (lower.includes('critical') || lower.includes('high') || lower.includes('p1')) return 'high';
    if (lower.includes('medium') || lower.includes('p2')) return 'medium';
    if (lower.includes('low') || lower.includes('p3')) return 'low';
    return '';
  };

  return (
    <div className="left-panel" style={{ position: 'relative' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1 style={{ fontSize: '1.5rem', fontWeight: 700 }}>
          Structured Complaint Record
        </h1>
        {activeComplaint && (
          <span style={{ fontSize: '0.75rem', backgroundColor: '#e0e7ff', color: '#3730a3', padding: '0.25rem 0.5rem', borderRadius: '0.375rem', fontWeight: 600 }}>
            ID: {activeComplaint.id.slice(0, 8)}...
          </span>
        )}
      </div>

      {error && (
        <div style={{ backgroundColor: '#fee2e2', color: '#991b1b', padding: '1rem', borderRadius: '0.5rem', marginBottom: '1.5rem', border: '1px solid #fca5a5' }}>
          <strong>Error:</strong> {error}
        </div>
      )}

      {isLoading && (
        <div style={{
          backgroundColor: 'rgba(255, 255, 255, 0.85)',
          backdropFilter: 'blur(2px)',
          padding: '1.5rem',
          borderRadius: '0.75rem',
          border: '1px solid #e0e7ff',
          marginBottom: '1.5rem',
          display: 'flex',
          alignItems: 'center',
          gap: '0.75rem',
          color: 'var(--primary-color)',
          fontWeight: 600
        }}>
          <Loader2 className="animate-spin" size={22} />
          Processing AI extraction & risk assessment...
        </div>
      )}

      <div className="card">
        <div className="card-title">
          <UserCheck size={20} color="var(--primary-color)" />
          General Reporter Info
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div className="form-group">
            <label className="form-label">Customer / Reporter Name</label>
            <input className="form-input" value={formatVal(activeComplaint?.customer_name)} readOnly placeholder="Auto-populated by AI" />
          </div>
          
          <div className="form-group">
            <label className="form-label">Complaint Source</label>
            <input className="form-input" value={formatVal(activeComplaint?.complaint_source)} readOnly placeholder="Auto-populated by AI" />
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div className="form-group">
            <label className="form-label">Complaint Type / Category</label>
            <input className="form-input" value={formatVal(activeComplaint?.complaint_type)} readOnly placeholder="Auto-populated by AI" />
          </div>
          
          <div className="form-group">
            <label className="form-label">Reported Complaint Date</label>
            <input className="form-input" value={formatVal(activeComplaint?.complaint_date)} readOnly placeholder="Auto-populated by AI" />
          </div>
        </div>
      </div>

      <div className="card">
        <div className="card-title">
          <Package size={20} color="var(--primary-color)" />
          Product & Batch Specification
        </div>
        
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
          <div className="form-group">
            <label className="form-label">Product Name / Service</label>
            <input className="form-input" value={formatVal(activeComplaint?.product_or_service)} readOnly placeholder="Auto-populated by AI" />
          </div>
          
          <div className="form-group">
            <label className="form-label">Product Strength / Dosage</label>
            <input className="form-input" value={formatVal(activeComplaint?.product_strength)} readOnly placeholder="Auto-populated by AI" />
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1rem' }}>
          <div className="form-group">
            <label className="form-label">Batch / Lot Number</label>
            <input className="form-input" value={formatVal(activeComplaint?.batch_number)} readOnly placeholder="Auto-populated by AI" />
          </div>
          
          <div className="form-group">
            <label className="form-label">Manufacturing Date</label>
            <input className="form-input" value={formatVal(activeComplaint?.manufacturing_date)} readOnly placeholder="Auto-populated by AI" />
          </div>

          <div className="form-group">
            <label className="form-label">Expiry Date</label>
            <input className="form-input" value={formatVal(activeComplaint?.expiry_date)} readOnly placeholder="Auto-populated by AI" />
          </div>
        </div>

        <div className="form-group" style={{ marginBottom: 0 }}>
          <label className="form-label">Quantity Affected</label>
          <input className="form-input" value={formatVal(activeComplaint?.quantity_affected)} readOnly placeholder="Auto-populated by AI" />
        </div>
      </div>

      <div className="card">
        <div className="card-title">
          <FileText size={20} color="var(--primary-color)" />
          Incident Details
        </div>
        
        <div className="form-group">
          <label className="form-label">Date of Incident</label>
          <input className="form-input" value={formatVal(activeComplaint?.date_of_incident)} readOnly placeholder="Auto-populated by AI" />
        </div>
        
        <div className="form-group" style={{ marginBottom: 0 }}>
          <label className="form-label">Issue Description</label>
          <textarea className="form-input" value={formatVal(activeComplaint?.issue_description)} readOnly placeholder="Auto-populated by AI" />
        </div>
      </div>

      <div className="card">
        <div className="card-title">
          <AlertTriangle size={20} color="#f59e0b" />
          Proportional AI Risk Assessment
        </div>
        
        {activeComplaint?.risk_assessment ? (
          <>
            <div style={{ display: 'flex', gap: '1.5rem', marginBottom: '1.25rem', backgroundColor: '#fafafa', padding: '0.75rem 1rem', borderRadius: '0.5rem', border: '1px solid #f3f4f6' }}>
              <div>
                <span className="form-label" style={{ marginBottom: '0.25rem' }}>Severity</span>
                <span className={`badge ${getBadgeClass(activeComplaint.risk_assessment.severity)}`}>
                  {formatVal(activeComplaint.risk_assessment.severity) || 'Not set'}
                </span>
              </div>
              <div>
                <span className="form-label" style={{ marginBottom: '0.25rem' }}>Priority</span>
                <span className={`badge ${getBadgeClass(activeComplaint.risk_assessment.priority)}`}>
                  {formatVal(activeComplaint.risk_assessment.priority) || 'Not set'}
                </span>
              </div>
              <div>
                <span className="form-label" style={{ marginBottom: '0.25rem' }}>Risk Level</span>
                <span className={`badge ${getBadgeClass(activeComplaint.risk_assessment.risk_level)}`}>
                  {formatVal(activeComplaint.risk_assessment.risk_level) || 'Not set'}
                </span>
              </div>
            </div>
            
            <div className="form-group">
              <label className="form-label">Quality Reasoning</label>
              <textarea className="form-input" value={formatVal(activeComplaint.risk_assessment.reasoning)} readOnly />
            </div>
            
            {activeComplaint.risk_assessment.recommended_action && (
              <div className="form-group" style={{ marginBottom: 0 }}>
                <label className="form-label">Recommended CAPA / QA Action</label>
                <textarea className="form-input" value={formatVal(activeComplaint.risk_assessment.recommended_action)} readOnly />
              </div>
            )}
          </>
        ) : (
          <p style={{ fontSize: '0.875rem', color: 'var(--text-secondary)' }}>
            Log a complaint or upload a document to generate an automated AI risk assessment.
          </p>
        )}
      </div>
    </div>
  );
};

export default ComplaintPanel;
