import streamlit as st
from auth import handle_redirect, build_login_url

handle_redirect()

st.title("Minha Aplicação Segura")

if st.session_state.get("email"):
    st.success(f"✅ Logado como: {st.session_state.email}")
    # Aqui vai o conteúdo do seu dashboard
else:
    st.warning("Você não está logado.")
    login_url = build_login_url()
    st.markdown(f"[Clique aqui para login com Google]({login_url})")
