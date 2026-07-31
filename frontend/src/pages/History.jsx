import { useEffect, useState } from 'react'
import { getPosts, publishPost } from '../api'
import { PLATFORM_ICONS } from '../components/Icons'

function statusBadge(status) {
  if (status === 'success') return <span className="badge badge-success">Published</span>
  if (status === 'error') return <span className="badge badge-error">Failed</span>
  return <span className="badge badge-missing">Not published</span>
}

function History() {
  const [posts, setPosts] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [publishingKey, setPublishingKey] = useState(null)

  function load() {
    setLoading(true)
    getPosts()
      .then((all) => setPosts(all.filter((p) => p.status !== 'draft' && p.status !== 'pending_approval')))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }

  useEffect(load, [])

  async function handlePublish(postId, platform) {
    const key = `${postId}-${platform}`
    setPublishingKey(key)
    try {
      await publishPost(postId, platform)
    } catch (err) {
      setError(err.message)
    } finally {
      setPublishingKey(null)
      load()
    }
  }

  return (
    <main className="page">
      <div className="eyebrow">History</div>
      <h1>Approved &amp; published posts</h1>
      <p className="lede">
        Publish an approved draft to each connected platform, and track what has already
        gone out.
      </p>

      {error && <p className="form-error">{error}</p>}

      {loading && (
        <div className="state-loading">
          <div className="spinner"></div>
          <p className="loading-step">LOADING HISTORY...</p>
        </div>
      )}

      {!loading && posts.length === 0 && (
        <div className="state-empty">
          <h3 className="empty-title">Nothing here yet</h3>
          <p className="empty-desc">Approve a draft first, then it will show up here for publishing.</p>
        </div>
      )}

      {posts.map((post) => {
        const platformPosts = post.platform_posts ? JSON.parse(post.platform_posts) : {}
        const results = post.publish_results ? JSON.parse(post.publish_results) : {}
        return (
          <article className="result-card" key={post.id}>
            <div className="card-top">
              <span className="card-platform-name" style={{ fontSize: '15px' }}>{post.topic}</span>
              <span className="loading-step" style={{ fontSize: '10px' }}>
                {new Date(post.created_at).toLocaleDateString()}
              </span>
            </div>

            {post.status === 'rejected' && (
              <p style={{ color: 'var(--text-muted)', fontSize: '12px' }}>
                Rejected — not eligible for publishing.
              </p>
            )}

            {post.status !== 'rejected' && (
              <div>
                {Object.keys(platformPosts).map((platform) => {
                  const result = results[platform]
                  const key = `${post.id}-${platform}`
                  const Icon = PLATFORM_ICONS[platform]
                  return (
                    <div
                      key={platform}
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        padding: '10px 0',
                        borderTop: '1px solid var(--border-subtle)',
                      }}
                    >
                      <div className="card-platform">
                        <span className="platform-icon">{Icon && <Icon />}</span>
                        <span style={{ textTransform: 'capitalize', fontSize: '12px', fontWeight: 500 }}>
                          {platform.replace('_', ' ')}
                        </span>
                      </div>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                        {statusBadge(result?.status)}
                        {result?.status === 'success' && result.url && (
                          <a href={result.url} target="_blank" rel="noreferrer" style={{ fontSize: '11px' }}>
                            View
                          </a>
                        )}
                        {result?.status === 'error' && (
                          <span style={{ fontSize: '11px', color: 'var(--text-muted)' }}>{result.detail}</span>
                        )}
                        {!result && (
                          <button
                            className="btn-outline"
                            disabled={publishingKey === key}
                            onClick={() => handlePublish(post.id, platform)}
                          >
                            {publishingKey === key ? 'Publishing...' : 'Publish'}
                          </button>
                        )}
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </article>
        )
      })}
    </main>
  )
}

export default History
