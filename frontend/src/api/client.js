import axios from "axios";

const apiBaseUrl = (
  import.meta.env.VITE_API_BASE_URL ||
  "https://breatheesg-hngw.onrender.com/api"
).replace(/\/+$/, "");

const client = axios.create({
  baseURL: apiBaseUrl,
});

export default client;