import { FiFileText } from 'react-icons/fi'

export default function JobDescription({ value, onChange, disabled = false }) {
  return (
    <div className="ni-card">
      <div className="ni-card-title">
        <FiFileText className="ni-card-title-icon" />
        <span>Target Job Description</span>
      </div>
      <textarea
        className="ni-textarea"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Paste the target job description here..."
        rows={6}
        disabled={disabled}
      />
    </div>
  )
}
