from textblob import TextBlob

# 🔹 DICCIONARIO DE RESCATE PARA ESPAÑOL
# Como TextBlob solo sabe inglés, ayudamos con palabras clave comunes en español
POSITIVE_ES = {
    "feliz", "bien", "bueno", "buena", "mejor", "genial", "encanta", 
    "amo", "gracias", "excelente", "alegre", "contento", "contenta", 
    "maravilloso", "maravillosa", "bonito", "gusta", "amor"
}

NEGATIVE_ES = {
    "triste", "mal", "malo", "mala", "terrible", "peor", "odio", 
    "enfadado", "enfadada", "molesto", "molesta", "horrible", 
    "fatal", "deprimido", "llorar", "dolor", "asco"
}

POSITIVE_FR = {
    "heureux", "content", "bonne", "bien", "génial", "merci", "amour"
}

NEGATIVE_FR = {
    "mauvais", "mauvaise", "triste", "mal", "pire",
    "horrible", "déprimé", "déprimée", "problème"
}

def analyze_sentiment(text: str) -> dict:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    words = text.lower().split()
    manual_score = 0

    for word in words:
        clean = word.strip(".,!¡?¿'")

        if clean in POSITIVE_ES:
            manual_score += 0.6
        elif clean in NEGATIVE_ES:
            manual_score -= 0.6
        elif clean in POSITIVE_FR:
            manual_score += 0.6
        elif clean in NEGATIVE_FR:
            manual_score -= 0.6

    if manual_score != 0:
        polarity = manual_score

    if polarity > 0.1:
        sentiment = "positive"
    elif polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "polarity": polarity,
        "sentiment": sentiment
    }
