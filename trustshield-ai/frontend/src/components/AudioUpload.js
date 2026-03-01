import React, { useRef, useState, useCallback } from 'react';
import axios from 'axios';
import './AudioUpload.css';

function AudioUpload({ onAnalysisComplete, apiUrl, disabled }) {
  const [uploadedFile, setUploadedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  // Memoized file validation
  const validateFile = useCallback((file) => {
    const allowedTypes = ['audio/mpeg', 'audio/wav', 'audio/ogg', 'audio/mp4', 'audio/flac', 'audio/aac', 'audio/x-m4a'];
    const allowedExtensions = ['.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac'];
    const fileExtension = file.name.toLowerCase().substring(file.name.lastIndexOf('.'));
    
    if (!allowedTypes.includes(file.type) && !allowedExtensions.includes(fileExtension)) {
      return { valid: false, error: 'Invalid file type. Please upload an audio file (MP3, WAV, OGG, M4A, FLAC, AAC)' };
    }

    const maxSize = 50 * 1024 * 1024; // 50MB
    if (file.size > maxSize) {
      return { valid: false, error: 'File too large. Maximum size is 50MB' };
    }

    if (file.size === 0) {
      return { valid: false, error: 'File is empty' };
    }

    return { valid: true };
  }, []);

  const handleFileSelect = useCallback(async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const validation = validateFile(file);
    if (!validation.valid) {
      setError(validation.error);
      return;
    }

    setUploadedFile(file);
    setError(null);
    await uploadAndAnalyze(file);
  }, [validateFile]);

  const uploadAndAnalyze = useCallback(async (file) => {
    setIsUploading(true);
    setUploadProgress(0);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(`${apiUrl}/upload-audio`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(percentCompleted);
        },
        timeout: 120000, // 2 minute timeout for large files
      });

      // Call parent callback with results
      if (onAnalysisComplete) {
        onAnalysisComplete(response.data);
      }

    } catch (err) {
      console.error('Upload error:', err);
      let errorMessage = 'Upload failed. Please try again.';
      
      if (err.response) {
        errorMessage = err.response.data.detail || errorMessage;
      } else if (err.request) {
        errorMessage = 'Cannot connect to server. Please ensure the backend is running.';
      } else if (err.code === 'ECONNABORTED') {
        errorMessage = 'Upload timeout. File may be too large or connection is slow.';
      }
      
      setError(errorMessage);
    } finally {
      setIsUploading(false);
      setUploadProgress(0);
    }
  }, [apiUrl, onAnalysisComplete]);

  const clearFile = useCallback(() => {
    setUploadedFile(null);
    setError(null);
    setUploadProgress(0);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  }, []);

  const formatFileSize = useCallback((bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
  }, []);

  return (
    <div className="audio-upload-container">
      <input
        ref={fileInputRef}
        type="file"
        accept="audio/*,.mp3,.wav,.ogg,.m4a,.flac,.aac"
        onChange={handleFileSelect}
        style={{ display: 'none' }}
        disabled={disabled || isUploading}
        aria-label="Upload audio file"
      />
      
      <div className="upload-section">
        <button
          className="upload-button"
          onClick={() => fileInputRef.current?.click()}
          disabled={disabled || isUploading}
          title={disabled ? "Backend offline" : "Upload audio file for analysis"}
          aria-label={isUploading ? `Uploading ${uploadProgress}%` : "Upload audio file"}
        >
          {isUploading ? (
            <>
              <span className="upload-spinner" role="status" aria-live="polite">⏳</span>
              Uploading... {uploadProgress}%
            </>
          ) : (
            <>
              <span className="upload-icon" aria-hidden="true">📁</span>
              Upload Audio File
            </>
          )}
        </button>

        {uploadedFile && !isUploading && (
          <div className="uploaded-file-info" role="status" aria-live="polite">
            <div className="file-details">
              <span className="file-icon" aria-hidden="true">🎵</span>
              <div className="file-text">
                <span className="file-name" title={uploadedFile.name}>{uploadedFile.name}</span>
                <span className="file-size">{formatFileSize(uploadedFile.size)}</span>
              </div>
            </div>
            <button
              className="clear-file-button"
              onClick={clearFile}
              title="Clear file"
              aria-label="Clear uploaded file"
            >
              ✕
            </button>
          </div>
        )}

        {isUploading && (
          <div className="upload-progress-bar" role="progressbar" aria-valuenow={uploadProgress} aria-valuemin="0" aria-valuemax="100">
            <div 
              className="upload-progress-fill" 
              style={{ width: `${uploadProgress}%` }}
            />
          </div>
        )}

        {error && (
          <div className="upload-error" role="alert" aria-live="assertive">
            <span className="error-icon" aria-hidden="true">⚠️</span>
            <span className="error-message">{error}</span>
            <button 
              className="error-close" 
              onClick={() => setError(null)}
              aria-label="Dismiss error"
            >
              ✕
            </button>
          </div>
        )}
      </div>

      <div className="upload-info">
        <p className="upload-hint">
          💡 Supported formats: MP3, WAV, OGG, M4A, FLAC, AAC (Max 50MB)
        </p>
      </div>
    </div>
  );
}

export default React.memo(AudioUpload);
