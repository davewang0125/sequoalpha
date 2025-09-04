const UserDashboard = ({ user, onLogout }) => {
  const [documents, setDocuments] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState('');
  const [selectedCategory, setSelectedCategory] = React.useState('All');
  const [searchTerm, setSearchTerm] = React.useState('');

  React.useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    setLoading(true);
    setError('');
    
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${window.API_BASE_URL}/documents`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        setDocuments(data);
      } else {
        setError('Failed to load documents');
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

  const handleDownload = async (document) => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(`${window.API_BASE_URL}/documents/${document.id}/download`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = document.filename || `${document.title}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } else {
        setError('Failed to download document');
      }
    } catch (err) {
      setError('Network error during download');
    }
  };

  const handleExternalLink = (url) => {
    window.open(url, '_blank');
  };

  // Filter documents based on category and search term
  const filteredDocuments = documents.filter(doc => {
    const matchesCategory = selectedCategory === 'All' || doc.category === selectedCategory;
    const matchesSearch = doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         doc.description.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesCategory && matchesSearch;
  });

  // Get unique categories
  const categories = ['All', ...new Set(documents.map(doc => doc.category))];

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
            <p>Document Center - View and download available documents</p>
          </div>

          {error && <div className="error-message">{error}</div>}

          {loading && (
            <div className="loading-section">
              <p>Loading documents...</p>
            </div>
          )}

          {!loading && (
            <div className="documents-section">
              <div className="documents-header">
                <h3>Available Documents</h3>
                <div className="documents-controls">
                  <div className="search-box">
                    <input
                      type="text"
                      placeholder="Search documents..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="search-input"
                    />
                  </div>
                  <div className="category-filter">
                    <select
                      value={selectedCategory}
                      onChange={(e) => setSelectedCategory(e.target.value)}
                      className="category-select"
                    >
                      {categories.map(category => (
                        <option key={category} value={category}>
                          {category}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              {filteredDocuments.length === 0 ? (
                <div className="no-documents">
                  <p>No documents found matching your criteria.</p>
                </div>
              ) : (
                <div className="documents-grid">
                  {filteredDocuments.map(doc => (
                    <div key={doc.id} className="document-card">
                      <div className="document-header">
                        <h4>{doc.title}</h4>
                        {doc.is_new && <span className="new-badge">NEW</span>}
                      </div>
                      <p className="document-description">{doc.description}</p>
                      <div className="document-meta">
                        <span className="document-category">{doc.category}</span>
                        <span className="document-type">{doc.type}</span>
                        {doc.file_size && <span className="document-size">{doc.file_size}</span>}
                      </div>
                      <div className="document-actions">
                        {doc.is_external ? (
                          <button
                            className="btn-external"
                            onClick={() => handleExternalLink(doc.external_url)}
                          >
                            🔗 Open External Link
                          </button>
                        ) : (
                          <button
                            className="btn-download"
                            onClick={() => handleDownload(doc)}
                          >
                            📥 Download
                          </button>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              )}
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
