from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Chatbot PLN Multilenguaje",
    description="Chatbot basado en PLN clásico con contexto, persistencia y análisis de sentimiento",
    version="1.0.0"
)

app.include_router(router)
