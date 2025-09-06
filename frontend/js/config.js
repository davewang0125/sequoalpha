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

// Detect environment - CORRECTED for Netlify
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1';
const isNetlify = window.location.hostname.includes('netlify.app');
const currentConfig = isDevelopment ? config.development : config.production;

// Export the API URL
window.API_BASE_URL = currentConfig.apiUrl;

// Log for debugging
console.log('🌍 Environment detected:', window.location.hostname);
console.log('🔧 Is Development:', isDevelopment);
console.log('☁️ Is Netlify:', isNetlify);
console.log('🚀 API URL set to:', window.API_BASE_URL);
