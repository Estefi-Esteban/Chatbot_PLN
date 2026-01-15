import streamlit as st
import requests
import uuid
import streamlit.components.v1 as components

# ---------------- CONFIGURACIÓN INICIAL ----------------
API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="PLN Chatbot AI",
    page_icon="🧠",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ---------------- CSS DARK MODE + SCROLLABLE CONTAINER ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

/* 1. CONFIGURACIÓN GENERAL */
.stApp {
    font-family: 'Inter', sans-serif;
    background-color: #0e1117;
    color: #e0e0e0;
}

/* Forzar Sidebar Oscuro */
[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #2d2d2d;
}

/* Ocultar elementos nativos */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* 2. CONTENEDOR CON SCROLL (LA MAGIA) */
.scroll-container {
    height: 60vh; /* Altura fija */
    overflow-y: auto; /* Scroll vertical */
    padding: 20px;
    background-color: #13161c;
    border-radius: 15px;
    border: 1px solid #2d2d2d;
    margin-bottom: 20px;
    scroll-behavior: smooth;
    
    /* Scrollbar personalizada */
    scrollbar-width: thin;
    scrollbar-color: #4b5563 #13161c;
}

/* Estilo del Scrollbar (Chrome/Edge/Safari) */
.scroll-container::-webkit-scrollbar {
    width: 8px;
}
.scroll-container::-webkit-scrollbar-track {
    background: #13161c;
}
.scroll-container::-webkit-scrollbar-thumb {
    background-color: #4b5563;
    border-radius: 10px;
}

/* 3. FILAS Y AVATARES */
.chat-row {
    display: flex;
    margin-bottom: 25px;
    align-items: flex-start; 
}

.user-row {
    justify-content: flex-end;
}

.bot-row {
    justify-content: flex-start;
}

.avatar {
    width: 40px;
    height: 40px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin: 0 10px;
    flex-shrink: 0;
}

.user-avatar {
    background: linear-gradient(135deg, #8A2387 0%, #E94057 50%, #F27121 100%);
    color: white;
    order: 2;
    box-shadow: 0 0 15px rgba(233, 64, 87, 0.4);
}

.bot-avatar {
    background: #1f2937;
    color: #fff;
    border: 1px solid #374151;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}

/* 4. BURBUJAS DE MENSAJE */
.msg-bubble {
    padding: 16px 22px;
    border-radius: 16px;
    max-width: 80%;
    font-size: 15px;
    line-height: 1.6;
    position: relative;
}

.user-msg {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 18px 18px 0 18px;
    box-shadow: 0 10px 20px -5px rgba(118, 75, 162, 0.4);
}

.bot-msg {
    background: #1f2937; 
    color: #e5e7eb;
    border: 1px solid #374151;
    border-radius: 0 18px 18px 18px;
    box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
}

/* 5. BADGES */
.meta-info {
    display: flex;
    gap: 8px;
    margin-top: 10px;
    font-size: 0.75rem;
}

.badge {
    padding: 4px 10px;
    border-radius: 6px;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.7rem;
    display: flex;
    align-items: center;
    gap: 5px;
}

.badge-lang { background-color: #1e3a8a; color: #93c5fd; border: 1px solid #2563eb; }
.sentiment-positive { background-color: #064e3b; color: #6ee7b7; border: 1px solid #059669; }
.sentiment-negative { background-color: #7f1d1d; color: #fca5a5; border: 1px solid #dc2626; }
.sentiment-neutral { background-color: #374151; color: #d1d5db; border: 1px solid #4b5563; }

/* 6. AJUSTES FOOTER */
.custom-footer {
    text-align: center;
    color: #6b7280;
    font-size: 0.8em;
    margin-top: 20px;
}
.stChatInputContainer { background-color: #0e1117; padding-bottom: 20px; }

</style>
""", unsafe_allow_html=True)

# ---------------- LÓGICA DE SESIÓN ----------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712027.png", width=80) 
    st.title("NLP Assistant")
    st.markdown("---")
    
    st.markdown("""
    <div style="background: #0d1117; padding: 15px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #30363d;">
        <h4 style="margin:0; color:#e5e7eb;">📊 Estado del Sistema</h4>
        <p style="font-size:0.9em; color:#8b949e;">
        ✔ Motor: <b>TF-IDF + LSA</b><br>
        ✔ Modo: <b>Multilenguaje</b><br>
        ✔ Backend: <b>FastAPI</b>
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("✨ Nueva Conversación", type="primary", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.markdown("---")

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align: center;'>🤖 Chatbot PLN <span style='color:#a78bfa'>Multilenguaje</span></h1>", unsafe_allow_html=True)

# ---------------- HELPERS ----------------
def get_sentiment_class(sentiment):
    if not sentiment: return "sentiment-neutral"
    s = sentiment.lower()
    if "positiv" in s: return "sentiment-positive"
    if "negativ" in s: return "sentiment-negative"
    return "sentiment-neutral"

def get_sentiment_icon(sentiment):
    s = sentiment.lower() if sentiment else ""
    if "positiv" in s: return "😊"
    if "negativ" in s: return "😔"
    return "😐"

# ---------------- CHAT AREA (SCROLLABLE) ----------------
# IMPORTANTE: El HTML aquí NO tiene espacios al principio de las líneas
chat_html = """<div class="scroll-container" id="chat-container">"""

for msg in st.session_state.messages:
    if msg["role"] == "user":
        # Mensaje de USUARIO (Sin indentación)
        chat_html += f"""
<div class="chat-row user-row">
    <div class="msg-bubble user-msg">{msg['content']}</div>
    <div class="avatar user-avatar">👤</div>
</div>
"""
    else:
        # Mensaje de BOT (Sin indentación)
        sentiment_cls = get_sentiment_class(msg.get('sentiment', 'Neutral'))
        sentiment_icon = get_sentiment_icon(msg.get('sentiment', 'Neutral'))
        
        chat_html += f"""
<div class="chat-row bot-row">
    <div class="avatar bot-avatar">🤖</div>
    <div class="msg-container">
        <div class="msg-bubble bot-msg">{msg['content']}</div>
        <div class="meta-info">
            <span class="badge badge-lang">🌍 {msg.get('language', 'UNK')}</span>
            <span class="badge {sentiment_cls}">{sentiment_icon} {msg.get('sentiment', 'Neutral')}</span>
        </div>
    </div>
</div>
"""

# Script JS para bajar el scroll automáticamente
chat_html += """
<script>
    var container = document.getElementById("chat-container");
    container.scrollTop = container.scrollHeight;
</script>
</div>
"""

st.markdown(chat_html, unsafe_allow_html=True)

# ---------------- INPUT AREA ----------------
user_input = st.chat_input("Escribe tu pregunta aquí...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        with st.spinner("Analizando..."):
            response = requests.post(
                f"{API_URL}/chat",
                json={"message": user_input, "session_id": st.session_state.session_id}
            ).json()

        st.session_state.messages.append({
            "role": "assistant",
            "content": response["response"],
            "language": response["language"],
            "sentiment": response["sentiment"]["sentiment"]
        })
        st.rerun()
        
    except Exception as e:
        st.error(f"Error: {e}")

# ---------------- FOOTER ----------------
st.markdown("<div class='custom-footer'>Desarrollado con Python | © 2026 Proyecto Chatbot PLN</div>", unsafe_allow_html=True)