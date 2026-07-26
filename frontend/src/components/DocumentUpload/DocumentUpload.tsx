/**
 * DocumentUpload.tsx
 * A component for uploading PDF/TXT documents via drag and drop.
 */

import React, { useRef, useState } from 'react';
import { UploadCloud } from 'lucide-react';
import { useAppDispatch, useAppSelector } from '../../hooks/reduxHooks';
import { uploadDocumentAction } from '../../store/slices/complaintSlice';

const DocumentUpload: React.FC = () => {
  const dispatch = useAppDispatch();
  const isLoading = useAppSelector((state) => state.complaint.isLoading);
  const [dragActive, setDragActive] = useState(false);
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
    if (file.type === 'application/pdf' || file.type === 'text/plain') {
      dispatch(uploadDocumentAction(file));
    } else {
      alert('Only PDF or TXT files are supported.');
    }
  };

  return (
    <div
      className={`upload-dropzone ${dragActive ? 'drag-active' : ''}`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.txt"
        multiple={false}
        onChange={handleChange}
        style={{ display: 'none' }}
      />
      <UploadCloud className="upload-icon" size={28} />
      <div className="upload-text">
        {isLoading ? 'Processing document...' : 'Drag & drop a document or click to browse'}
      </div>
    </div>
  );
};

export default DocumentUpload;
