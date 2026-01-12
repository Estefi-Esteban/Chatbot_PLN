from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .language import detect_language
from .sentiment import analyze_sentiment
from .preprocessing import normalize_text

from app.db.database import SessionLocal
from app.db.crud import save_message, get_recent_user_messages
from app.utils.logger import get_logger

import nltk
import random

logger = get_logger("PLNChatbot")


class PLNChatbot:
    def __init__(self, corpus_paths: dict):
        logger.info("Initializing PLNChatbot")

        self.corpora = {}
        self.vectorizers = {}
        self.session_language = {}

        # 🔹 Inyecciones de conocimiento
        self.knowledge_injections = {
            "es": [
                "El PLN se utiliza para traducción automática, chatbots, análisis de sentimientos y asistentes virtuales.",
                "La inteligencia artificial sirve para automatizar tareas, resolver problemas complejos y ayudar en la toma de decisiones.",
                "El PLN o Procesamiento del Lenguaje Natural es la rama de la IA que estudia la comunicación entre humanos y máquinas."
            ],
            "en": [
                "NLP is used for machine translation, chatbots, sentiment analysis, and virtual assistants.",
                "Artificial Intelligence is used to automate tasks, solve complex problems, and assist in decision making.",
                "NLP or Natural Language Processing is a field of AI focused on the interaction between computers and human language."
            ],
            "fr": [
                "Le TALN est utilisé pour la traduction automatique, les chatbots, l'analyse des sentiments et les assistants virtuels."
            ],
            "it": [
                "L'NLP viene utilizzato per la traduzione automatica, i chatbot, l'analisi del sentiment."
            ]
        }

        # 🔹 Fallback emocional por idioma
        self.emotional_fallbacks = {
            "es": {
                "negative": "Vaya, lamento escuchar eso. Espero que todo mejore.",
                "positive": "¡Me alegra mucho leer eso! ¿En qué puedo ayudarte hoy?"
            },
            "en": {
                "negative": "I'm sorry to hear that. I hope things get better.",
                "positive": "That's great to hear! How can I help you today?"
            },
            "fr": {
                "negative": "Je suis désolé d'entendre cela. J’espère que les choses s’amélioreront.",
                "positive": "C’est une excellente nouvelle !"
            },
            "it": {
                "negative": "Mi dispiace sentirlo. Spero che le cose migliorino.",
                "positive": "Che bella notizia!"
            }
        }

        # 🔹 Carga de corpus
        for lang, path in corpus_paths.items():
            logger.info(f"Loading corpus for language: {lang}")
            with open(path, encoding="utf-8", errors="ignore") as f:
                sentences = nltk.sent_tokenize(f.read())

            sentences.extend(self.knowledge_injections.get(lang, []))

            self.corpora[lang] = sentences
            self.vectorizers[lang] = TfidfVectorizer(
                tokenizer=lambda text, l=lang: normalize_text(text, l)
            )

        # 🔹 Saludos
        self.greetings = {
            "es": ["hola", "buenas", "saludos", "qué tal"],
            "en": ["hello", "hi", "hey"],
            "fr": ["bonjour", "salut"],
            "it": ["ciao", "salve"]
        }

        logger.info("PLNChatbot initialized successfully")

    # 🔹 Saludos
    def greet(self, text: str, lang: str):
        for word in text.lower().split():
            if word in self.greetings.get(lang, []):
                return random.choice(self.greetings[lang])
        return None

    # 🔹 Respuesta con contexto real
    def generate_response_with_context(self, text: str, lang: str, context: list):
        sentences = self.corpora.get(lang)
        vectorizer = self.vectorizers.get(lang)

        if not sentences:
            return "No he entendido tu mensaje."

        clean_context = list(dict.fromkeys(context))
        query_text = text

        if len(text.split()) < 6 and clean_context:
            query_text = clean_context[-1] + " " + text

        temp_corpus = sentences + clean_context + [query_text]
        tfidf = vectorizer.fit_transform(temp_corpus)

        similarity = cosine_similarity(tfidf[-1], tfidf[:-1]).flatten()
        best_idx = similarity.argmax()
        best_score = similarity[best_idx]

        logger.info(f"Best similarity score: {best_score:.3f}")

        if best_score > 0.20:
            return temp_corpus[best_idx]

        return "No he entendido tu mensaje."

    # 🔹 Chat principal
    def chat(self, text: str, session_id: str = "default"):
        logger.info(f"New message | session_id={session_id}")
        logger.info(f"User message: {text}")

        db = SessionLocal()
        supported_langs = set(self.corpora.keys())

        # 🔹 Idioma por sesión (solo si es fiable)
        if session_id in self.session_language:
            lang = self.session_language[session_id]
        else:
            detected = detect_language(text)
            lower = text.lower()

            if detected in supported_langs:
                lang = detected
            elif any(w in lower for w in ["oggi", "brutto", "triste", "male"]):
                lang = "it"
            elif any(w in lower for w in ["aujourd", "mauvais", "triste"]):
                lang = "fr"
            else:
                lang = "en"

            if len(text.split()) >= 3:
                self.session_language[session_id] = lang

        logger.info(f"Language used: {lang}")

        sentiment = analyze_sentiment(text)
        context = get_recent_user_messages(db=db, session_id=session_id, limit=3)

        greeting = self.greet(text, lang)

        if greeting:
            response = greeting
        else:
            response = self.generate_response_with_context(text, lang, context)

            if response == "No he entendido tu mensaje.":
                fallback = self.emotional_fallbacks.get(lang, {}).get(sentiment["sentiment"])
                if fallback:
                    response = fallback

        if sentiment["sentiment"] == "negative" and "💙" not in response:
            response += " 💙"
        elif sentiment["sentiment"] == "positive" and "😊" not in response:
            response += " 😊"

        save_message(
            db=db,
            session_id=session_id,
            user_message=text,
            bot_response=response,
            language=lang,
            sentiment=sentiment["sentiment"],
            polarity=sentiment["polarity"]
        )

        db.close()

        return {
            "response": response,
            "language": lang,
            "sentiment": sentiment,
            "context_used": context
        }
