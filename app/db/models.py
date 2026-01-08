from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)

    user_message = Column(String)
    bot_response = Column(String)

    language = Column(String)
    sentiment = Column(String)
    polarity = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
