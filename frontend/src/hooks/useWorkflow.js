import { useState, useCallback, useRef } from 'react'
import {
  startWorkflow,
  resumeWorkflow,
  getWorkflowState,
  downloadResume,
  triggerDownload,
} from '../services/api.js'

export const WF_STATUS = {
  IDLE:     'idle',
  RUNNING:  'running',
  AWAITING: 'awaiting_approval',
  DONE:     'completed',
  FAILED:   'failed',
}

const INIT = {
  jobDescription: '',
  resumeFile:     null,
  templateFile:   null,
  provider:       'azure',

  status:       WF_STATUS.IDLE,
  threadId:     null,
  currentStage: null,

  hitlStage:   null,
  planContent: null,
  atsResult:   null,

  logs:          [],
  error:         null,
  executionTime: null,

  isSubmitting:        false,
  isApprovingHitl:     false,
  isDownloadingResume: false,
}

function timestamp() {
  return new Date().toLocaleTimeString('en-US', {
    hour12: false, hour: '2-digit', minute: '2-digit', second: '2-digit',
  })
}

function makeLog(message, level = 'info') {
  return { timestamp: timestamp(), message, level }
}

export function useWorkflow() {
  const [state, setState] = useState(INIT)
  const startedAtRef = useRef(null)

  const patch = useCallback((partial) => {
    setState((prev) => ({ ...prev, ...partial }))
  }, [])

  const addLog = useCallback((message, level = 'info') => {
    setState((prev) => ({
      ...prev,
      logs: [...prev.logs, makeLog(message, level)],
    }))
  }, [])

  const handleResponse = useCallback((data) => {
    const interrupted = data.is_interrupted
    const interrupt   = data.pending_interrupt?.[0]
    const stage       = interrupt?.value?.stage ?? data.current_stage

    if (interrupted && stage === 'planner') {
      patch({
        status:       WF_STATUS.AWAITING,
        currentStage: 'planner',
        hitlStage:    'planner',
        planContent:  interrupt?.value ?? {},
        isSubmitting: false,
        isApprovingHitl: false,
      })
      addLog('Extraction complete — awaiting human skill approval', 'warn')
      return
    }

    if (!interrupted && data.execution_success) {
      const elapsed = startedAtRef.current
        ? ((Date.now() - startedAtRef.current) / 1000).toFixed(1)
        : null
      patch({
        status:          WF_STATUS.DONE,
        currentStage:    null,
        hitlStage:       null,
        atsResult:       data.ats_score_result,
        executionTime:   elapsed,
        isSubmitting:    false,
        isApprovingHitl: false,
      })
      addLog('Resume generated & ATS score calculated successfully ✓', 'success')
      return
    }

    if (!interrupted && data.execution_error) {
      patch({
        status:          WF_STATUS.FAILED,
        currentStage:    null,
        error:           data.execution_error,
        isSubmitting:    false,
        isApprovingHitl: false,
      })
      addLog(`Execution failed: ${data.execution_error}`, 'error')
    }
  }, [patch, addLog])

  const setJobDescription = useCallback((v) => patch({ jobDescription: v }), [patch])
  const setResumeFile     = useCallback((f) => patch({ resumeFile: f }),      [patch])
  const setTemplateFile   = useCallback((f) => patch({ templateFile: f }),    [patch])
  const setProvider       = useCallback((p) => patch({ provider: p }),        [patch])
  const clearError        = useCallback(()  => patch({ error: null }),         [patch])

  const startGeneration = useCallback(async () => {
    let snap
    setState((prev) => { snap = prev; return prev })
    await Promise.resolve()

    if (!snap.jobDescription.trim()) {
      patch({ error: 'Paste a job description before generating.' })
      return
    }

    startedAtRef.current = Date.now()
    patch({
      status:        WF_STATUS.RUNNING,
      currentStage:  'planner',
      isSubmitting:  true,
      error:         null,
      logs:          [makeLog('Starting analysis & skill extraction...', 'info')],
      threadId:      null,
      hitlStage:     null,
      planContent:   null,
      atsResult:     null,
      executionTime: null,
    })

    try {
      addLog('Analyzing target JD and candidate resume...', 'info')
      const data = await startWorkflow({
        jobDescription: snap.jobDescription,
        resumeFile:     snap.resumeFile,
        templateFile:   snap.templateFile,
        provider:       snap.provider,
      })

      patch({ threadId: data.thread_id })
      addLog(`Session Thread ID: ${data.thread_id}`, 'success')
      handleResponse(data)
    } catch (err) {
      patch({ isSubmitting: false, status: WF_STATUS.FAILED, error: err.message })
      addLog(`Error: ${err.message}`, 'error')
    }
  }, [patch, addLog, handleResponse])

  const approveHitl = useCallback(async (hitlPayload) => {
    let snap
    setState((prev) => { snap = prev; return prev })
    await Promise.resolve()

    if (!snap.threadId) return

    patch({ isApprovingHitl: true, error: null, status: WF_STATUS.RUNNING, hitlStage: null })
    addLog('Skills approved — executing parametric resume generator & computing ATS score...', 'info')

    try {
      const data = await resumeWorkflow({
        threadId: snap.threadId,
        decision: 'approve',
        approved_skills: hitlPayload?.approved_skills,
        added_skills: hitlPayload?.added_skills,
        removed_skills: hitlPayload?.removed_skills,
        user_suggestions: hitlPayload?.user_suggestions,
      })
      handleResponse(data)
    } catch (err) {
      patch({ isApprovingHitl: false, status: WF_STATUS.FAILED, error: err.message })
      addLog(`Error: ${err.message}`, 'error')
    }
  }, [patch, addLog, handleResponse])

  const regenerateHitl = useCallback(async (feedback = '') => {
    let snap
    setState((prev) => { snap = prev; return prev })
    await Promise.resolve()

    if (!snap.threadId) return

    patch({ isApprovingHitl: true, error: null, status: WF_STATUS.RUNNING, hitlStage: null })
    addLog('Regenerating skill analysis...', 'warn')

    try {
      const data = await resumeWorkflow({
        threadId: snap.threadId,
        decision: 'regenerate',
        feedback,
      })
      handleResponse(data)
    } catch (err) {
      patch({ isApprovingHitl: false, status: WF_STATUS.FAILED, error: err.message })
      addLog(`Error: ${err.message}`, 'error')
    }
  }, [patch, addLog, handleResponse])

  const handleDownloadResume = useCallback(async () => {
    let snap
    setState((prev) => { snap = prev; return prev })
    await Promise.resolve()
    if (!snap.threadId) return

    patch({ isDownloadingResume: true })
    try {
      const blob = await downloadResume(snap.threadId)
      triggerDownload(blob, `Tailored_Resume_${snap.threadId.slice(0, 8)}.docx`)
      addLog('Resume downloaded successfully.', 'success')
    } catch (err) {
      patch({ error: `Download failed: ${err.message}` })
      addLog(`Download error: ${err.message}`, 'error')
    } finally {
      patch({ isDownloadingResume: false })
    }
  }, [patch, addLog])

  const resetWorkflow = useCallback(() => {
    startedAtRef.current = null
    setState(INIT)
  }, [])

  const isRunning   = state.status === WF_STATUS.RUNNING
  const isAwaiting  = state.status === WF_STATUS.AWAITING
  const isCompleted = state.status === WF_STATUS.DONE
  const isFailed    = state.status === WF_STATUS.FAILED

  const stageStatus = {
    planner: isCompleted || (isAwaiting && state.hitlStage !== 'planner') ? 'done' : isRunning && state.currentStage === 'planner' ? 'running' : 'pending',
    plannerApproval: isCompleted ? 'done' : isAwaiting ? 'awaiting' : 'pending',
    generator: isCompleted ? 'done' : isRunning && state.currentStage === 'generator' ? 'running' : 'pending',
    ats: isCompleted ? 'done' : 'pending',
  }

  return {
    ...state,
    stageStatus,
    isIdle:      state.status === WF_STATUS.IDLE,
    isRunning,
    isAwaiting,
    isCompleted,
    isFailed,
    isActive:    isRunning || isAwaiting || state.isSubmitting,

    setJobDescription,
    setResumeFile,
    setTemplateFile,
    setProvider,

    startGeneration,
    approveHitl,
    regenerateHitl,
    handleDownloadResume,
    resetWorkflow,
    clearError,
  }
}
