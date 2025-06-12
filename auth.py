import os
from dotenv import load_dotenv
from authlib.integrations.requests_client import OAuth2Session
import streamlit as st
from urllib.parse import urlencode

load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPE = "openid email profile"

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

def build_login_url():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": SCOPE,
        "redirect_uri": REDIRECT_URI,
        "access_type": "offline",
        "prompt": "consent"
    }
    return f"{AUTH_URL}?{urlencode(params)}"

def handle_redirect():
    query_params = st.query_params
    code = query_params.get("code")

    if code and not st.session_state.get("email"):
        if isinstance(code, list):
            code = code[0]

        try:
            client = OAuth2Session(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)
            token = client.fetch_token(TOKEN_URL, code=code, redirect_uri=REDIRECT_URI, include_client_id=True)
            client.token = token
            userinfo = client.get(USERINFO_URL).json()
            st.session_state.email = userinfo["email"]
        except Exception as e:
            st.error("❌ Erro no login:")
            st.exception(e)
        finally:
            st.query_params.clear()
