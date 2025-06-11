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

if "email" not in st.session_state:
    st.session_state.email = None


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
    if "code" in query_params:
        code = query_params["code"][0]
        client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
        token = client.fetch_token(TOKEN_URL, code=code)
        client.token = token  # ✅ <-- ESSENCIAL!
        userinfo = client.get(USERINFO_URL).json()
        st.session_state.email = userinfo["email"]
        st.query_params.clear()  # limpa a URL após login

def main():
    handle_redirect()

    st.title("🔒 Autenticação Google com Streamlit + Authlib")

    if st.session_state.email:
        st.success(f"Logado como: {st.session_state.email}")
        st.write("🎉 Bem-vindo!")
    else:
        st.warning("Você não está logado.")
        login_url = build_login_url()
        st.markdown(f"[Clique aqui para login com Google]({login_url})")


if __name__ == "__main__":
    main()
