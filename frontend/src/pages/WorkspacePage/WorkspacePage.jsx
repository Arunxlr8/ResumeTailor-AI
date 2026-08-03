import { useWorkflow } from '../../hooks/useWorkflow.js'
import Navbar from '../../components/Navbar/Navbar.jsx'
import JobDescription from '../../components/JobDescription/JobDescription.jsx'
import ResumeUpload from '../../components/ResumeUpload/ResumeUpload.jsx'
import ProviderSelector from '../../components/ProviderSelector/ProviderSelector.jsx'
import GenerateButton from '../../components/GenerateButton/GenerateButton.jsx'
import Timeline from '../../components/Timeline/Timeline.jsx'
import ExecutionLogs from '../../components/ExecutionLogs/ExecutionLogs.jsx'
import HitlApproval from '../../components/HitlApproval/HitlApproval.jsx'
import ResultCard from '../../components/Result/ResultCard.jsx'

export default function WorkspacePage() {
  const wf = useWorkflow()
  const inputsDisabled = wf.isActive || wf.isCompleted

  return (
    <div className="ni-root">
      <Navbar provider={wf.provider} isActive={wf.isActive} />

      <main className="ni-content">
        {/* ── LEFT PANEL (30%) ── */}
        <section className="ni-left-panel" aria-label="Resume Inputs">
          <JobDescription
            value={wf.jobDescription}
            onChange={wf.setJobDescription}
            disabled={inputsDisabled}
          />

          <ResumeUpload
            file={wf.resumeFile}
            onFileChange={wf.setResumeFile}
            disabled={inputsDisabled}
          />

          <ProviderSelector
            selected={wf.provider}
            onSelect={wf.setProvider}
            disabled={inputsDisabled}
          />

          {wf.error && (
            <div className="ni-validation-error">
              <span>{wf.error}</span>
            </div>
          )}

          <GenerateButton
            onClick={wf.startGeneration}
            isLoading={wf.isSubmitting}
            disabled={inputsDisabled && !wf.isCompleted}
          />
        </section>

        {/* ── CENTER PANEL (50%) ── */}
        <section className="ni-center-panel" aria-label="Workflow & HITL Stage">
          {/* Timeline Pipeline Tracker */}
          <div className="ni-card">
            <div className="ni-card-title">
              <span>Workflow Pipeline Progress</span>
            </div>
            <Timeline stageStatus={wf.stageStatus} />
          </div>

          {/* Interactive Skill & Keyword HITL Approval */}
          {wf.isAwaiting && (
            <HitlApproval
              hitlStage={wf.hitlStage}
              planContent={wf.planContent}
              onApprove={wf.approveHitl}
              onRegenerate={wf.regenerateHitl}
              isApproving={wf.isApprovingHitl}
            />
          )}

          {/* Live Execution Logs */}
          <ExecutionLogs
            logs={wf.logs}
            isRunning={wf.isRunning || wf.isSubmitting}
          />
        </section>

        {/* ── RIGHT PANEL (22%) ── */}
        <section className="ni-right-panel" aria-label="Session & Results">
          {/* Active Session Info */}
          <div className="ni-card">
            <div className="ni-card-title">
              <span>Active Workflow Session</span>
            </div>
            {wf.threadId ? (
              <div className="ni-session-id-display">
                Session ID: {wf.threadId}
              </div>
            ) : (
              <div className="ni-session-no-session">
                No active session. Click 'Tailor & Analyze Resume' to start.
              </div>
            )}
          </div>

          {/* Results & Download Card */}
          {wf.isCompleted && (
            <ResultCard
              threadId={wf.threadId}
              atsResult={wf.atsResult}
              onDownloadResume={wf.handleDownloadResume}
              onReset={wf.resetWorkflow}
              isDownloadingResume={wf.isDownloadingResume}
            />
          )}
        </section>
      </main>
    </div>
  )
}
