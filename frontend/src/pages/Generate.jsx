import { useEffect, useRef, useState } from 'react'
import { generatePost, getPlatformStatus } from '../api'
import { PLATFORM_ICONS } from '../components/Icons'
import { PLATFORMS } from '../constants'
import './Generate.css'

const LOADING_STEPS = [
  'ANALYZING STORY BRIEF...',
  'CRAFTING OPTIMIZED POST VARIATIONS...',
  'GENERATING VISUAL ASSET...',
]

function Generate() {
  const [topic, setTopic] = useState('')
  const [keywords, setKeywords] = useState('')
  const [link, setLink] = useState('')
  const [selected, setSelected] = useState(PLATFORMS.map((p) => p.key))
  const [platformStatus, setPlatformStatus] = useState({})
  const [loading, setLoading] = useState(false)
  const [loadingStep, setLoadingStep] = useState(0)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)
  const [aspectRatio, setAspectRatio] = useState('landscape')
  const [toast, setToast] = useState(null)
  const stepInterval = useRef(null)

  useEffect(() => {
    getPlatformStatus().then(setPlatformStatus).catch(() => {})
  }, [])

  useEffect(() => {
    if (!toast) return
    const timer = setTimeout(() => setToast(null), 2500)
    return () => clearTimeout(timer)
  }, [toast])

  function togglePlatform(key) {
    setSelected((prev) => (prev.includes(key) ? prev.filter((k) => k !== key) : [...prev, key]))
  }

  function toggleSelectAll() {
    setSelected((prev) => (prev.length === PLATFORMS.length ? [] : PLATFORMS.map((p) => p.key)))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setLoadingStep(0)
    setError(null)
    setResult(null)

    stepInterval.current = setInterval(() => {
      setLoadingStep((prev) => Math.min(prev + 1, LOADING_STEPS.length - 1))
    }, 900)

    try {
      const post = await generatePost({ topic, keywords, link, platforms: selected })
      setResult(post)
    } catch (err) {
      setError(err.message)
    } finally {
      clearInterval(stepInterval.current)
      setLoading(false)
    }
  }

  function handleCopy(text) {
    navigator.clipboard.writeText(text)
    setToast('Text copied to clipboard!')
  }

  const platformPosts = result?.platform_posts ? JSON.parse(result.platform_posts) : null
  const today = new Date().toLocaleDateString()

  return (
    <>
      <main className="workspace-grid">
        <section className="studio-panel">
          <form id="campaignForm" onSubmit={handleSubmit}>
            <div className="panel-header">
              <h1 className="panel-title">Compose Campaign</h1>
              <span className="panel-date">{today}</span>
            </div>

            <div className="field-group">
              <label className="field-label" htmlFor="topic">
                <span>01 / Topic / Story Focus</span>
                <span className="char-count">{topic.length}/280</span>
              </label>
              <textarea
                id="topic"
                className="plain-input"
                placeholder="e.g. Launching a new AI-powered resume builder for job seekers..."
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                required
              />
            </div>

            <div className="field-group">
              <label className="field-label" htmlFor="keywords">
                02 / Keywords &amp; Hashtags (optional)
              </label>
              <input
                id="keywords"
                type="text"
                className="plain-input"
                placeholder="e.g. AI, resume, job search"
                value={keywords}
                onChange={(e) => setKeywords(e.target.value)}
              />
            </div>

            <div className="field-group">
              <label className="field-label" htmlFor="targetLink">
                03 / Target Link (optional)
              </label>
              <input
                id="targetLink"
                type="url"
                className="plain-input"
                placeholder="https://example.com/launch"
                value={link}
                onChange={(e) => setLink(e.target.value)}
              />
            </div>

            <div className="field-group">
              <div className="platform-header-actions">
                <label className="field-label" style={{ marginBottom: 0 }}>
                  04 / Select Target Platforms
                </label>
                <button type="button" className="btn-text" onClick={toggleSelectAll}>
                  {selected.length === PLATFORMS.length ? 'Deselect All' : 'Select All'}
                </button>
              </div>

              <div className="platform-selector-grid">
                {PLATFORMS.map((p) => {
                  const Icon = PLATFORM_ICONS[p.key]
                  const isSelected = selected.includes(p.key)
                  const isDisconnected = platformStatus[p.key] === false && p.key in platformStatus
                  return (
                    <div
                      key={p.key}
                      className={`platform-chip ${isSelected ? 'selected' : ''}`}
                      onClick={() => togglePlatform(p.key)}
                      title={isDisconnected ? 'Not connected for publishing yet — content can still be generated' : ''}
                    >
                      <div className="platform-chip-left">
                        <span className="platform-icon">{Icon && <Icon />}</span>
                        <span>{p.label}</span>
                      </div>
                      {isDisconnected && <span className="badge-disconnected">Offline</span>}
                    </div>
                  )
                })}
              </div>
            </div>

            {error && <p className="form-error">{error}</p>}

            <button type="submit" className="btn-submit btn-submit-full" disabled={loading || selected.length === 0}>
              <span>{loading ? 'Generating...' : 'Generate Content'}</span>
            </button>
          </form>
        </section>

        <section className="output-canvas">
          {!result && !loading && (
            <div className="state-empty cyber-showroom-empty">
              <div className="empty-telemetry">
                <span className="telemetry-pill">&gt;|&lt; SYSTEM READY</span>
                <span className="telemetry-dots">▪ ▪ ▪ ▪ ▪</span>
              </div>
              <h1 className="hero-cyber-title">DEX</h1>
              <p className="hero-cyber-subtitle">AUTONOMOUS MULTI-CHANNEL CONTENT DISPATCH</p>
              <div className="cyber-ascii-divider">-- [ 09 BROADCAST CHANNELS // HUMAN-IN-THE-LOOP ] --</div>
              <p className="empty-desc">
                Input your campaign focus on the command panel to generate bespoke, platform-compliant variations &amp; AI visual assets.
              </p>
            </div>
          )}

          {loading && (
            <div className="state-loading">
              <div className="spinner"></div>
              <p className="loading-step">{LOADING_STEPS[loadingStep]}</p>
            </div>
          )}

          {result && platformPosts && (
            <div>
              <div className="canvas-header">
                <h2>{topic}</h2>
                <span className="canvas-date">{today}</span>
              </div>

              {result.image_url && (
                <div className="media-preview-box">
                  <div className={`media-image-container ${aspectRatio === 'square' ? 'square' : ''}`}>
                    <img src={result.image_url} alt="Generated visual" />
                  </div>
                  <div className="media-info">
                    <span className="media-tag">01 / Generated Visual Artwork</span>
                    <h4 className="media-title">AI Campaign Asset</h4>
                    <div className="aspect-ratio-controls">
                      <button
                        type="button"
                        className={`btn-ratio ${aspectRatio === 'landscape' ? 'active' : ''}`}
                        onClick={() => setAspectRatio('landscape')}
                      >
                        Landscape (16:9)
                      </button>
                      <button
                        type="button"
                        className={`btn-ratio ${aspectRatio === 'square' ? 'active' : ''}`}
                        onClick={() => setAspectRatio('square')}
                      >
                        Square (1:1)
                      </button>
                    </div>
                  </div>
                </div>
              )}

              <div className="results-grid">
                {Object.entries(platformPosts).map(([platform, data]) => {
                  const Icon = PLATFORM_ICONS[platform]
                  const text = data.post || data.caption || ''
                  return (
                    <article className="result-card" key={platform}>
                      <div className="card-top">
                        <div className="card-platform">
                          <span className="platform-icon">{Icon && <Icon />}</span>
                          <span className="card-platform-name">{platform.replace('_', ' ')}</span>
                        </div>
                        <div className="badge badge-success">
                          <span className="pulse-dot"></span>
                          Sent to Approve Queue
                        </div>
                      </div>

                      <div className="card-body">{text}</div>

                      {data.hashtags?.length > 0 && (
                        <div className="card-hashtags">
                          {data.hashtags.map((h) => `#${h.replace(/^#+/, '')}`).join(' ')}
                        </div>
                      )}

                      {data.call_to_action && (
                        <div className="card-cta-box">
                          <strong>Suggested CTA:</strong> {data.call_to_action}
                        </div>
                      )}

                      <div className="card-footer">
                        <span></span>
                        <button className="btn-outline" onClick={() => handleCopy(text)}>
                          Copy Text
                        </button>
                      </div>
                    </article>
                  )
                })}
              </div>
            </div>
          )}
        </section>
      </main>

      <div className={`toast-notification ${toast ? 'show' : ''}`}>
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <polyline points="20 6 9 17 4 12"></polyline>
        </svg>
        <span>{toast}</span>
      </div>
    </>
  )
}

export default Generate
