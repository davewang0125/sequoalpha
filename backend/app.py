from flask import Flask, request, jsonify, send_file
from functools import wraps
from jose import jwt
import requests
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
API_IDENTIFIER = os.getenv('API_IDENTIFIER')
ALGORITHMS = ['RS256']


def get_token_auth_header():
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise Exception("Authorization header is expected")
    parts = auth.split()
    if parts[0].lower() != "bearer":
        raise Exception("Authorization header must start with Bearer")
    return parts[1]


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = requests.get(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
        jwks = jsonurl.json()
        unverified_header = jwt.get_unverified_header(token)
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=ALGORITHMS,
                    audience=API_IDENTIFIER,
                    issuer=f'https://{AUTH0_DOMAIN}/'
                )
            except Exception:
                return jsonify({"message": "Token validation failed"}), 401
        return f(*args, **kwargs)
    return decorated


@app.route('/protected')
@requires_auth
def protected():
    return jsonify({"message": "Welcome to protected data!"})


@app.route('/download/report')
@requires_auth
def download():
    return send_file('sample_report.pdf')  # Ensure this file exists


if __name__ == '__main__':
    app.run(debug=True)


## frontend/index.html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>Auth0 + Flask Example</title>
  <script src="https://cdn.auth0.com/js/auth0-spa-js/1.13/auth0-spa-js.production.js"></script>
</head>
<body>
  <h1>Protected Content Demo</h1>
  <button id="login">Login</button>
  <button id="get-data">Get Protected Data</button>
  <pre id="result"></pre>

  <script src="script.js"></script>
</body>
</html>


## frontend/script.js
let auth0 = null;

const configureClient = async () => {
  auth0 = await createAuth0Client({
    domain: 'YOUR_AUTH0_DOMAIN',
    client_id: 'YOUR_AUTH0_CLIENT_ID',
    audience: 'YOUR_API_IDENTIFIER'
  });
};

window.onload = async () => {
  await configureClient();

  document.getElementById('login').addEventListener('click', async () => {
    await auth0.loginWithPopup();
    const user = await auth0.getUser();
    document.getElementById('result').innerText = JSON.stringify(user, null, 2);
  });

  document.getElementById('get-data').addEventListener('click', async () => {
    const token = await auth0.getTokenSilently();
    const res = await fetch('https://your-backend.com/protected', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    });
    const data = await res.json();
    document.getElementById('result').innerText = JSON.stringify(data, null, 2);
  });
};

