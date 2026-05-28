import axios from "axios";

const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api").replace(/\/+$/, "");

const client = axios.create({
  baseURL: apiBaseUrl,
});

export default client;
