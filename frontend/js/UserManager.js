const UserManager = ({ token, onBack }) => {
  const [users, setUsers] = React.useState([]);
  const [loading, setLoading] = React.useState(true);
  const [message, setMessage] = React.useState({ text: '', type: '' });
  const [userData, setUserData] = React.useState({ username: '', email: '', password: '', fullName: '' });

  React.useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${window.API_BASE_URL}/admin/users`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setUsers(data.users);
      }
    } catch (err) {
      showMessage('Error loading users', 'error');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: '', type: '' }), 3000);
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    try {
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
        setUserData({ username: '', email: '', password: '', fullName: '' });
        showMessage('User created successfully', 'success');
        fetchUsers();
      } else {
        const err = await response.json();
        showMessage(err.detail || 'Failed to create user', 'error');
      }
    } catch (err) {
      showMessage('Network error', 'error');
    }
  };

  const handleDeleteUser = async (userId, username) => {
    if (!window.confirm(`Delete user "${username}"? This cannot be undone.`)) return;

    try {
      const response = await fetch(`${window.API_BASE_URL}/admin/users/${userId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        showMessage('User deleted', 'success');
        fetchUsers();
      } else {
        const err = await response.json();
        showMessage(err.detail || 'Failed to delete user', 'error');
      }
    } catch (err) {
      showMessage('Network error', 'error');
    }
  };

  if (loading) {
    return (
      <div className="user-manager">
        <div className="loading">Loading users...</div>
      </div>
    );
  }

  return (
    <div className="user-manager">
      <div className="um-header">
        <button className="back-button" onClick={onBack}>
          &larr; Back to Dashboard
        </button>
        <div className="header-content">
          <h1>Manage Users</h1>
          <p>Create and manage user accounts</p>
        </div>
      </div>

      {message.text && (
        <div className={`um-message ${message.type}`}>{message.text}</div>
      )}

      <div className="um-create-section">
        <h3>Create New User</h3>
        <form onSubmit={handleCreateUser} className="um-create-form">
          <input
            type="text"
            placeholder="Username"
            value={userData.username}
            onChange={(e) => setUserData({ ...userData, username: e.target.value })}
            required
          />
          <input
            type="email"
            placeholder="Email"
            value={userData.email}
            onChange={(e) => setUserData({ ...userData, email: e.target.value })}
            required
          />
          <input
            type="text"
            placeholder="Full Name"
            value={userData.fullName}
            onChange={(e) => setUserData({ ...userData, fullName: e.target.value })}
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={userData.password}
            onChange={(e) => setUserData({ ...userData, password: e.target.value })}
            required
          />
          <button type="submit">Create User</button>
        </form>
      </div>

      <div className="um-users-list">
        <h3>All Users ({users.length})</h3>
        {users.length === 0 ? (
          <div className="no-users">No users found.</div>
        ) : (
          <div className="users-table">
            {users.map(u => (
              <div key={u.id} className="user-row">
                <div className="user-info">
                  <div className="user-name">
                    {u.full_name || u.username}
                    {u.is_admin && <span className="admin-badge">Admin</span>}
                  </div>
                  <div className="user-meta">
                    <span>{u.username}</span>
                    <span className="user-email">{u.email}</span>
                  </div>
                </div>
                <div className="user-actions">
                  {!u.is_admin && (
                    <button
                      className="delete-user-btn"
                      onClick={() => handleDeleteUser(u.id, u.username)}
                    >
                      Delete
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
