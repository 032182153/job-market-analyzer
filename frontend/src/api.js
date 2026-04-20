import axios from 'axios';

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE,
});

export const fetchStats = async () => {
  const { data } = await api.get('/stats');
  return data;
};

export const fetchTrendingSkills = async (filters) => {
  const { data } = await api.get('/skills/trending', { params: filters });
  return data;
};

export const fetchSkillTrend = async ({ skill, ...filters }) => {
  const { data } = await api.get('/skills/trend', { params: { skill, ...filters } });
  return data;
};

export const fetchCooccurrence = async () => {
  const { data } = await api.get('/skills/cooccurrence');
  return data;
};

export const fetchJobs = async (params) => {
  const { data } = await api.get('/jobs', { params });
  return data;
};

export default api;
