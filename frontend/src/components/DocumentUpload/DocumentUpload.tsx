/**
 * DocumentUpload.tsx
 * A component for uploading PDF/TXT documents via drag and drop.
 * Supports explicit loading animations and validation feedback.
 */

import React, { useRef, useState } from 'react';
import { UploadCloud, Loader2 } from 'lucide-react';
import { useAppDispatch, useAppSelector } from '../../hooks/reduxHooks';
import { uploadDocumentAction } from '../../store/slices/complaintSlice';

const DocumentUpload: React.FC = () => {
  const dispatch = useAppDispatch();
  const isLoading = useAppSelector((state) => state.complaint.isLoading);
  const [dragActive, setDragActive] = useState(false);
  const [fileError, setFileError] = useState<string | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = (file: File) => {
    setFileError(null);
    const validTypes = ['application/pdf', 'text/plain'];
    const hasValidExtension = file.name.endsWith('.pdf') || file.name.endsWith('.txt');
    
    if (validTypes.includes(file.type) || hasValidExtension) {
      dispatch(uploadDocumentAction(file));
    } else {
      setFileError('Invalid file type. Please upload a PDF (.pdf) or Text (.txt) document.');
    }
  };

  return (
    <div>
      <div
        className={`upload-dropzone ${dragActive ? 'drag-active' : ''}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => !isLoading && inputRef.current?.click()}
        style={{ opacity: isLoading ? 0.7 : 1, cursor: isLoading ? 'not-allowed' : 'pointer' }}
      >
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,.txt"
          multiple={false}
          onChange={handleChange}
          style={{ display: 'none' }}
        />
        {isLoading ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem' }}>
            <Loader2 className="animate-spin" size={28} color="var(--primary-color)" />
            <div className="upload-text" style={{ color: 'var(--primary-color)', fontWeight: 600 }}>
              Parsing document and extracting fields...
            </div>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.25rem' }}>
            <UploadCloud className="upload-icon" size={28} />
            <div className="upload-text">
              <strong>Click to upload</strong> or drag & drop a PDF/TXT complaint document
            </div>
            <div style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
              Supports .pdf and .txt files
            </div>
          </div>
        )}
      </div>

      {fileError && (
        <div style={{ fontSize: '0.8125rem', color: '#dc2626', marginTop: '-0.5rem', marginBottom: '1rem', textAlign: 'center' }}>
          {fileError}
        </div>
      )}
    </div>
  );
};

export default DocumentUpload;
