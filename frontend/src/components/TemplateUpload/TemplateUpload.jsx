import { useCallback, useRef, useState } from 'react'
import { FiLayout, FiFile, FiX } from 'react-icons/fi'
import { motion, AnimatePresence } from 'framer-motion'
import './TemplateUpload.css'

const ACCEPTED = '.docx'
const MIME     = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'

function formatBytes(bytes) {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export default function TemplateUpload({ file, onFileChange, disabled = false }) {
  const inputRef     = useRef(null)
  const [isDragging, setIsDragging] = useState(false)
  const [error, setError]           = useState(null)

  const handleFile = useCallback((incoming) => {
    setError(null)
    if (incoming.type !== MIME && !incoming.name.endsWith('.docx')) {
      setError('Only DOCX templates are supported.')
      return
    }
    onFileChange(incoming)
  }, [onFileChange])

  const onInputChange = useCallback((e) => {
    const f = e.target.files?.[0]
    if (f) handleFile(f)
    e.target.value = ''
  }, [handleFile])

  const onDragOver  = useCallback((e) => { e.preventDefault(); if (!disabled) setIsDragging(true) }, [disabled])
  const onDragLeave = useCallback(() => setIsDragging(false), [])
  const onDrop      = useCallback((e) => {
    e.preventDefault()
    setIsDragging(false)
    if (disabled) return
    const f = e.dataTransfer.files?.[0]
    if (f) handleFile(f)
  }, [disabled, handleFile])

  const removeFile = useCallback((e) => {
    e.stopPropagation()
    onFileChange(null)
    setError(null)
  }, [onFileChange])

  return (
    <motion.div
      className="card-base tmpl-card"
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, delay: 0.15 }}
    >
      <div className="tmpl-card__header">
        <span className="tmpl-card__label">
          <FiLayout size={13} aria-hidden="true" />
          Resume template
        </span>
        <span className="tmpl-card__optional">optional</span>
      </div>

      <AnimatePresence mode="wait">
        {file ? (
          <motion.div
            key="preview"
            className="tmpl-card__preview"
            initial={{ opacity: 0, scale: 0.97 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.97 }}
            transition={{ duration: 0.18 }}
          >
            <div className="tmpl-card__file-icon">
              <FiFile size={16} />
              <span className="tmpl-card__file-ext">DOCX</span>
            </div>
            <div className="tmpl-card__file-info">
              <span className="tmpl-card__file-name text-truncate">{file.name}</span>
              <span className="tmpl-card__file-size">{formatBytes(file.size)}</span>
            </div>
            {!disabled && (
              <button
                className="tmpl-card__remove-btn"
                onClick={removeFile}
                aria-label="Remove template"
              >
                <FiX size={13} />
              </button>
            )}
          </motion.div>
        ) : (
          <motion.div
            key="zone"
            className={`tmpl-card__zone ${isDragging ? 'tmpl-card__zone--dragging' : ''} ${disabled ? 'tmpl-card__zone--disabled' : ''}`}
            onClick={() => !disabled && inputRef.current?.click()}
            onDragOver={onDragOver}
            onDragLeave={onDragLeave}
            onDrop={onDrop}
            role="button"
            tabIndex={disabled ? -1 : 0}
            aria-label="Upload DOCX template — click or drag and drop"
            onKeyDown={(e) => e.key === 'Enter' && !disabled && inputRef.current?.click()}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <FiLayout size={18} className="tmpl-card__zone-icon" aria-hidden="true" />
            <p className="tmpl-card__zone-title">
              {isDragging ? 'Drop template here' : 'Drag and drop a DOCX template'}
            </p>
            <p className="tmpl-card__zone-sub">or click to browse · DOCX only</p>
          </motion.div>
        )}
      </AnimatePresence>

      {error && (
        <p className="tmpl-card__error">{error}</p>
      )}

      <input
        ref={inputRef}
        type="file"
        accept={ACCEPTED}
        onChange={onInputChange}
        className="sr-only"
        aria-hidden="true"
        tabIndex={-1}
      />
    </motion.div>
  )
}
