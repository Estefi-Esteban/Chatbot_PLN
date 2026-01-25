import json
import os
import random
import nltk
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer

# Asegúrate de que estos imports coincidan con tu estructura de carpetas
from .language import detect_language
from .sentiment import analyze_sentiment
from .preprocessing import normalize_text

from app.db.database import SessionLocal
from app.db.crud import save_message, get_recent_user_messages
from app.utils.logger import get_logger

logger = get_logger("PLNChatbot")

class PLNChatbot:
    def __init__(self, corpus_paths: dict, config_path="data/config/languages.json"):
        logger.info("Initializing LSA-PLNChatbot...")

        self.corpora = {}
        self.models = {}
        self.encoded_corpora = {}
        self.session_language = {}

        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                self.lang_config = json.load(f)
        else:
            logger.error(f"Config file not found at {config_path}")
            self.lang_config = {}

        self.knowledge_injections = {
            "es": [
                "El PLN o Procesamiento del Lenguaje Natural es la definición de la rama de la IA que estudia la comunicación entre humanos y máquinas.",
                "El PLN se utiliza y tiene aplicaciones para traducción automática, chatbots, análisis de sentimientos y asistentes virtuales.",
                "La historia y origen del PLN empezó en la década de 1950 con Alan Turing y el test de Turing."
            ],
            "en": [
                "NLP or Natural Language Processing is the definition of a field of AI focused on the interaction between computers and human language.",
                "The applications, tasks and usage of NLP include machine translation, chatbots, sentiment analysis, recognition and virtual assistants.",
                "The history and origin of NLP started in the 1950s with Alan Turing and the Turing Test."
            ],
            "fr": [
                "Le TALN est défini comme le traitement automatique du langage naturel.",
                "Les applications et usages du TALN servent à la traduction automatique, les chatbots et l'analyse.",
                "L'histoire et l'origine du TALN a commencé dans les années 1950 avec Turing."
            ],
            "it": [
                "L'NLP è definito come l'elaborazione del linguaggio naturale.",
                "L'NLP viene utilizzato e ha applicazioni per la traduzione automatica, i chatbot e l'analisi.",
                "La storia e l'origine dell'NLP inizia negli anni '50 con Alan Turing."
            ]
        }

        self.emotional_fallbacks = {
            "es": {
                "negative": "Vaya, lamento escuchar eso. Espero que todo mejore. 💙",
                "positive": "¡Me alegra mucho leer eso! ¿En qué puedo ayudarte hoy? 😊"
            },
            "en": {
                "negative": "I'm sorry to hear that. I hope things get better. 💙",
                "positive": "That's great to hear! How can I help you today? 😊"
            },
            "fr": {"negative": "Je suis désolé d'entendre cela. 💙", "positive": "C’est excellent ! 😊"},
            "it": {"negative": "Mi dispiace sentirlo. 💙", "positive": "Che bella notizia! 😊"}
        }

        self.greetings = {
            "es": ["hola", "buenas", "saludos", "qué tal"],
            "en": ["hello", "hi", "hey"],
            "fr": ["bonjour", "salut"],
            "it": ["ciao", "salve"]
        }

        for lang, path in corpus_paths.items():
            self._train_language_model(lang, path)

        logger.info("PLNChatbot initialized successfully")

    def _train_language_model(self, lang, path):
        """Entrena el pipeline LSA (TF-IDF + SVD) con limpieza y boosting."""
        logger.info(f"Training LSA model for language: {lang}")
        
        try:
            with open(path, encoding="utf-8", errors="ignore") as f:
                sentences = nltk.sent_tokenize(f.read())
        except FileNotFoundError:
            logger.error(f"Corpus file not found: {path}")
            return

        clean_sentences = []
        garbage_markers = ["encyclopædia", "britannica", "open library", "su open", "su enciclopedia", "(en)", "isbn", "doi:"]
        
        for s in sentences:
            s_lower = s.lower()
            if len(s) > 20 and not any(marker in s_lower for marker in garbage_markers):
                clean_sentences.append(s.strip())

        sentences = clean_sentences

        injections = self.knowledge_injections.get(lang, [])
        sentences.extend(injections * 5) 
        
        if not sentences:
            return

        self.corpora[lang] = sentences

        n_components = min(100, len(sentences) - 1)
        if n_components < 2: n_components = 2 

        self.models[lang] = make_pipeline(
            TfidfVectorizer(tokenizer=lambda text: normalize_text(text, lang)),
            TruncatedSVD(n_components=n_components, random_state=42),
            Normalizer(copy=False)
        )

        try:
            self.encoded_corpora[lang] = self.models[lang].fit_transform(sentences)
        except Exception as e:
            logger.error(f"Error training model for {lang}: {e}")

    def detect_intent(self, text: str, lang: str) -> str:
        text = text.lower()
        intent_map = self.lang_config.get(lang, {}).get("intent_map", {})
        
        for intent, keywords in intent_map.items():
            if any(k in text for k in keywords):
                return intent
        return "general"

    def get_response_lsa(self, text: str, lang: str, context: list):
        """Genera respuesta usando búsqueda semántica (LSA) con anclaje de contexto."""
        if lang not in self.models:
            return None # Retornamos None para que el fallback lo maneje

        intent = self.detect_intent(text, lang)
        
        query_text = text
        
        if intent != "general":
            keywords = self.lang_config.get(lang, {}).get("intent_map", {}).get(intent, [])
            query_text += " " + " ".join(keywords)
            
            query_text += " NLP Natural Language Processing PLN" 

        if context:
            query_text = context[-1] + " " + query_text

        pipeline = self.models[lang]
        try:
            query_vec = pipeline.transform([query_text])
            similarities = cosine_similarity(query_vec, self.encoded_corpora[lang]).flatten()
            
            best_idx = similarities.argmax()
            best_score = similarities[best_idx]
            
            logger.info(f"Intent: {intent} | Best Score (LSA): {best_score}")

            if best_score > 0.25:
                return self.corpora[lang][best_idx]
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")

        return None

    def greet(self, text: str, lang: str):
        for word in text.lower().split():
            if word in self.greetings.get(lang, []):
                return random.choice(self.greetings[lang])
        return None

    def chat(self, text: str, session_id: str = "default"):
        logger.info(f"Msg: {text} | Session: {session_id}")
        
        db = SessionLocal()
        supported_langs = set(self.corpora.keys())

        if session_id in self.session_language:
            lang = self.session_language[session_id]
        else:
            detected = detect_language(text)
            if detected in supported_langs:
                lang = detected
            else:
                lang = "en"
            
            if len(text.split()) >= 3:
                self.session_language[session_id] = lang

        sentiment = analyze_sentiment(text)
        intent = self.detect_intent(text, lang)
        context_raw = get_recent_user_messages(db=db, session_id=session_id, limit=2)
        
        response = self.greet(text, lang)

        if not response:
            if intent == "general" and sentiment["sentiment"] != "neutral":
                response = self.emotional_fallbacks.get(lang, {}).get(sentiment["sentiment"])
            
            if not response:
                 response = self.get_response_lsa(text, lang, context_raw)

        if not response:
            fallback = self.emotional_fallbacks.get(lang, {}).get(sentiment["sentiment"])
            response = fallback if fallback else "I didn't understand. / No entendí."

        # Guardar en BD
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
            "intent": intent,
            "context_used": context_raw 
        }