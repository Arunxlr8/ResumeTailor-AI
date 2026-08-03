import { useEffect, useRef } from 'react'
import { FiTerminal } from 'react-icons/fi'

export default function ExecutionLogs({ logs = [], isRunning = false }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
    }
  }, [logs])

  if (logs.length === 0 && !isRunning) return null

  return (
    <div className="ni-card">
      <div className="ni-card-title">
        <FiTerminal className="ni-card-title-icon" />
        <span>Execution & Workflow Logs</span>
        {isRunning && <span className="ni-health-dot healthy" style={{ marginLeft: '6px' }} />}
      </div>
      <div className="ni-log-box">
        {logs.length === 0 ? (
          <span style={{ color: 'var(--ni-text-muted)' }}>Waiting for execution events...</span>
        ) : (
          logs.map((l, i) => (
            <div key={i} style={{ marginBottom: '2px' }}>
              <span style={{ color: 'var(--ni-text-muted)', fontSize: '10px', marginRight: '6px' }}>[{l.timestamp}]</span>
              <span>{l.message}</span>
            </div>
          ))
        )}
        <div ref={bottomRef} />
      </div>
    </div>
  )
}
