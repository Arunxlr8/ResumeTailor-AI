import { FiZap, FiAlertCircle } from 'react-icons/fi'
import { motion, AnimatePresence } from 'framer-motion'
import './StatusBar.css'

const STATUS_MESSAGES = {
  idle:              null,
  running:           'AI is thinking...',
  awaiting_approval: 'Waiting for your approval',
  completed:         'Resume generated successfully',
  failed:            'Something went wrong',
}

const STAGE_MESSAGES = {
  planner:   'Planner is analyzing the job description...',
  generator: 'Generator is writing the Python script...',
  executor:  'Executor is building your resume...',
}

export default function StatusBar({ status, currentStage, error, isSubmitting }) {
  const showBar = status !== 'idle' || isSubmitting

  const message = isSubmitting
    ? 'Starting workflow...'
    : currentStage && status === 'running'
      ? STAGE_MESSAGES[currentStage] ?? STATUS_MESSAGES[status]
      : STATUS_MESSAGES[status]

  const isRunning  = status === 'running' || isSubmitting
  const isAwaiting = status === 'awaiting_approval'
  const isComplete = status === 'completed'
  const isFailed   = status === 'failed'

  if (!showBar && !error) return null

  return (
    <AnimatePresence>
      {(showBar || error) && (
        <motion.div
          className={`card-base status-bar ${isFailed ? 'status-bar--failed' : isComplete ? 'status-bar--done' : ''}`}
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.2 }}
        >
          {error ? (
            <div className="status-bar__error">
              <FiAlertCircle size={14} aria-hidden="true" />
              <span>{error}</span>
            </div>
          ) : (
            <>
              <div className="status-bar__row">
                <span
                  className={`status-bar__dot ${isRunning ? 'status-bar__dot--pulse' : ''} ${isComplete ? 'status-bar__dot--done' : ''} ${isFailed ? 'status-bar__dot--error' : ''} ${isAwaiting ? 'status-bar__dot--warn' : ''}`}
                  aria-hidden="true"
                />
                <span className="status-bar__message">{message}</span>
                {isRunning && (
                  <FiZap size={12} className="status-bar__zap" aria-hidden="true" />
                )}
              </div>

              {(isRunning || isAwaiting) && (
                <div className="status-bar__progress" role="progressbar" aria-label="Workflow progress">
                  {isRunning ? (
                    <div className="status-bar__progress-indeterminate" />
                  ) : (
                    <div className="status-bar__progress-fill" style={{ width: '50%' }} />
                  )}
                </div>
              )}
            </>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  )
}
