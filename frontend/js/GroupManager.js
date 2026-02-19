const GroupManager = ({ token, onBack }) => {
  const [tags, setTags] = React.useState([]);
  const [users, setUsers] = React.useState([]);
  const [newTagName, setNewTagName] = React.useState('');
  const [expandedTag, setExpandedTag] = React.useState(null);
  const [selectedUser, setSelectedUser] = React.useState('');
  const [message, setMessage] = React.useState({ text: '', type: '' });
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    fetchTags();
    fetchUsers();
  }, []);

  const fetchTags = async () => {
    try {
      const response = await fetch(`${window.API_BASE_URL}/admin/tags`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setTags(data.tags);
      }
    } catch (err) {
      showMessage('Error loading tags', 'error');
    } finally {
      setLoading(false);
    }
  };

  const fetchUsers = async () => {
    try {
      const response = await fetch(`${window.API_BASE_URL}/admin/users`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        // Filter out admin users
        setUsers(data.users.filter(u => !u.is_admin));
      }
    } catch (err) {
      console.error('Error loading users:', err);
    }
  };

  const showMessage = (text, type) => {
    setMessage({ text, type });
    setTimeout(() => setMessage({ text: '', type: '' }), 3000);
  };

  const handleCreateTag = async () => {
    const name = newTagName.trim();
    if (!name) return;

    try {
      const response = await fetch(`${window.API_BASE_URL}/admin/tags`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name })
      });

      if (response.ok) {
        setNewTagName('');
        showMessage('Group created', 'success');
        fetchTags();
      } else {
        const err = await response.json();
        showMessage(err.detail || 'Failed to create group', 'error');
      }
    } catch (err) {
      showMessage('Network error', 'error');
    }
  };

  const handleDeleteTag = async (tagId) => {
    if (!window.confirm('Delete this group? This will also remove it from any document visibility rules.')) return;

    try {
      const response = await fetch(`${window.API_BASE_URL}/admin/tags/${tagId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        showMessage('Group deleted', 'success');
        if (expandedTag === tagId) setExpandedTag(null);
        fetchTags();
      } else {
        showMessage('Failed to delete group', 'error');
      }
    } catch (err) {
      showMessage('Network error', 'error');
    }
  };

  const handleAddUser = async (tagId) => {
    if (!selectedUser) return;

    try {
      const response = await fetch(`${window.API_BASE_URL}/admin/tags/${tagId}/users`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ user_id: parseInt(selectedUser) })
      });

      if (response.ok) {
        setSelectedUser('');
        showMessage('User added to group', 'success');
        fetchTags();
      } else {
        const err = await response.json();
        showMessage(err.detail || 'Failed to add user', 'error');
      }
    } catch (err) {
      showMessage('Network error', 'error');
    }
  };

  const handleRemoveUser = async (tagId, userId) => {
    try {
      const response = await fetch(`${window.API_BASE_URL}/admin/tags/${tagId}/users/${userId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.ok) {
        showMessage('User removed from group', 'success');
        fetchTags();
      } else {
        showMessage('Failed to remove user', 'error');
      }
    } catch (err) {
      showMessage('Network error', 'error');
    }
  };

  const getAvailableUsers = (tag) => {
    const memberIds = tag.members.map(m => m.id);
    return users.filter(u => !memberIds.includes(u.id));
  };

  if (loading) {
    return (
      <div className="group-manager">
        <div className="loading">Loading groups...</div>
      </div>
    );
  }

  return (
    <div className="group-manager">
      <div className="group-header">
        <button className="back-button" onClick={onBack}>
          ← Back to Dashboard
        </button>
        <div className="header-content">
          <h1>Manage Groups</h1>
          <p>Create groups and assign users to control document visibility</p>
        </div>
      </div>

      {message.text && (
        <div className={`gm-message ${message.type}`}>{message.text}</div>
      )}

      <div className="create-tag-section">
        <input
          type="text"
          placeholder="New group name..."
          value={newTagName}
          onChange={(e) => setNewTagName(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleCreateTag()}
        />
        <button onClick={handleCreateTag}>Create Group</button>
      </div>

      {tags.length === 0 ? (
        <div className="no-tags">
          <p>No groups yet. Create your first group above.</p>
        </div>
      ) : (
        <div className="tags-list">
          {tags.map(tag => (
            <div key={tag.id} className="tag-card">
              <div className="tag-card-header" onClick={() => setExpandedTag(expandedTag === tag.id ? null : tag.id)}>
                <div className="tag-info">
                  <h3>{tag.name}</h3>
                  <span>{tag.member_count} member{tag.member_count !== 1 ? 's' : ''}</span>
                </div>
                <div className="tag-actions">
                  <button
                    className="expand-btn"
                    onClick={(e) => { e.stopPropagation(); setExpandedTag(expandedTag === tag.id ? null : tag.id); }}
                  >
                    {expandedTag === tag.id ? '▲ Collapse' : '▼ Expand'}
                  </button>
                  <button
                    className="delete-tag-btn"
                    onClick={(e) => { e.stopPropagation(); handleDeleteTag(tag.id); }}
                  >
                    Delete
                  </button>
                </div>
              </div>

              {expandedTag === tag.id && (
                <div className="tag-card-body">
                  <div className="add-member-row">
                    <select
                      value={selectedUser}
                      onChange={(e) => setSelectedUser(e.target.value)}
                    >
                      <option value="">Select a user...</option>
                      {getAvailableUsers(tag).map(u => (
                        <option key={u.id} value={u.id}>
                          {u.full_name || u.username} ({u.email})
                        </option>
                      ))}
                    </select>
                    <button onClick={() => handleAddUser(tag.id)}>Add User</button>
                  </div>

                  {tag.members.length === 0 ? (
                    <div className="no-members">No members in this group</div>
                  ) : (
                    <div className="members-list">
                      {tag.members.map(member => (
                        <div key={member.id} className="member-row">
                          <div className="member-info">
                            {member.full_name || member.username}
                            <span className="member-email">{member.email}</span>
                          </div>
                          <button
                            className="remove-btn"
                            onClick={() => handleRemoveUser(tag.id, member.id)}
                          >
                            Remove
                          </button>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
