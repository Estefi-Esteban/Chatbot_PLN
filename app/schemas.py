from pydantic import BaseModel
from typing import Optional, List


class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"


class ChatResponse(BaseModel):
    response: str
    language: str
    sentiment: dict
    context_used: Optional[List[str]]


class HistoryResponse(BaseModel):
    user_message: str
    bot_response: str
    language: str
    sentiment: str
    polarity: str
    created_at: str
