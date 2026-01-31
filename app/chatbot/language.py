from langdetect import detect, LangDetectException

def detect_language(text: str) -> str:
    text_lower = text.lower()

    # 1. Heurística rápida por caracteres únicos
    # Detecta Español
    if any(c in text_lower for c in ['ñ', 'á', 'é', 'í', 'ó', 'ú', '¿']):
        return "es"
    
    # Detecta Francés
    if any(c in text_lower for c in ['à', 'â', 'ç', 'ê', 'î', 'ô', 'û', "aujourd'hui", "quoi"]):
        return "fr"
    
    # Detecta Italiano
    if any(c in text_lower for c in ['ì', 'ò', 'ù', 'gli', 'perché', "cos'è", "oggi"]):
        return "it"
    
    # 2. Detección estándar para el resto
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"