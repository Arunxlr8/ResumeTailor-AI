import { FiZap } from 'react-icons/fi'

export default function GenerateButton({ onClick, isLoading = false, disabled = false }) {
  return (
    <button
      type="button"
      className="ni-btn ni-btn-primary"
      onClick={onClick}
      disabled={disabled || isLoading}
      style={{ width: '100%', padding: '12px 20px', fontSize: '14px', marginTop: '6px' }}
    >
      {isLoading ? (
        <>
          <span className="ni-spinner" />
          <span>Analyzing Resume & Extracting Skills...</span>
        </>
      ) : (
        <>
          <FiZap size={16} />
          <span>Tailor & Analyze Resume</span>
        </>
      )}
    </button>
  )
}
