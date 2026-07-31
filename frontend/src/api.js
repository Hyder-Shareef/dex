import { getStoredPassword } from './auth'

export const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8020'

export class AuthError extends Error {}

function authFetch(url, options = {}) {
  const headers = { ...(options.headers || {}) }
  const password = getStoredPassword()
  if (password) headers['X-Site-Password'] = password
  return fetch(url, { ...options, headers })
}

export function withSitePassword(url) {
  const password = getStoredPassword()
  if (!password) return url
  const sep = url.includes('?') ? '&' : '?'
  return `${url}${sep}site_password=${encodeURIComponent(password)}`
}

async function handle(res, fallbackMessage) {
  if (res.status === 401) throw new AuthError('Invalid site password.')
  if (!res.ok) {
    let message = fallbackMessage
    try {
      const data = await res.json()
      message = data.detail || message
    } catch {
      // ignore
    }
    throw new Error(message)
  }
  return res.json()
}

export async function getPosts() {
  const res = await authFetch(`${API_URL}/api/posts`)
  return handle(res, 'Could not load posts.')
}

export async function generatePost({ topic, keywords, link, platforms }) {
  const res = await authFetch(`${API_URL}/api/posts/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ topic, keywords, link, platforms }),
  })
  return handle(res, 'Could not generate content.')
}

export async function updatePostStatus(postId, status) {
  const res = await authFetch(`${API_URL}/api/posts/${postId}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status }),
  })
  return handle(res, 'Could not update status.')
}

export async function publishPost(postId, platform) {
  const res = await authFetch(`${API_URL}/api/posts/${postId}/publish/${platform}`, {
    method: 'POST',
  })
  return handle(res, 'Could not publish post.')
}

export async function getPlatformStatus() {
  const res = await authFetch(`${API_URL}/api/posts/meta/platform-status`)
  return handle(res, 'Could not load platform status.')
}
