// Configuration for API URLs
const config = {
  // Development (localhost)
  development: {
    apiUrl: 'http://localhost:8000'
  },
  // Production - EC2 or custom deployment
  production: {
    // For EC2: Use /api prefix (nginx will proxy to backend)
    // For same-server deployment, use relative path
    apiUrl: window.location.origin + '/api'
  },
  // Legacy: Render deployment (if still using)
  render: {
    apiUrl: 'https://sequoalpha-backend.onrender.com'
  },
  // Legacy: Netlify deployment (if still using)
  netlify: {
    apiUrl: 'https://sequoalpha-backend.onrender.com'
  }
};

// Detect environment
const isDevelopment = window.location.hostname === 'localhost' || 
                     window.location.hostname === '127.0.0.1';
const isNetlify = window.location.hostname.includes('netlify.app');
const isRender = window.location.hostname.includes('onrender.com');

// Select configuration
let currentConfig;
if (isDevelopment) {
  currentConfig = config.development;
} else if (isNetlify) {
  currentConfig = config.netlify;
} else if (isRender) {
  currentConfig = config.render;
} else {
  // EC2 or custom deployment - use relative API path
  currentConfig = config.production;
}

// Export the API URL
window.API_BASE_URL = currentConfig.apiUrl;

// Log for debugging
console.log('🌍 Environment detected:', window.location.hostname);
console.log('🔧 Is Development:', isDevelopment);
console.log('☁️ Is Netlify:', isNetlify);
console.log('🔧 Is Render:', isRender);
console.log('🚀 API URL set to:', window.API_BASE_URL);
