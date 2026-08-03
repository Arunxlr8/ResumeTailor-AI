import { FiDownload, FiCheckCircle, FiRefreshCw } from 'react-icons/fi'
import AtsScoreCard from './AtsScoreCard'

export default function ResultCard({
  threadId,
  atsResult,
  onDownloadResume,
  onReset,
  isDownloadingResume = false,
}) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
      {/* Completed Banner */}
      <div className="ni-completed-banner">
        <h3><FiCheckCircle size={16} /> Resume Successfully Generated!</h3>
        <p>Tailored using python-docx parametric template grid.</p>
      </div>

      {/* ATS Score Card */}
      {atsResult && <AtsScoreCard atsResult={atsResult} />}

      {/* Download Action Card */}
      <div className="ni-card">
        <div className="ni-card-title">
          <FiDownload className="ni-card-title-icon" />
          <span>Download Output Artifact</span>
        </div>

        <div className="ni-artifact-list" style={{ marginBottom: '12px' }}>
          <div className="ni-artifact-item">
            <div className="ni-artifact-icon"><FiDownload size={18} /></div>
            <div className="ni-artifact-info">
              <div className="ni-artifact-name">Tailored_Resume.docx</div>
              <div className="ni-artifact-type">DOCX Document • Exact 2-Column Grid Layout</div>
            </div>
            <button
              type="button"
              className="ni-btn ni-btn-primary"
              onClick={onDownloadResume}
              disabled={isDownloadingResume}
              style={{ padding: '6px 12px', fontSize: '12px' }}
            >
              {isDownloadingResume ? <span className="ni-spinner" /> : <FiDownload size={13} />} Download
            </button>
          </div>
        </div>

        <div style={{ display: 'flex', justifyContent: 'flex-end' }}>
          <button
            type="button"
            className="ni-btn ni-btn-secondary"
            onClick={onReset}
            style={{ fontSize: '12px' }}
          >
            <FiRefreshCw size={13} /> Tailor Another Resume
          </button>
        </div>
      </div>
    </div>
  )
}
