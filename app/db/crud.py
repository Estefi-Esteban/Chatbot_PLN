from sqlalchemy.orm import Session
from .models import Conversation


def save_message(
    db: Session,
    session_id: str,
    user_message: str,
    bot_response: str,
    language: str,
    sentiment: str,
    polarity: float
):
    conversation = Conversation(
        session_id=session_id,
        user_message=user_message,
        bot_response=bot_response,
        language=language,
        sentiment=sentiment,
        polarity=str(polarity)
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def get_history(db: Session, session_id: str, limit: int = 5):
    return (
        db.query(Conversation)
        .filter(Conversation.session_id == session_id)
        .order_by(Conversation.created_at.desc())
        .limit(limit)
        .all()
    )

def get_recent_user_messages(db, session_id: str, limit: int = 3):
    results = (
        db.query(Conversation.user_message)
        .filter(Conversation.session_id == session_id)
        .order_by(Conversation.created_at.desc())
        .limit(limit)
        .all()
    )
    return [r[0] for r in results]
