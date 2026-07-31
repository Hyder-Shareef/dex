import { useEffect, useState } from 'react'
import { getPlatformStatus } from '../api'
import { PLATFORM_ICONS } from '../components/Icons'

const PLATFORM_INFO = [
  {
    key: 'bluesky',
    label: 'Bluesky',
    free: true,
    help: 'Create an app password at bsky.app/settings/app-passwords, then set BLUESKY_HANDLE and BLUESKY_APP_PASSWORD in the backend .env.',
  },
  {
    key: 'mastodon',
    label: 'Mastodon',
    free: true,
    help: 'Create an access token from your instance\'s Development settings, then set MASTODON_INSTANCE_URL and MASTODON_ACCESS_TOKEN.',
  },
  {
    key: 'x',
    label: 'X',
    free: false,
    help: 'Requires a paid X API developer plan (developer.x.com). Set X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET.',
  },
  {
    key: 'linkedin',
    label: 'LinkedIn',
    free: false,
    help: 'Requires an app approved by LinkedIn for the w_member_social scope. Set LINKEDIN_ACCESS_TOKEN and LINKEDIN_PERSON_URN.',
  },
  {
    key: 'facebook',
    label: 'Facebook',
    free: false,
    help: 'Requires a Meta app reviewed for page publishing. Set META_PAGE_ACCESS_TOKEN and META_PAGE_ID.',
  },
  {
    key: 'instagram',
    label: 'Instagram',
    free: false,
    help: 'Requires a Meta app reviewed for IG publishing. Set META_PAGE_ACCESS_TOKEN and META_IG_USER_ID.',
  },
]

function Accounts() {
  const [status, setStatus] = useState({})
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    getPlatformStatus()
      .then(setStatus)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false))
  }, [])

  return (
    <main className="page">
      <div className="eyebrow">Accounts</div>
      <h1>Connected platforms</h1>
      <p className="lede">
        Credentials are set as environment variables on the backend, not through this
        page — that keeps API keys off the client entirely. Restart the backend after
        adding new ones.
      </p>

      {error && <p className="form-error">{error}</p>}

      {loading && (
        <div className="state-loading">
          <div className="spinner"></div>
          <p className="loading-step">CHECKING CONNECTIONS...</p>
        </div>
      )}

      {!loading &&
        PLATFORM_INFO.map((p) => {
          const Icon = PLATFORM_ICONS[p.key]
          const connected = status[p.key]
          return (
            <article className="result-card" key={p.key}>
              <div className="card-top">
                <div className="card-platform">
                  <span className="platform-icon">{Icon && <Icon />}</span>
                  <span className="card-platform-name">{p.label}</span>
                </div>
                {connected ? (
                  <span className="badge badge-success">Connected</span>
                ) : (
                  <span className="badge badge-missing">Not configured</span>
                )}
              </div>
              {!p.free && (
                <p style={{ fontSize: '11px', color: 'var(--text-subtle)', marginBottom: '6px' }}>
                  Requires external approval — not free/instant.
                </p>
              )}
              <p style={{ fontSize: '12px', color: 'var(--text-muted)' }}>{p.help}</p>
            </article>
          )
        })}
    </main>
  )
}

export default Accounts
