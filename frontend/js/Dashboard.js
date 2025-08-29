

const Dashboard = ({ user, onLogout }) => {
  const [dashboardData, setDashboardData] = React.useState(null);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');

  React.useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    setError('');
    
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/dashboard', {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setDashboardData(data);
      } else {
        setError('Failed to load dashboard data');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    onLogout();
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
          </div>

          {loading && (
            <div className="loading-section">
              <p>Loading dashboard...</p>
            </div>
          )}

          {error && <div className="error-message">{error}</div>}

          {dashboardData && (
            <div className="dashboard-info">
              <h3>Dashboard Information</h3>
              <p><strong>Message:</strong> {dashboardData.message}</p>
              <p><strong>User:</strong> {dashboardData.user}</p>
              <p><strong>Timestamp:</strong> {new Date(dashboardData.timestamp).toLocaleString()}</p>
            </div>
          )}

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
    </div>
  );
};
