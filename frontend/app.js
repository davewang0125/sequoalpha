let auth0 = null;

const auth0Config = {
  domain: 'YOUR_AUTH0_DOMAIN',
  client_id: 'YOUR_CLIENT_ID',
  audience: 'YOUR_API_IDENTIFIER',  // optional
};

async function initAuth0() {
  auth0 = await createAuth0Client(auth0Config);

  // handle redirect callback
  if (window.location.search.includes('code=')) {
    await auth0.handleRedirectCallback();
    window.history.replaceState({}, document.title, '/');
  }

  const isAuthenticated = await auth0.isAuthenticated();
  if (isAuthenticated) {
    const user = await auth0.getUser();
    document.getElementById('output').textContent = `Logged in as:\n${JSON.stringify(user, null, 2)}`;
  }
}

window.onload = async () => {
  await initAuth0();

  document.getElementById('login').onclick = () => auth0.loginWithRedirect({ redirect_uri: window.location.origin });

  document.getElementById('logout').onclick = () => auth0.logout({ returnTo: window.location.origin });

  document.getElementById('call-api').onclick = async () => {
    const token = await auth0.getTokenSilently();
    const response = await fetch('https://your-flask-api.com/protected', {
      headers: { Authorization: `Bearer ${token}` }
    });
    const data = await response.json();
    document.getElementById('output').textContent = JSON.stringify(data, null, 2);
  };
};

