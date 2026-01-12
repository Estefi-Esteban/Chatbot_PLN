import wikipediaapi
import os
import re
from typing import Dict

# User-Agent obligatorio
USER_AGENT = "ChatbotPLN_Estefania/1.0 (chatbot@proyecto.com)"

WIKI_PAGES: Dict[str, str] = {
    "es": "Procesamiento_del_lenguaje_natural",
    "en": "Natural_language_processing",
    "fr": "Traitement_automatique_du_langage_naturel",
    "it": "Elaborazione_del_linguaggio_naturale"
}

# --- CAMBIO IMPORTANTE AQUÍ ---
# Ajusta esta ruta a donde TÚ tienes tus carpetas.
# He quitado el "app/" del principio para que busque en la carpeta data actual.
BASE_PATH = "data/corpora/raw"

# --- VERIFICACIÓN DE SEGURIDAD ---
# En vez de crear la carpeta, verificamos si existe.
if not os.path.exists(BASE_PATH):
    print(f"❌ ERROR: No encuentro la carpeta: {os.path.abspath(BASE_PATH)}")
    print("   El script se ha detenido para no crear carpetas nuevas.")
    print("   Por favor, edita la variable 'BASE_PATH' en el código para que coincida con tu carpeta.")
    exit()

def clean_text(text: str) -> str:
    text = re.sub(r"\[\d+\]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def scrape_wikipedia(lang: str, title: str) -> None:
    print(f"🔎 Conectando a Wikipedia ({lang}) - {title}...")

    try:
        wiki = wikipediaapi.Wikipedia(
            user_agent=USER_AGENT,
            language=lang
        )
        
        page = wiki.page(title)

        if not page.exists():
            print(f"⚠️  Página NO encontrada: {title} ({lang})")
            return

        raw_text = page.text
        
        # Filtro suave para asegurar contenido
        paragraphs = []
        for p in raw_text.split("\n"):
            cleaned = clean_text(p)
            if len(cleaned) > 20: 
                paragraphs.append(cleaned)

        corpus = "\n".join(paragraphs)

        if not corpus:
            print("   ⚠️  El contenido está vacío.")
            return

        file_path = os.path.join(BASE_PATH, f"corpus_{lang}_api.txt")
        
        # Aquí solo escribimos el archivo (mode 'w')
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(corpus)

        print(f"✅ Archivo creado: {file_path} ({len(paragraphs)} párrafos)\n")

    except Exception as e:
        print(f"❌ Error en {lang}: {e}")

if __name__ == "__main__":
    print(f"--- Guardando archivos en: {os.path.abspath(BASE_PATH)} ---\n")
    for lang, title in WIKI_PAGES.items():
        scrape_wikipedia(lang, title)