

const Login = ({ onLogin, onBack }) => {
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await fetch(`${window.API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });

      const data = await response.json();

      if (response.ok) {
        console.log('🔑 Login successful, token:', data.access_token);
        localStorage.setItem('token', data.access_token);
        
        // Get user info with the token
        const userResponse = await fetch(`${window.API_BASE_URL}/users/me`, {
          headers: {
            'Authorization': `Bearer ${data.access_token}`
          }
        });
        
        if (userResponse.ok) {
          const userData = await userResponse.json();
          localStorage.setItem('user', JSON.stringify(userData));
          onLogin(userData);
        } else {
          // Fallback to basic user info
          localStorage.setItem('user', JSON.stringify({ username }));
          onLogin({ username });
        }
      } else {
        setError(data.detail || 'Login failed');
      }
    } catch (err) {
      setError('Network error. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        {onBack && (
          <button className="login-close" onClick={onBack} aria-label="Back to home">&times;</button>
        )}
        <div className="login-header">
          <h1>SequoAlpha Management</h1>
          <p>Secure Login Portal</p>
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <div className="form-group">
            <label htmlFor="username">Username</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Password</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={loading}
            />
          </div>

          {error && <div className="error-message">{error}</div>}

          <button type="submit" className="login-button" disabled={loading}>
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>

        <div className="login-footer">
          <p>Access to this site is authorized and permitted solely for those persons who have agreed to SequoAlpha Management LLC's Terms of Service and who have received from SequoAlpha a valid User ID and Password.</p>
          <p>© 2025 SequoAlpha Management LP. All rights reserved.</p>
        </div>
      </div>
    </div>
  );
};
