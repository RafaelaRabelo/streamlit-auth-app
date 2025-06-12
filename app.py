import streamlit as st
import asyncio
from auth import get_authorization_url, get_access_token, get_user_info

REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

def main():
    st.title("🔐 Autenticação com Google - Separado")

    query_params = st.query_params
    code = query_params.get("code", [None])[0]

    if "email" not in st.session_state:
        st.session_state.email = None

    if code and not st.session_state.email:
        try:
            st.info("🔄 Processando código de autorização...")
            token = asyncio.run(get_access_token(code, REDIRECT_URI))
            _, email = asyncio.run(get_user_info(token))
            st.session_state.email = email
            st.success(f"✅ Logado como {email}")
        except Exception as e:
            st.error("❌ Erro ao obter token ou e-mail")
            st.exception(e)
        finally:
            st.query_params.clear()

    if st.session_state.email:
        st.success(f"✅ Você está logado como {st.session_state.email}")
    else:
        login_url = asyncio.run(get_authorization_url(REDIRECT_URI))
        st.markdown(f"[Clique aqui para login com Google]({login_url})")

if __name__ == "__main__":
    main()
