import axios from 'axios';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/campaign';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 10000,
});

export const registerParticipant = (data) => api.post('/participants/', data);
export const getStats = () => api.get('/stats/');
export const getRegions = () => api.get('/regions/');
export const getActivities = () => api.get('/activities/');

export default api;
