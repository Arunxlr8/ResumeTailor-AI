import { useRef, useState } from 'react'
import { FiUploadCloud, FiFileText, FiX } from 'react-icons/fi'

export default function ResumeUpload({ file, onFileChange, disabled = false }) {
  const inputRef = useRef(null)

  const handleFileChange = (e) => {
    const selected = e.target.files?.[0]
    if (selected) onFileChange(selected)
  }

  return (
    <div className="ni-card">
      <div className="ni-card-title">
        <FiFileText className="ni-card-title-icon" />
        <span>Existing Resume (Docx / PDF / TXT)</span>
      </div>

      <div className="ni-doc-upload-row">
        <span className="ni-doc-upload-label">
          {file ? file.name : "No file selected (will use default template)"}
        </span>
        {file ? (
          <button
            type="button"
            className="ni-btn ni-btn-danger"
            onClick={() => onFileChange(null)}
            disabled={disabled}
            style={{ padding: '4px 10px', fontSize: '12px' }}
          >
            <FiX size={13} /> Remove
          </button>
        ) : (
          <button
            type="button"
            className={`ni-btn ni-btn-secondary ${disabled ? 'disabled' : ''}`}
            onClick={() => !disabled && inputRef.current?.click()}
            disabled={disabled}
            style={{ padding: '6px 12px', fontSize: '12px' }}
          >
            <FiUploadCloud size={14} /> Upload Resume
          </button>
        )}
      </div>

      <input
        ref={inputRef}
        type="file"
        accept=".docx,.pdf,.txt"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />
    </div>
  )
}
