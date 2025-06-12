import os
import streamlit as st
from authlib.integrations.requests_client import OAuth2Session
from urllib.parse import urlencode
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPE = "openid email profile"

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# Inicializa sessão
if "email" not in st.session_state:
    st.session_state.email = None

# Cria URL de login
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

# Lida com retorno do Google
def handle_auth():
    query_params = st.query_params
    code = query_params.get("code", [None])[0] if isinstance(query_params.get("code"), list) else query_params.get("code")

    if code and not st.session_state.email:
        try:
            st.info("📨 Solicitando token...")
            client = OAuth2Session(CLIENT_ID, CLIENT_SECRET, redirect_uri=REDIRECT_URI)
            token = client.fetch_token(
                TOKEN_URL,
                code=code,
                include_client_id=True,
                redirect_uri=REDIRECT_URI,
            )
            client.token = token
            userinfo = client.get(USERINFO_URL).json()
            st.session_state.email = userinfo["email"]
            st.success(f"✅ Logado como: {userinfo['email']}")
            st.query_params.clear()
        except Exception as e:
            st.error("❌ Erro durante o login:")
            st.exception(e)

# App principal
st.set_page_config(page_title="Login com Google", page_icon="🔒")
st.title("🔒 Autenticação com Google")

handle_auth()

if st.session_state.email:
    st.success(f"🎉 Bem-vindo, {st.session_state.email}!")
    st.write("Você está autenticado com sucesso!")
else:
    login_url = build_login_url()
    st.warning("Você não está logado.")
    st.markdown(f"[Clique aqui para login com Google]({login_url})")
