const KEY = 'site_password'

export function getStoredPassword() {
  return localStorage.getItem(KEY) || ''
}

export function setStoredPassword(password) {
  localStorage.setItem(KEY, password)
}

export function clearStoredPassword() {
  localStorage.removeItem(KEY)
}
