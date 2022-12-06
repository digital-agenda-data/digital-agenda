import axios from "axios";

const apiBaseEndpoint = "/api/v1";

export let apiHost = window.location.host;
export let apiURL = `${window.location.origin}${apiBaseEndpoint}`;
export let apiBase = `${window.location.origin}`;

if (import.meta.env.DEV) {
  apiHost = "localhost:8000";
  apiURL = `http://localhost:8000${apiBaseEndpoint}`;
  apiBase = "http://localhost:8000";
}

if (import.meta.env.VITE_APP_API_HOST) {
  apiHost = import.meta.env.VITE_APP_API_HOST;
  apiURL = `${window.location.protocol}//${apiHost}${apiBaseEndpoint}`;
  apiBase = `${window.location.protocol}//${apiHost}`;
}

export const api = axios.create({
  baseURL: apiURL,
  withCredentials: true,
  xsrfCookieName: "csrftoken",
  xsrfHeaderName: "X-CSRFToken",
  headers: {},
  maxRedirects: 5,
});
