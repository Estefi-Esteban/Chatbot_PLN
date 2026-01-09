import streamlit as st
import requests
import uuid

# ---------------- CONFIG ----------------
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Chatbot PLN",
    page_icon="🤖",
    layout="centered"
)

# ---------------- ESTILOS ----------------
st.markdown("""
<style>
.chat-wrapper {
    max-width: 900px;
    margin: auto;
}

.user-msg {
    background: rgba(0, 123, 255, 0.15);
    color: inherit;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 10px 0;
    text-align: right;
}

.bot-msg {
    background: rgba(120, 120, 120, 0.15);
    color: inherit;
    padding: 14px 18px;
    border-radius: 18px;
    margin: 10px 0;
    text-align: left;
}

.meta {
    font-size: 0.75em;
    opacity: 0.7;
    margin-top: 4px;
}

.footer {
    text-align: center;
    font-size: 0.8em;
    opacity: 0.6;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🤖 Chatbot PLN")

st.sidebar.markdown("""
**Chatbot basado en PLN clásico**

✔ Multilenguaje  
✔ Contexto conversacional  
✔ Análisis de sentimiento  
✔ Persistencia en BD  
✔ FastAPI + Streamlit
""")

# 🔹 Botón nueva conversación
if st.sidebar.button("🆕 Nueva conversación"):
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())
    st.experimental_rerun()

st.sidebar.markdown("---")
st.sidebar.caption("Desarrollado por Estefanía 💙")

# ---------------- SESIÓN ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- HEADER ----------------
st.title("🤖 Chatbot PLN Multilenguaje")
st.markdown(
    "Chatbot académico basado en **TF-IDF**, "
    "**contexto conversacional** y **análisis de sentimiento**."
)

st.markdown("---")

# ---------------- CHAT ----------------
with st.container():
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(
                f"<div class='user-msg'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div class='bot-msg'>{msg['content']}</div>",
                unsafe_allow_html=True
            )
            st.markdown(
                f"<div class='meta'>🌍 {msg['language']} · 💭 {msg['sentiment']}</div>",
                unsafe_allow_html=True
            )

# ---------------- INPUT ----------------
user_input = st.chat_input("Escribe tu mensaje...")

if user_input:
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.spinner("Pensando... 🤔"):
        response = requests.post(
            f"{API_URL}/chat",
            json={
                "message": user_input,
                "session_id": st.session_state.session_id
            }
        ).json()

    st.session_state.messages.append({
        "role": "assistant",
        "content": response["response"],
        "language": response["language"],
        "sentiment": response["sentiment"]["sentiment"]
    })

    st.experimental_rerun()

# ---------------- FOOTER ----------------
st.markdown(
    "<div class='footer'>Proyecto PLN · Arquitectura clásica · 2024/2025</div>",
    unsafe_allow_html=True
)
