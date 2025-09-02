

const App = () => {
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);
  const [user, setUser] = React.useState(null);
  const [currentView, setCurrentView] = React.useState('dashboard'); // 'dashboard' or 'documentCenter'

  React.useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    
    if (token && savedUser) {
      setIsAuthenticated(true);
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const handleLogin = (loginData) => {
    setIsAuthenticated(true);
    setUser({ username: loginData.username });
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setIsAuthenticated(false);
    setUser(null);
    setCurrentView('dashboard');
  };

  const handleOpenDocumentCenter = () => {
    setCurrentView('documentCenter');
  };

  const handleBackToDashboard = () => {
    setCurrentView('dashboard');
  };

  if (isAuthenticated) {
    if (currentView === 'documentCenter') {
      return <DocumentCenter token={localStorage.getItem('token')} onBack={handleBackToDashboard} />;
    }
    return <Dashboard user={user} onLogout={handleLogout} onOpenDocumentCenter={handleOpenDocumentCenter} />;
  }

  return (
    <div className="app">
      <Login onLogin={handleLogin} />
    </div>
  );
};
