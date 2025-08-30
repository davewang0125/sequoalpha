// Configuration for API URLs
const config = {
  // Development (localhost)
  development: {
    apiUrl: 'http://localhost:8000'
  },
  // Production (Render)
  production: {
    apiUrl: 'https://sequoalpha-backend.onrender.com'
  }
};

// Detect environment
const isDevelopment = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1';
const currentConfig = isDevelopment ? config.development : config.production;

// Export the API URL
window.API_BASE_URL = currentConfig.apiUrl;
