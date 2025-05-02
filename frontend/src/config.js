const apiURL = import.meta.env.VITE_API_URL || "http://localhost:8000";
if (!import.meta.env.VITE_API_URL) {
  console.warn("VITE_API_URL is not set. Using default: http://localhost:8000");
}

const config = {
  API_URL: apiURL,
};

export default config;
