import { FiCpu } from 'react-icons/fi'

const PROVIDERS = [
  { id: 'azure', label: 'Azure OpenAI' },
  { id: 'ollama', label: 'Ollama' },
  { id: 'lmstudio', label: 'LM Studio' },
  { id: 'openai', label: 'OpenAI API' },
]

export default function ProviderSelector({ selected, onSelect, disabled = false }) {
  return (
    <div className="ni-card">
      <div className="ni-card-title">
        <FiCpu className="ni-card-title-icon" />
        <span>Select LLM Provider</span>
      </div>
      <div className="ni-mode-row" role="radiogroup">
        {PROVIDERS.map((p) => {
          const isActive = selected === p.id
          return (
            <button
              key={p.id}
              type="button"
              className={`ni-mode-chip ${isActive ? 'active' : ''}`}
              onClick={() => !disabled && onSelect(p.id)}
              disabled={disabled}
              role="radio"
              aria-checked={isActive}
            >
              {p.label}
            </button>
          )
        })}
      </div>
    </div>
  )
}
