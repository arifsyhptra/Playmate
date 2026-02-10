import axios from "axios";

export const API_BASE = "https://playmate.my.id/api";

const api = axios.create({
  baseURL: API_BASE,
  timeout: 10000
});

// optional: interceptor (kalau nanti pakai token)
api.interceptors.request.use((config) => {
  const user = localStorage.getItem("user");
  if (user) {
    const token = JSON.parse(user).token;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

export default api;