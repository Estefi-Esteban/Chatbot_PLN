import streamlit as st
import requests
import uuid
import logging

logging.basicConfig(level=logging.INFO)

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Chatbot PLN",
    page_icon="🤖",
    layout="centered"
)

st.markdown("""
<style>
.chat-title {
    text-align: center;
    font-size: 2.5em;
    font-weight: bold;
}
.chat-subtitle {
    text-align: center;
    color: #6c757d;
}
</style>

<div class="chat-title">🤖 Chatbot PLN Multilenguaje</div>
<div class="chat-subtitle">
Procesamiento del Lenguaje Natural · Contexto · Sentimiento
</div>
<hr>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("ℹ️ Información")
    st.markdown("""
    **Tecnologías**
    - FastAPI
    - Streamlit
    - TF-IDF
    - SQLite
    
    **Características**
    - Multilenguaje
    - Contexto conversacional
    - Análisis de sentimiento
    """)

# Crear sesión única
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar historial
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input del usuario
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    # Mostrar mensaje usuario
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })
    with st.chat_message("user"):
        st.markdown(user_input)

    # Llamada a FastAPI
    response = requests.post(
        f"{API_URL}/chat",
        json={
            "message": user_input,
            "session_id": st.session_state.session_id
        }
    ).json()

    bot_text = response["response"]
    language = response["language"]
    sentiment = response["sentiment"]["sentiment"]

    logging.info(f"User: {user_input}")
    logging.info(f"Bot: {bot_text}")


    # Mostrar respuesta bot
    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_text
    })
    with st.chat_message("assistant"):
        st.markdown(bot_text)
        st.caption(f"🌍 Idioma: {language} | 💭 Sentimiento: {sentiment}")

if st.sidebar.button("🔄 Nueva conversación"):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.experimental_rerun()

