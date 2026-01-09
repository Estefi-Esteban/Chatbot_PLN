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

        # 🔹 Inyecciones de conocimiento (controladas)
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
                "Le TALN est utilisé pour la traduction automatique, les chatbots, l'analyse des sentiments et les assistants virtuels.",
                "Le traitement automatique du langage naturel est un domaine de l'intelligence artificielle."
            ],
            "it": [
                "L'NLP viene utilizzato per la traduzione automatica, i chatbot, l'analisi del sentiment e gli assistenti virtuali."
            ]
        }

        # 🔹 Respuestas emocionales (fallback empático)
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

        # 🔹 Cargar corpus por idioma
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

    # 🔹 Detección de saludo
    def greet(self, text: str, lang: str):
        for word in text.lower().split():
            if word in self.greetings.get(lang, []):
                logger.info("Greeting detected")
                return random.choice(self.greetings[lang])
        return None

    # 🔹 Generación de respuesta con contexto
    def generate_response_with_context(self, text: str, lang: str, context: list):
        logger.info("Generating response with context")

        sentences = self.corpora.get(lang)
        vectorizer = self.vectorizers.get(lang)

        if not sentences:
            logger.warning("Language not supported")
            return "No he entendido tu mensaje."

        clean_context = list(dict.fromkeys(context))

        query_text = text
        if len(text.split()) < 6 and clean_context:
            query_text = clean_context[-1] + " " + text
            logger.info("Short query expanded using context")

        temp_sentences = sentences + clean_context + [query_text]

        tfidf = vectorizer.fit_transform(temp_sentences)
        similarity = cosine_similarity(tfidf[-1], tfidf).flatten()

        for idx in similarity.argsort()[::-1]:
            if idx == len(temp_sentences) - 1:
                continue
            if similarity[idx] > 0:
                logger.info(f"Response selected (similarity={similarity[idx]:.3f})")
                return temp_sentences[idx]

        logger.warning("No suitable response found")
        return "No he entendido tu mensaje."

    # 🔹 Chat principal
    def chat(self, text: str, session_id: str = "default"):
        logger.info(f"New message | session_id={session_id}")
        logger.info(f"User message: {text}")

        db = SessionLocal()

        detected_lang = detect_language(text)
        supported_langs = set(self.corpora.keys())

        lang = detected_lang if detected_lang in supported_langs else None

        # 🔹 Heurística de rescate por vocabulario (MUY IMPORTANTE)
        lower_text = text.lower()

        if not lang:
            if any(w in lower_text for w in ["oggi", "brutto", "brutta", "triste", "male"]):
                lang = "it"
            elif any(w in lower_text for w in ["aujourd", "mauvais", "triste", "mal"]):
                lang = "fr"
            else:
                lang = "en"  # fallback neutro


        logger.info(f"Detected language: {detected_lang} | Using: {lang}")

        # 🔹 Sentimiento
        sentiment = analyze_sentiment(text)
        logger.info(
            f"Sentiment detected: {sentiment['sentiment']} "
            f"(polarity={sentiment['polarity']})"
        )

        # 🔹 Contexto conversacional
        context = get_recent_user_messages(db=db, session_id=session_id, limit=3)
        logger.info(f"Context retrieved: {len(context)} messages")

        # 🔹 Generar respuesta
        greeting = self.greet(text, lang)

        if greeting:
            response = greeting
        else:
            response = self.generate_response_with_context(text, lang, context)

            # 🔹 Fallback emocional (MISMO idioma siempre)
            if response == "No he entendido tu mensaje.":
                emotional_msg = self.emotional_fallbacks.get(lang, {}).get(
                    sentiment["sentiment"]
                )
                if emotional_msg:
                    logger.info("Emotional fallback applied")
                    response = emotional_msg

        # 🔹 Emojis finales (sin duplicar)
        already_has_emoji = any(e in response for e in ["💙", "😊"])
        if not already_has_emoji:
            if sentiment["sentiment"] == "negative":
                response += " 💙"
            elif sentiment["sentiment"] == "positive":
                response += " 😊"

        logger.info(f"Final bot response: {response}")

        # 🔹 Persistencia
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
        logger.info("Conversation saved to database")

        return {
            "response": response,
            "language": lang,
            "sentiment": sentiment,
            "context_used": context
        }

