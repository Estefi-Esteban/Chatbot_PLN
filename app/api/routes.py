from fastapi import APIRouter
from app.schemas import ChatRequest, ChatResponse, HistoryResponse
from app.chatbot.core import PLNChatbot
from app.db.database import SessionLocal
from app.db.crud import get_history

router = APIRouter()

# Inicializar chatbot (singleton simple)
bot = PLNChatbot(
    corpus_paths={
        "es": "data/corpus_es.txt",
        "en": "data/corpus_en.txt",
        "fr": "data/corpus_fr.txt"
    }
)


@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    result = bot.chat(
        text=request.message,
        session_id=request.session_id
    )
    return result


@router.get("/history/{session_id}", response_model=list[HistoryResponse])
def history_endpoint(session_id: str, limit: int = 10):
    db = SessionLocal()
    history = get_history(db, session_id, limit)
    db.close()

    return [
        {
            "user_message": h.user_message,
            "bot_response": h.bot_response,
            "language": h.language,
            "sentiment": h.sentiment,
            "polarity": h.polarity,
            "created_at": h.created_at.isoformat()
        }
        for h in history
    ]
