import { Routes, Route } from 'react-router-dom'
import { ToastProvider } from './components/common/Toast/Toast.jsx'
import WorkspacePage from './pages/WorkspacePage/WorkspacePage.jsx'
import './App.css'

export default function App() {
  return (
    <ToastProvider>
      <Routes>
        <Route path="/"  element={<WorkspacePage />} />
        <Route path="*"  element={<WorkspacePage />} />
      </Routes>
    </ToastProvider>
  )
}
