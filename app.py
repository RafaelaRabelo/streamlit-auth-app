import os
from dotenv import load_dotenv
from authlib.integrations.requests_client import OAuth2Session
import streamlit as st
from urllib.parse import urlencode

load_dotenv()

# 🔐 Credenciais e URLs
CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")
SCOPE = "openid email profile"

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"

# Inicializa estado
if "email" not in st.session_state:
    st.session_state.email = None

# Debug das variáveis carregadas
st.write("🔐 CLIENT_ID:", CLIENT_ID)
st.write("🔐 CLIENT_SECRET:", CLIENT_SECRET[:5] + "..." if CLIENT_SECRET else None)
st.write("🔁 REDIRECT_URI:", REDIRECT_URI)

# 🔗 Monta URL de login
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

# 🔁 Processa redirecionamento do Google
def handle_redirect():
    query_params = st.query_params
    st.write("📦 query_params:", query_params)

    code = query_params.get("code")

    if code and not st.session_state.email:
        if isinstance(code, list):
            code = code[0]

        st.write("🔑 Código recebido:", code)

        try:
            st.info("📨 Solicitando token...")
            client = OAuth2Session(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI)

            token = client.fetch_token(
                TOKEN_URL,
                code=code,
                redirect_uri=REDIRECT_URI,
                include_client_id=True,
            )

            client.token = token
            userinfo = client.get(USERINFO_URL).json()
            st.session_state.email = userinfo["email"]
            st.success(f"✅ Logado como: {userinfo['email']}")

        except Exception as e:
            st.error("❌ Erro no login:")
            st.exception(e)

        finally:
            st.query_params.clear()

# 🧠 Interface principal
def main():
    handle_redirect()

    st.title("🔒 Autenticação Google com Streamlit + Authlib")

    if st.session_state.email:
        st.success(f"✅ Logado como: {st.session_state.email}")
        st.write("🎉 Bem-vindo à aplicação segura!")
    else:
        st.warning("Você não está logado.")
        login_url = build_login_url()
        st.markdown(f"[Clique aqui para login com Google]({login_url})")

if __name__ == "__main__":
    main()
