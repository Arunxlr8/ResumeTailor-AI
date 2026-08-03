import { useState } from 'react'
import { FiCheck, FiPlus, FiX, FiZap, FiEdit3, FiLoader } from 'react-icons/fi'

export default function HitlApproval({
  hitlStage,
  planContent,
  onApprove,
  onRegenerate,
  isApproving = false,
}) {
  if (!hitlStage) return null

  const output = planContent?.output || planContent || {}
  const extracted = output.extracted_skills || ["Python", "FastAPI", "LangChain", "RAG", "Docker", "React"]
  const suggested = output.suggested_skills || ["Google ADK", "MCP", "vLLM", "ChromaDB", "Multi-Agent Orchestration"]

  const [skills, setSkills] = useState([...new Set([...extracted, ...suggested])])
  const [removed, setRemoved] = useState([])
  const [customSkill, setCustomSkill] = useState('')
  const [userSuggestions, setUserSuggestions] = useState('')

  const toggleSkill = (skill) => {
    if (skills.includes(skill)) {
      setSkills(skills.filter((s) => s !== skill))
      setRemoved([...removed, skill])
    } else {
      setSkills([...skills, skill])
      setRemoved(removed.filter((s) => s !== skill))
    }
  }

  const handleAddCustom = (e) => {
    e.preventDefault()
    if (customSkill.trim() && !skills.includes(customSkill.trim())) {
      setSkills([...skills, customSkill.trim()])
      setCustomSkill('')
    }
  }

  const handleApproveClick = () => {
    onApprove({
      approved_skills: skills,
      added_skills: skills.filter((s) => !extracted.includes(s)),
      removed_skills: removed,
      user_suggestions: userSuggestions,
    })
  }

  return (
    <div className="ni-card" style={{ borderLeft: '4px solid var(--ni-primary)' }}>
      <div className="ni-card-title">
        <FiZap className="ni-card-title-icon" />
        <span>Human-in-the-Loop: Skill & Keyword Approval</span>
      </div>

      <p style={{ fontSize: '12px', color: 'var(--ni-text-secondary)', marginBottom: '12px' }}>
        Review extracted skills and suggested JD keywords. Click chips to enable/disable, add custom keywords, or provide suggestions before generating your resume.
      </p>

      {/* Skills Chip List */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px', marginBottom: '14px' }}>
        {skills.map((skill) => {
          const isSuggested = suggested.includes(skill)
          return (
            <span
              key={skill}
              className={`ni-skill-chip ${isSuggested ? 'suggested' : 'current'}`}
              onClick={() => toggleSkill(skill)}
              title="Click to remove"
            >
              {skill} <FiX size={12} />
            </span>
          )
        })}

        {removed.map((skill) => (
          <span
            key={skill}
            className="ni-skill-chip removed"
            onClick={() => toggleSkill(skill)}
            title="Click to re-add"
          >
            + {skill}
          </span>
        ))}
      </div>

      {/* Add Custom Skill Form */}
      <form onSubmit={handleAddCustom} style={{ display: 'flex', gap: '6px', marginBottom: '14px' }}>
        <input
          type="text"
          className="ni-input"
          value={customSkill}
          onChange={(e) => setCustomSkill(e.target.value)}
          placeholder="Add additional skill or keyword..."
          style={{ flex: 1, padding: '6px 10px', fontSize: '12px' }}
        />
        <button type="submit" className="ni-btn ni-btn-secondary" style={{ padding: '6px 12px', fontSize: '12px' }}>
          <FiPlus size={13} /> Add Skill
        </button>
      </form>

      {/* User Suggestions Input */}
      <div style={{ marginBottom: '14px' }}>
        <label style={{ display: 'flex', alignItems: 'center', gap: '4px', fontSize: '11px', fontWeight: 600, color: 'var(--ni-text-secondary)', marginBottom: '4px' }}>
          <FiEdit3 size={12} /> Custom Instructions & Suggestions:
        </label>
        <textarea
          className="ni-textarea"
          value={userSuggestions}
          onChange={(e) => setUserSuggestions(e.target.value)}
          placeholder="e.g. Highlight micro-services experience, emphasize automotive domain leadership..."
          rows={2}
          style={{ minHeight: '60px', fontSize: '12px' }}
        />
      </div>

      {/* Action Buttons */}
      <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
        <button
          type="button"
          className="ni-btn ni-btn-secondary"
          onClick={() => onRegenerate(userSuggestions)}
          disabled={isApproving}
        >
          Regenerate
        </button>
        <button
          type="button"
          className="ni-btn ni-btn-primary"
          onClick={handleApproveClick}
          disabled={isApproving}
        >
          {isApproving ? <span className="ni-spinner" /> : <FiCheck size={14} />} Approve & Generate Resume
        </button>
      </div>
    </div>
  )
}
