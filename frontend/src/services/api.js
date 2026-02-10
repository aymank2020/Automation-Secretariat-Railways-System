import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api

// Document API
export const documentApi = {
  getAll: (params) => api.get('/documents/', { params }),
  search: (params) => api.get('/documents/search', { params }),
  getById: (id) => api.get(`/documents/${id}`),
  create: (data) => api.post('/documents/', data),
  update: (id, data) => api.put(`/documents/${id}`, data),
  delete: (id) => api.delete(`/documents/${id}`),
  getHistory: (id) => api.get(`/documents/${id}/history`)
}

// User API
export const userApi = {
  getAll: () => api.get('/users/'),
  getById: (id) => api.get(`/users/${id}`),
  create: (data) => api.post('/users/', data),
  delete: (id) => api.delete(`/users/${id}`)
}