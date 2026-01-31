import re
import nltk
import string
from nltk.stem import WordNetLemmatizer, SnowballStemmer
from nltk.corpus import stopwords

PUNCTUATION_TABLE = dict((ord(p), None) for p in string.punctuation)

lemmatizer_en = WordNetLemmatizer()

NLTK_LANG_MAP = {
    "es": "spanish",
    "en": "english",
    "fr": "french",
    "it": "italian"
}

stemmer_map = {
    "es": SnowballStemmer("spanish"),
    "fr": SnowballStemmer("french"),
    "it": SnowballStemmer("italian"),
    "de": SnowballStemmer("german"),
}

def load_corpus(path: str) -> str:
    with open(path, "r", encoding='utf-8', errors='ignore') as f:
        return f.read().lower()
    
def sentence_tokenize(text: str):
    return nltk.sent_tokenize(text)

def normalize_text(text: str, lang: str):
    # 1. Limpieza preliminar con Regex: Quitar referencias tipo [1], [12]
    text = re.sub(r'\[\d+\]', '', text) 
    
    # 2. Tokenización normal
    tokens = nltk.word_tokenize(text.lower().translate(PUNCTUATION_TABLE))

    nltk_lang_name = NLTK_LANG_MAP.get(lang, "english")
    
    try:
        stop_words = set(stopwords.words(nltk_lang_name))
    except OSError:
        stop_words = set()

    tokens = [t for t in tokens if t not in stop_words]

    if lang == "en":
        return [lemmatizer_en.lemmatize(t) for t in tokens]

    if lang in stemmer_map:
        return [stemmer_map[lang].stem(t) for t in tokens]

    return tokens