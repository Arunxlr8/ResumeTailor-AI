import { FiZap } from 'react-icons/fi'

const PROVIDER_LABELS = {
  azure:    'Azure OpenAI',
  ollama:   'Ollama (Local)',
  lmstudio: 'LM Studio (Local)',
  openai:   'OpenAI API',
}

export default function Navbar({ provider = 'azure', isActive = false }) {
  return (
    <header className="ni-header">
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <div
          style={{
            width: '36px',
            height: '36px',
            borderRadius: '50%',
            background: 'rgba(255, 255, 255, 0.2)',
            border: '2px solid rgba(255, 255, 255, 0.5)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#ffffff',
            boxShadow: '0 2px 6px rgba(0, 0, 0, 0.15)',
          }}
        >
          <FiZap size={20} />
        </div>
        <div>
          <span className="ni-header-title">Agentic Resume Tailor</span>
          <span className="ni-header-subtitle">Custom Resume Tailoring & ATS Scoring Platform</span>
        </div>
      </div>

      <div className="ni-header-spacer" />

      <div className="ni-health-indicator">
        <span className={`ni-health-dot ${isActive ? 'healthy' : 'healthy'}`} />
        <span>Provider: {PROVIDER_LABELS[provider] || provider}</span>
      </div>
    </header>
  )
}
