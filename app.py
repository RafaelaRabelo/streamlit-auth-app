import os
import streamlit as st
import asyncio
from httpx_oauth.clients.google import GoogleOAuth2
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

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
    st.title("🔒 Autenticação com Google - httpx_oauth")

    code = st.query_params.get("code", [None])[0]

    if "email" not in st.session_state:
        st.session_state.email = None

    if st.session_state.email:
        st.success(f"✅ Você está logado como: {st.session_state.email}")

    elif code:
        st.info("🔄 Processando código de autorização...")
        try:
            token = asyncio.run(get_access_token(code))
            _, email = asyncio.run(get_user_info(token["access_token"]))
            st.session_state.email = email
            st.success(f"✅ Login realizado: {email}")
            st.query_params.clear()
        except Exception as e:
            st.error("❌ Erro ao obter token:")
            st.exception(e)

    else:
        if st.button("Login com Google"):
            authorization_url = asyncio.run(get_authorization_url())
            st.markdown(f"[Clique aqui para login com Google]({authorization_url})")

if __name__ == "__main__":
    main()
