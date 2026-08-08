import os
from dotenv import load_dotenv

load_dotenv()

# OAuth configuration
OAUTH_SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/userinfo.email',
    'openid'
]

# Allow HTTP for local development OAuth callback
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SECRET_KEY = os.environ.get('FLASK_SECRET_KEY', 'super-secret-key-change-in-prod')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')
