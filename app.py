import os
import streamlit as st
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

# Inicializa cliente Google OAuth2
client = GoogleOAuth2(CLIENT_ID, CLIENT_SECRET)


async def get_authorization_url():
    return await client.get_authorization_url(
        redirect_uri=REDIRECT_URI,
        scope=["profile", "email"]
    )


async def get_access_token(code):
    return await client.get_access_token(code, REDIRECT_URI)


async def get_user_info(token):
    return await client.get_id_email(token)


def main():
    st.set_page_config(page_title="Login com Google")

    # Verifica se já temos o e-mail salvo
    if "email" not in st.session_state:
        st.session_state.email = None

    st.title("🔒 Autenticação com Google - httpx_oauth")

    query_params = st.query_params
    code = query_params.get("code", [None])[0]

    if st.session_state.email:
        st.success(f"✅ Você está logado como: {st.session_state.email}")
    elif code:
        st.info("🔄 Processando código de autorização...")

        try:
            # Obtem token
            token = asyncio.run(get_access_token(code))
            # Obtem email
            _, email = asyncio.run(get_user_info(token["access_token"]))
            st.session_state.email = email
            st.success(f"✅ Login realizado: {email}")
            st.experimental_set_query_params()  # Limpa URL

        except Exception as e:
            st.error("❌ Erro ao obter token:")
            st.exception(e)

    else:
        # Exibe botão de login se não estiver logado
        if st.button("Login com Google"):
            authorization_url = asyncio.run(get_authorization_url())
            st.markdown(f"[Clique aqui para login com Google]({authorization_url})")

if __name__ == "__main__":
    main()
