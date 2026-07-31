import { useEffect, useState } from 'react'
import { getPosts, updatePostStatus } from '../api'
import { PLATFORM_ICONS } from '../components/Icons'

function Approve() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [actingId, setActingId] = useState(null)

  function load() {
    setLoading(true)
    getPosts()
      .then((all) => setPosts(all.filter((p) => p.status === 'pending_approval')))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  async function handleDecision(id, status) {
    setActingId(id)
    try {
      await updatePostStatus(id, status)
      setPosts((prev) => prev.filter((p) => p.id !== id))
    } catch (err) {
      setError(err.message)
    } finally {
      setActingId(null)
    }
  }

  return (
    <main className="page">
      <div className="eyebrow">Approve</div>
      <h1>Pending drafts</h1>
      <p className="lede">Review each draft before it can be published anywhere.</p>

      {error && <p className="form-error">{error}</p>}

      {loading && (
        <div className="state-loading">
          <div className="spinner"></div>
          <p className="loading-step">LOADING QUEUE...</p>
        </div>
      )}

      {!loading && posts.length === 0 && (
        <div className="state-empty">
          <h3 className="empty-title">Queue is empty</h3>
          <p className="empty-desc">No drafts waiting for approval — go to Generate to create one.</p>
        </div>
      )}

      {posts.map((post) => {
        const platformPosts = post.platform_posts ? JSON.parse(post.platform_posts) : {}
        return (
          <article className="result-card" key={post.id}>
            <div className="card-top">
              <span className="card-platform-name" style={{ fontSize: '15px' }}>{post.topic}</span>
              <span className="badge badge-pending">Pending review</span>
            </div>

            {post.image_url && (
              <div style={{ marginBottom: '16px' }}>
                <img
                  src={post.image_url}
                  alt="Generated visual"
                  style={{ maxWidth: '220px', borderRadius: '6px', border: '1px solid var(--border-medium)' }}
                />
              </div>
            )}

            {Object.entries(platformPosts).map(([platform, data]) => {
              const Icon = PLATFORM_ICONS[platform]
              return (
                <div key={platform} style={{ marginBottom: '14px' }}>
                  <div className="card-platform" style={{ marginBottom: '6px' }}>
                    <span className="platform-icon">{Icon && <Icon />}</span>
                    <span className="card-platform-name" style={{ fontSize: '12px', textTransform: 'capitalize' }}>
                      {platform.replace('_', ' ')}
                    </span>
                  </div>
                  <p className="card-body" style={{ marginBottom: 0 }}>{data.post || data.caption}</p>
                </div>
              )
            })}

            <div className="card-footer">
              <span></span>
              <div style={{ display: 'flex', gap: '10px' }}>
                <button
                  className="btn-outline"
                  disabled={actingId === post.id}
                  onClick={() => handleDecision(post.id, 'rejected')}
                >
                  Reject
                </button>
                <button
                  className="btn-submit"
                  disabled={actingId === post.id}
                  onClick={() => handleDecision(post.id, 'approved')}
                >
                  Approve
                </button>
              </div>
            </div>
          </article>
        )
      })}
    </main>
  )
}

export default Approve
