const CategoryManager = ({ token, onBack }) => {
  const [categories, setCategories] = React.useState([]);
  const [newCategoryName, setNewCategoryName] = React.useState('');
  const [loading, setLoading] = React.useState(true);
  const [message, setMessage] = React.useState({ text: '', type: '' });

  React.useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await fetch(`${window.API_BASE_URL}/admin/categories`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setCategories(data.categories);
      }
    } catch (err) {
      showMessage('Error loading categories', 'error');
    } finally {
      setLoading(false);
    }
  };

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: '', type: '' }), 3000);
  };

  const handleCreateCategory = async () => {
    const name = newCategoryName.trim();
    if (!name) return;

    try {
      const response = await fetch(`${window.API_BASE_URL}/admin/categories`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name })
      });

      if (response.ok) {
        setNewCategoryName('');
        showMessage('Category created', 'success');
        fetchCategories();
      } else {
        const err = await response.json();
        showMessage(err.detail || 'Failed to create category', 'error');
      }
    } catch (err) {
      showMessage('Network error', 'error');
    }
  };

  const handleDeleteCategory = async (categoryId) => {
    if (!window.confirm('Delete this category?')) return;

    try {
      const response = await fetch(`${window.API_BASE_URL}/admin/categories/${categoryId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        showMessage('Category deleted', 'success');
        fetchCategories();
      } else {
        const err = await response.json();
        showMessage(err.detail || 'Failed to delete category', 'error');
      }
    } catch (err) {
      showMessage('Network error', 'error');
    }
  };

  if (loading) {
    return (
      <div className="category-manager">
        <div className="loading">Loading categories...</div>
      </div>
    );
  }

  return (
    <div className="category-manager">
      <div className="cm-header">
        <button className="back-button" onClick={onBack}>
          &larr; Back to Dashboard
        </button>
        <div className="header-content">
          <h1>Manage Categories</h1>
          <p>Create and manage document categories</p>
        </div>
      </div>

      {message.text && (
        <div className={`cm-message ${message.type}`}>{message.text}</div>
      )}

      <div className="cm-create-section">
        <input
          type="text"
          placeholder="New category name..."
          value={newCategoryName}
          onChange={(e) => setNewCategoryName(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleCreateCategory()}
        />
        <button onClick={handleCreateCategory}>Create Category</button>
      </div>

      {categories.length === 0 ? (
        <div className="no-categories">
          <p>No categories yet. Create your first category above.</p>
        </div>
      ) : (
        <div className="categories-list">
          {categories.map(cat => (
            <div key={cat.id} className="category-card">
              <div className="category-info">
                <h3>{cat.name}</h3>
                <span>{cat.document_count} document{cat.document_count !== 1 ? 's' : ''}</span>
              </div>
              <div className="category-actions">
                {cat.document_count > 0 ? (
                  <span className="delete-blocked" title="Remove documents from this category first">
                    Has documents
                  </span>
                ) : (
                  <button
                    className="delete-category-btn"
                    onClick={() => handleDeleteCategory(cat.id)}
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
  );
};
