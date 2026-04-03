import React, { useState } from 'react'
import './index.css'

interface Step {
  agent: string
  action: string
}

function App() {
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [response, setResponse] = useState('')
  const [steps, setSteps] = useState<Step[]>([])
  const [activeAgent, setActiveAgent] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    setLoading(true)
    setResponse('')
    setSteps([])
    setActiveAgent(null)

    try {
      const res = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input })
      })
      const data = await res.json()
      
      // Simulate the step-by-step pulse for the demo visual
      for (const step of data.steps) {
        setActiveAgent(step.agent)
        setSteps(prev => [...prev, step])
        await new Promise(r => setTimeout(r, 1000)) // Pause for effect
      }
      
      setResponse(data.response)
      setActiveAgent('done')
    } catch (err) {
      console.error(err)
      setResponse("System Error: Check if your backend is running.")
      setActiveAgent('error')
    } finally {
      setLoading(false)
    }
  }

  const agents = [
    { name: 'Librarian', icon: '📚', description: 'Internal Data' },
    { name: 'Scout', icon: '🔍', description: 'Web Search' },
    { name: 'CEO', icon: '🧠', description: 'Reasoning' },
    { name: 'Operator', icon: '⚙️', description: 'Workspace' }
  ]

  return (
    <div className="dashboard-container">
      <header className="header">
        <h1 className="title">Venture Assistant</h1>
        <div className="status-text">
          Target: Google Cloud Demo
        </div>
      </header>

      <div className="agent-grid">
        {agents.map(agent => (
          <div key={agent.name} className={`agent-card ${activeAgent === agent.name ? 'active' : ''}`}>
            <div className="pulse-indicator">{agent.icon}</div>
            <div className="agent-info">
              <span className="agent-name">{agent.name}</span>
              <span className="agent-desc">{agent.description}</span>
            </div>
          </div>
        ))}
      </div>

      <div className="main-content">
        <div className="mission-brief">
          <h2 className="brief-title">Response</h2>
          {response ? (
            <div className="brief-content">{response}</div>
          ) : (
            <div style={{ color: 'var(--text-secondary)' }}>
              Provide a prompt to begin coordination.
            </div>
          )}
        </div>

        <div className="execution-steps">
          <h3 className="workflow-title">Multi-Agent Workflow</h3>
          {steps.length === 0 && !loading && (
            <div style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>No active jobs.</div>
          )}
          {steps.map((step, i) => {
            const isLastStep = i === steps.length - 1;
            const isAgentCurrentlyActive = activeAgent === step.agent && isLastStep && activeAgent !== 'done';
            
            return (
              <div key={i} className={`step-item ${isAgentCurrentlyActive ? 'active-step' : ''}`}>
                <span className="step-agent">{step.agent}:</span> {step.action}
              </div>
            )
          })}
          {loading && activeAgent === null && (
            <div className="step-item">
              Initializing systems...
            </div>
          )}
        </div>
      </div>

      <form className="chat-input-wrapper" onSubmit={handleSubmit}>
        <input 
          placeholder="e.g., Prepare a brief for my meeting with Sequoia tomorrow" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button type="submit" disabled={loading}>
          {loading ? (
            <>
              <span className="spinner"></span> Running
            </>
          ) : 'Run Assistant'}
        </button>
      </form>
    </div>
  )
}

export default App
