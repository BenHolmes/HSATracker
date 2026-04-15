/**
 * Shared Axios instance for all API calls.
 *
 * baseURL '/api/v1' is resolved relative to the current origin, so:
 *   - In development: Vite proxies /api → http://localhost:8000
 *   - In production: Nginx proxies /api/ → http://backend:8000
 *
 * All requests default to JSON. Receipt uploads override Content-Type to
 * 'multipart/form-data' at the call site.
 */

import axios from 'axios'

const client = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

export default client
