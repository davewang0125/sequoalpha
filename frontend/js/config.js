// Configuration for API URLs
const config = {
  // Development (localhost or direct port access)
  development: {
    apiUrl: window.location.protocol + '//' + window.location.hostname + ':8000'
  },
  // Production - EC2 or custom deployment
  production: {
    // For EC2: Use /api prefix (nginx will proxy to backend)
    // For same-server deployment, use relative path
    apiUrl: window.location.origin + '/api'
  },
  // Legacy: Render deployment (if still using)
  render: {
    apiUrl: 'https://sequoalpha.onrender.com'
  },
  // Legacy: Netlify deployment (if still using)
  netlify: {
    apiUrl: 'https://sequoalpha.onrender.com'
  }
};

// Detect environment
const isDevelopment = window.location.hostname === 'localhost' ||
                     window.location.hostname === '127.0.0.1' ||
                     window.location.port === '8080';
const isNetlify = window.location.hostname.includes('netlify.app');
const isRender = window.location.hostname.includes('onrender.com');
const isCustomDomain = window.location.hostname.includes('sequoalpha.com');

// Select configuration
let currentConfig;
if (isDevelopment) {
  currentConfig = config.development;
} else if (isNetlify || isCustomDomain) {
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
