
const App = () => {
  console.log('🚀 App component is rendering');
  
  const [isAuthenticated, setIsAuthenticated] = React.useState(false);
  const [user, setUser] = React.useState(null);
  const [currentView, setCurrentView] = React.useState('dashboard'); // 'dashboard' or 'documentCenter'

  React.useEffect(() => {
    // Check if user is already logged in
    const token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    
    console.log('🔍 App useEffect - token:', token);
    console.log('🔍 App useEffect - savedUser:', savedUser);
    
    if (token && savedUser) {
      console.log('✅ User is authenticated');
      setIsAuthenticated(true);
      setUser(JSON.parse(savedUser));
    } else {
      console.log('❌ User is not authenticated');
    }
  }, []);

  const handleLogin = (loginData) => {
    setIsAuthenticated(true);
    setUser(loginData);
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

  console.log('🔍 isAuthenticated:', isAuthenticated);
  console.log('🔍 currentView:', currentView);
  console.log('🔍 user:', user);
  
  if (isAuthenticated) {
    if (currentView === 'documentCenter') {
      const token = localStorage.getItem('token');
      console.log('🔑 Token from localStorage:', token);
      if (!token) {
        console.log('❌ No token found, redirecting to login');
        // If no token, redirect to login
        handleLogout();
        return null;
      }
      return <DocumentCenter token={token} onBack={handleBackToDashboard} />;
    }
    
    // Show different dashboards based on user type
    if (user?.is_admin) {
      return <Dashboard user={user} onLogout={handleLogout} onOpenDocumentCenter={handleOpenDocumentCenter} />;
    } else {
      return <UserDashboard user={user} onLogout={handleLogout} />;
    }
  }

  return (
    <div className="app">
      <Login onLogin={handleLogin} />
    </div>
  );
};
