import { FiActivity, FiUserCheck, FiCode, FiAward } from 'react-icons/fi'

const STAGES = [
  { key: 'planner', label: '1. Skill Extraction & Keyword Gap Analysis', desc: 'Parses resume, extracts skills & matches JD keywords', Icon: FiActivity },
  { key: 'plannerApproval', label: '2. Human-in-the-Loop Review', desc: 'Approve skills, add custom keywords & suggestions', Icon: FiUserCheck },
  { key: 'generator', label: '3. Parametric Resume Compilation', desc: 'Generates DOCX via python-docx template tool', Icon: FiCode },
  { key: 'ats', label: '4. ATS Match Score Evaluation', desc: 'Computes ATS score %, keyword density & breakdown', Icon: FiAward },
]

export default function Timeline({ stageStatus }) {
  return (
    <div className="ni-pipeline-stages">
      {STAGES.map((s) => {
        const st = stageStatus?.[s.key] || 'pending'
        let cardState = ''
        if (st === 'running' || st === 'awaiting') cardState = 'running'
        if (st === 'done') cardState = 'completed'
        if (st === 'error') cardState = 'failed'

        return (
          <div key={s.key} className={`ni-stage-card ${cardState}`}>
            <div className="ni-stage-icon">
              <s.Icon size={16} />
            </div>
            <div className="ni-stage-info">
              <div className="ni-stage-name">{s.label}</div>
              <div className="ni-stage-desc">{s.desc}</div>
            </div>
            <span className={`ni-stage-badge ${st === 'awaiting' ? 'running' : st === 'done' ? 'completed' : st}`}>
              {st === 'awaiting' ? 'Awaiting Input' : st === 'done' ? 'Completed' : st === 'running' ? 'Running' : 'Pending'}
            </span>
          </div>
        )
      })}
    </div>
  )
}
