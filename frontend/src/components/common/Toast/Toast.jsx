import { createContext, useCallback, useContext, useRef, useState } from 'react'
import { AnimatePresence, motion } from 'framer-motion'
import { FiCheck, FiAlertCircle, FiInfo, FiAlertTriangle, FiX } from 'react-icons/fi'
import './Toast.css'

/* ── context ───────────────────────────────────────────────────────── */

const ToastCtx = createContext(null)

/* ── icons ─────────────────────────────────────────────────────────── */

const ICONS = {
  success: FiCheck,
  error:   FiAlertCircle,
  warn:    FiAlertTriangle,
  info:    FiInfo,
}

/* ── single toast ──────────────────────────────────────────────────── */

function Toast({ id, type = 'info', message, onDismiss }) {
  const Icon = ICONS[type] ?? FiInfo
  return (
    <motion.li
      layout
      initial={{ opacity: 0, y: 32, scale: 0.9 }}
      animate={{ opacity: 1, y: 0,  scale: 1   }}
      exit={{    opacity: 0, y: 16, scale: 0.95 }}
      transition={{ type: 'spring', stiffness: 380, damping: 28 }}
      className={`toast toast--${type}`}
      role="alert"
      aria-live="assertive"
    >
      <span className="toast__icon" aria-hidden="true">
        <Icon size={14} />
      </span>
      <span className="toast__msg">{message}</span>
      <button
        className="toast__close"
        onClick={() => onDismiss(id)}
        aria-label="Dismiss notification"
      >
        <FiX size={13} />
      </button>
    </motion.li>
  )
}

/* ── provider ──────────────────────────────────────────────────────── */

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([])
  const counter             = useRef(0)

  const dismiss = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id))
  }, [])

  const toast = useCallback((message, type = 'info', duration = 4000) => {
    const id = ++counter.current
    setToasts((prev) => [...prev, { id, message, type }])
    if (duration > 0) setTimeout(() => dismiss(id), duration)
    return id
  }, [dismiss])

  /* convenience shorthands */
  toast.success = (msg, d) => toast(msg, 'success', d)
  toast.error   = (msg, d) => toast(msg, 'error',   d ?? 6000)
  toast.warn    = (msg, d) => toast(msg, 'warn',    d)
  toast.info    = (msg, d) => toast(msg, 'info',    d)

  return (
    <ToastCtx.Provider value={toast}>
      {children}
      <ul className="toast-list" aria-label="Notifications">
        <AnimatePresence mode="popLayout">
          {toasts.map((t) => (
            <Toast key={t.id} {...t} onDismiss={dismiss} />
          ))}
        </AnimatePresence>
      </ul>
    </ToastCtx.Provider>
  )
}

/* ── hook ──────────────────────────────────────────────────────────── */

export function useToast() {
  const ctx = useContext(ToastCtx)
  if (!ctx) throw new Error('useToast must be used inside <ToastProvider>')
  return ctx
}
