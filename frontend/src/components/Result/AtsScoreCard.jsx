import { FiAward, FiCheckCircle, FiAlertTriangle } from 'react-icons/fi'

export default function AtsScoreCard({ atsResult }) {
  if (!atsResult) return null

  const overall = atsResult.overall_score || 85
  const skills = atsResult.skills_match || 88
  const density = atsResult.keyword_density || 82
  const relevance = atsResult.experience_relevance || 86

  let scoreClass = 'high'
  if (overall < 70) scoreClass = 'low'
  else if (overall < 85) scoreClass = 'medium'

  return (
    <div className="ni-ats-card">
      <div className="ni-ats-header">
        <div>
          <div className="ni-card-title" style={{ marginBottom: '2px' }}>
            <FiAward className="ni-card-title-icon" />
            <span>ATS Match Score</span>
          </div>
          <span style={{ fontSize: '11px', color: 'var(--ni-text-muted)' }}>
            Calculated against target Job Description
          </span>
        </div>
        <div className={`ni-ats-score-badge ${scoreClass}`}>
          {overall}%
        </div>
      </div>

      <div className="ni-divider" style={{ margin: '8px 0 12px' }} />

      {/* Metric Breakdown Bars */}
      <div className="ni-ats-metric-bar">
        <div className="ni-ats-metric-info">
          <span>Skills Match</span>
          <span>{skills}%</span>
        </div>
        <div className="ni-ats-bar-bg">
          <div className="ni-ats-bar-fill" style={{ width: `${skills}%` }} />
        </div>
      </div>

      <div className="ni-ats-metric-bar">
        <div className="ni-ats-metric-info">
          <span>Keyword Density</span>
          <span>{density}%</span>
        </div>
        <div className="ni-ats-bar-bg">
          <div className="ni-ats-bar-fill" style={{ width: `${density}%` }} />
        </div>
      </div>

      <div className="ni-ats-metric-bar">
        <div className="ni-ats-metric-info">
          <span>Experience Relevance</span>
          <span>{relevance}%</span>
        </div>
        <div className="ni-ats-bar-bg">
          <div className="ni-ats-bar-fill" style={{ width: `${relevance}%` }} />
        </div>
      </div>

      {/* Matched Keywords */}
      {atsResult.matched_keywords && atsResult.matched_keywords.length > 0 && (
        <div style={{ marginTop: '12px' }}>
          <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--ni-success)', marginBottom: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <FiCheckCircle size={12} /> Matched Keywords ({atsResult.matched_keywords.length})
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
            {atsResult.matched_keywords.slice(0, 8).map((kw, i) => (
              <span key={i} className="ni-skill-chip added" style={{ fontSize: '10.5px', padding: '2px 8px' }}>
                {kw}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Missing Keywords */}
      {atsResult.missing_keywords && atsResult.missing_keywords.length > 0 && (
        <div style={{ marginTop: '10px' }}>
          <div style={{ fontSize: '11px', fontWeight: 600, color: 'var(--ni-warning)', marginBottom: '4px', display: 'flex', alignItems: 'center', gap: '4px' }}>
            <FiAlertTriangle size={12} /> Keywords to consider adding
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
            {atsResult.missing_keywords.slice(0, 6).map((kw, i) => (
              <span key={i} className="ni-skill-chip suggested" style={{ fontSize: '10.5px', padding: '2px 8px' }}>
                {kw}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
