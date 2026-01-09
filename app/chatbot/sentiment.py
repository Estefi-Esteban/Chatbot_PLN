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

POSITIVE_IT = {
    "felice", "bene", "buono", "buona", "ottimo", "fantastico",
    "grazie", "amore", "contento", "contenta", "migliore"
}

NEGATIVE_IT = {
    "triste", "male", "cattivo", "cattiva", "pessimo",
    "odio", "arrabbiato", "arrabbiata", "problema",
    "brutto", "brutta", "deprimente"
}

def analyze_sentiment(text: str) -> dict:
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    words = text.lower().split()
    manual_score = 0

    for word in words:
        clean_word = word.strip(".,!¡?¿'")

        if clean_word in POSITIVE_ES:
            manual_score += 0.6
        elif clean_word in NEGATIVE_ES:
            manual_score -= 0.6
        elif clean_word in POSITIVE_FR:
            manual_score += 0.6
        elif clean_word in NEGATIVE_FR:
            manual_score -= 0.6
        elif clean_word in POSITIVE_IT:
            manual_score += 0.6
        elif clean_word in NEGATIVE_IT:
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