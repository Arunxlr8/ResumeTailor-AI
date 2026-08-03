import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:8000'

const client = axios.create({
  baseURL: BASE_URL,
  timeout: 180_000,
})

client.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error?.response?.data?.detail ||
      error?.response?.data?.message ||
      error?.message ||
      'An unexpected error occurred.'
    return Promise.reject(new Error(message))
  }
)

export async function startWorkflow({ jobDescription, resumeFile, templateFile, provider = 'azure' }) {
  const form = new FormData()
  form.append('job_description', jobDescription)
  form.append('provider', provider)
  if (resumeFile) {
    form.append('resume', resumeFile)
  }
  if (templateFile) {
    form.append('template', templateFile)
  }
  const response = await client.post('/workflow/start', form)
  return response.data
}

export async function resumeWorkflow({
  threadId,
  decision,
  feedback = '',
  approved_skills = null,
  added_skills = null,
  removed_skills = null,
  user_suggestions = null,
}) {
  if (!threadId) {
    throw new Error('threadId is required to resume a workflow.')
  }
  const body = {
    thread_id: threadId,
    decision,
    feedback,
    approved_skills,
    added_skills,
    removed_skills,
    user_suggestions,
  }
  const response = await client.post('/workflow/resume', body)
  return response.data
}

export async function getWorkflowState(threadId) {
  const response = await client.get(`/workflow/state/${threadId}`)
  return response.data
}

export async function downloadResume(threadId) {
  const response = await client.get(`/workflow/download/resume/${threadId}`, {
    responseType: 'blob',
  })
  return response.data
}

export function triggerDownload(blob, filename) {
  const url = URL.createObjectURL(blob)
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  document.body.appendChild(anchor)
  anchor.click()
  document.body.removeChild(anchor)
  URL.revokeObjectURL(url)
}
