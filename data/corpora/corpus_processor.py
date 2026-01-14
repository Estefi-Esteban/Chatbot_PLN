import os
import re
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    print("Descargando recursos de NLTK...")
    nltk.download('punkt')
    nltk.download('punkt_tab')

RAW_PATH = "data/corpora/raw"
PROCESSED_PATH = "data/corpora/processed"

os.makedirs(PROCESSED_PATH, exist_ok=True)

NLTK_LANG_MAP = {
    "es": "spanish",
    "en": "english",
    "fr": "french",
    "it": "italian"
}

def deep_clean_text(text: str) -> str:
    text = re.sub(r"\[.*?\]", " ", text)
    
    text = re.sub(r"\.\.+", ".", text)
    
    text = re.sub(r'([a-z])\.([A-Z])', r'\1. \2', text)
    
    text = re.sub(r'(\d)\.([A-Z])', r'\1. \2', text)

    return text

def clean_sentence(sentence: str) -> str:
    sentence = sentence.strip()
    sentence = re.sub(r"\s+", " ", sentence)
    sentence = re.sub(r"[•*◆►■]", "", sentence)
    return sentence

def process_corpus(lang: str):
    raw_file = os.path.join(RAW_PATH, f"corpus_{lang}_api.txt")
    output_file = os.path.join(PROCESSED_PATH, f"corpus_{lang}.txt")

    if not os.path.exists(raw_file):
        print(f"⚠️ No existe el archivo de entrada: {raw_file}")
        return

    with open(raw_file, "r", encoding="utf-8") as f:
        text = f.read()

    text = deep_clean_text(text)

    nltk_lang = NLTK_LANG_MAP.get(lang, "english")
    
    try:
        sentences = nltk.sent_tokenize(text, language=nltk_lang)
    except Exception as e:
        print(f"❌ Error al tokenizar {lang} (usando {nltk_lang}): {e}")
        return

    cleaned = []
    for s in sentences:
        s = clean_sentence(s)
        if len(s.split()) >= 5:
            cleaned.append(s)

    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(cleaned))

    print(f"✅ Corpus procesado y LIMPIO ({lang}): {output_file}")


if __name__ == "__main__":
    for lang in ["es", "en", "fr", "it"]:
        process_corpus(lang)