

const Dashboard = ({ user, onLogout, onOpenDocumentCenter }) => {
  const [dashboardData, setDashboardData] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');
  const [showChangePassword, setShowChangePassword] = React.useState(false);
  const [showCreateUser, setShowCreateUser] = React.useState(false);
  const [passwordData, setPasswordData] = React.useState({ username: '', newPassword: '', confirmPassword: '' });
  const [userData, setUserData] = React.useState({ username: '', email: '', password: '', fullName: '' });
  const [message, setMessage] = React.useState('');

  React.useEffect(() => {
    // No need to fetch dashboard data since we don't have that endpoint
    // The dashboard will show admin options directly
    setLoading(false);
  }, []);

  const fetchDashboardData = async () => {
    // This function is no longer needed since we removed the /dashboard endpoint
    setLoading(false);
  };

  const handleLogout = () => {
    onLogout();
  };

  const handleChangePassword = async (e) => {
    e.preventDefault();
    if (passwordData.newPassword !== passwordData.confirmPassword) {
      setMessage('New passwords do not match');
      return;
    }

    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${window.API_BASE_URL}/admin/change-password`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: passwordData.username,
          new_password: passwordData.newPassword
        })
      });

      if (response.ok) {
        setMessage('Password changed successfully!');
        setPasswordData({ username: '', newPassword: '', confirmPassword: '' });
        setShowChangePassword(false);
      } else {
        const errorData = await response.json();
        setMessage(errorData.detail || 'Failed to change password');
      }
    } catch (err) {
      setMessage('Network error');
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${window.API_BASE_URL}/admin/create-user`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          username: userData.username,
          email: userData.email,
          password: userData.password,
          full_name: userData.fullName
        })
      });

      if (response.ok) {
        setMessage('User created successfully!');
        setUserData({ username: '', email: '', password: '', fullName: '' });
        setShowCreateUser(false);
      } else {
        const errorData = await response.json();
        setMessage(errorData.detail || 'Failed to create user');
      }
    } catch (err) {
      setMessage('Network error');
    }
  };

  return (
    <div className="dashboard">
      <nav className="dashboard-nav">
        <div className="nav-brand">
          <h1>SequoAlpha Management</h1>
        </div>
        <div className="nav-user">
          <span>Welcome, {user?.username}</span>
          <button onClick={handleLogout} className="logout-button">
            Logout
          </button>
        </div>
      </nav>

      <main className="dashboard-main">
        <div className="dashboard-content">
          <div className="welcome-section">
            <h2>Welcome to SequoAlpha Management LLC</h2>
            <p>You are now logged into the secure portal.</p>
            
            {user?.is_admin && (
              <div className="admin-actions">
                <div className="admin-buttons">
                  <button 
                    className="admin-btn primary"
                    onClick={() => setShowChangePassword(true)}
                  >
                    🔐 Change Password
                  </button>
                  <button 
                    className="admin-btn primary"
                    onClick={() => setShowCreateUser(true)}
                  >
                    👤 Create User
                  </button>
                  <button 
                    className="admin-btn primary"
                    onClick={onOpenDocumentCenter}
                  >
                    📄 Document Center
                  </button>
                </div>
              </div>
            )}
          </div>

          {message && (
            <div className={`message ${message.includes('successfully') ? 'success' : 'error'}`}>
              {message}
            </div>
          )}

          {loading && (
            <div className="loading-section">
              <p>Loading dashboard...</p>
            </div>
          )}

          {error && <div className="error-message">{error}</div>}

          {/* Dashboard data section removed since we don't have that endpoint */}

          <div className="info-section">
            <h3>About SequoAlpha</h3>
            <p>
              SequoAlpha Management LLC is an Exempt Reporting Advisor managing 
              private investment funds exclusively for qualified investors. 
              Access to this site is authorized and permitted solely for those 
              persons who have agreed to SequoAlpha Management LLC's Terms of 
              Service and who have received from SequoAlpha a valid User ID and Password.
            </p>
            <div className="contact-info">
              <p><strong>Address:</strong> 319 N Bernardo Ave, Mountainview, CA 94043</p>
              <p><strong>Phone:</strong> 650-308-9049</p>
              <p><strong>Email:</strong> info@sequoalpha.com</p>
            </div>
          </div>
        </div>
      </main>

      {/* Change Password Modal */}
      {showChangePassword && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>Change Password</h3>
              <button 
                className="close-btn"
                onClick={() => setShowChangePassword(false)}
              >
                ×
              </button>
            </div>
            <form onSubmit={handleChangePassword} className="modal-form">
              <div className="form-group">
                <label>Username (to change password):</label>
                <input
                  type="text"
                  value={passwordData.username}
                  onChange={(e) => setPasswordData({...passwordData, username: e.target.value})}
                  placeholder="Enter username to change password"
                  required
                />
              </div>
              <div className="form-group">
                <label>New Password:</label>
                <input
                  type="password"
                  value={passwordData.newPassword}
                  onChange={(e) => setPasswordData({...passwordData, newPassword: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Confirm New Password:</label>
                <input
                  type="password"
                  value={passwordData.confirmPassword}
                  onChange={(e) => setPasswordData({...passwordData, confirmPassword: e.target.value})}
                  required
                />
              </div>
              <div className="form-actions">
                <button type="submit" className="btn-primary">Change Password</button>
                <button 
                  type="button" 
                  className="btn-secondary"
                  onClick={() => setShowChangePassword(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Create User Modal */}
      {showCreateUser && (
        <div className="modal-overlay">
          <div className="modal">
            <div className="modal-header">
              <h3>Create New User</h3>
              <button 
                className="close-btn"
                onClick={() => setShowCreateUser(false)}
              >
                ×
              </button>
            </div>
            <form onSubmit={handleCreateUser} className="modal-form">
              <div className="form-group">
                <label>Username:</label>
                <input
                  type="text"
                  value={userData.username}
                  onChange={(e) => setUserData({...userData, username: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Email:</label>
                <input
                  type="email"
                  value={userData.email}
                  onChange={(e) => setUserData({...userData, email: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Full Name:</label>
                <input
                  type="text"
                  value={userData.fullName}
                  onChange={(e) => setUserData({...userData, fullName: e.target.value})}
                  required
                />
              </div>
              <div className="form-group">
                <label>Password:</label>
                <input
                  type="password"
                  value={userData.password}
                  onChange={(e) => setUserData({...userData, password: e.target.value})}
                  required
                />
              </div>
              <div className="form-actions">
                <button type="submit" className="btn-primary">Create User</button>
                <button 
                  type="button" 
                  className="btn-secondary"
                  onClick={() => setShowCreateUser(false)}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
