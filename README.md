# 🤖 Chatbot PLN Multilenguaje con Análisis Semántico y Emocional

Proyecto académico avanzado de **Procesamiento del Lenguaje Natural (PLN)** que implementa un **chatbot multilenguaje** capaz de comprender preguntas técnicas, detectar intención, analizar sentimiento y responder utilizando **búsqueda semántica** sobre corpus reales obtenidos automáticamente desde Wikipedia.

---

## 📌 Descripción general del sistema

Este proyecto implementa un **chatbot PLN híbrido**, basado en técnicas clásicas de procesamiento del lenguaje natural, que combina:

- Búsqueda semántica mediante TF-IDF y LSA
- Análisis de sentimiento multilenguaje
- Detección de intención
- Gestión de contexto conversacional
- Soporte multilenguaje (Español, Inglés, Francés e Italiano)
- Scraping y procesamiento automático de corpus
- Persistencia de conversaciones
- Interfaz web interactiva

El objetivo del sistema es **simular un asistente conversacional inteligente**, sin depender directamente de modelos LLM, manteniendo **control total del conocimiento y del comportamiento del bot**.

---

## 🌍 Idiomas soportados

- 🇪🇸 Español  
- 🇬🇧 Inglés  
- 🇫🇷 Francés  
- 🇮🇹 Italiano  

El idioma se detecta automáticamente y se mantiene durante toda la sesión.

---

## 🧠 Funcionalidades principales

### ✅ Procesamiento del Lenguaje Natural
- Tokenización
- Normalización de texto
- Eliminación de stopwords
- Lematización según idioma

### ✅ Búsqueda semántica
- Vectorización TF-IDF
- Reducción de dimensionalidad mediante **LSA (Latent Semantic Analysis)**
- Similaridad coseno

### ✅ Detección de intención
- Clasificación basada en reglas y palabras clave
- Intenciones soportadas:
  - Definición
  - Uso / Aplicaciones
  - Historia
  - Preguntas generales

### ✅ Análisis de sentimiento
- Análisis híbrido combinando:
  - TextBlob
  - Diccionarios personalizados multilenguaje
- Clasificación:
  - Positivo
  - Negativo
  - Neutral

### ✅ Contexto conversacional
- Recuperación de mensajes anteriores desde base de datos
- Uso del contexto para mejorar la relevancia semántica

### ✅ Fallback emocional
- Respuestas empáticas cuando no se encuentra una respuesta clara en el corpus

### ✅ Persistencia de datos
- Almacenamiento de conversaciones en **SQLite**
- Registro de:
  - Mensaje del usuario
  - Respuesta del bot
  - Idioma
  - Sentimiento
  - Polaridad

### ✅ Interfaz web
- Frontend desarrollado con **Streamlit**
- Interfaz sencilla e intuitiva
- Visualización clara de respuestas y contexto

---

## 🗂️ Estructura del proyecto

📦 ChatbotPLN
│
├── app/
│ ├── api/ # Backend FastAPI
│ ├── core/
│ │ ├── core.py # Lógica principal del chatbot
│ │ ├── language.py # Detección de idioma
│ │ ├── sentiment.py # Análisis de sentimiento
│ │ └── preprocessing.py # Limpieza y normalización de texto
│ │
│ ├── data/
│ │ ├── corpora/
│ │ │ ├── raw/ # Corpus obtenido por scraping
│ │ │ └── processed/ # Corpus limpio y procesado
│ │ └── config/
│ │ └── languages.json # Configuración de intenciones
│ │
│ ├── db/
│ │ ├── database.py # Configuración SQLite
│ │ └── crud.py # Operaciones CRUD
│ │
│ └── utils/
│ └── logger.py # Sistema de logging
│
├── scrappers/
│ ├── wikipedia_scrapper.py # Scraping automático desde Wikipedia
│ └── scrapper_corpus.py # Procesamiento del corpus
│
├── streamlit_app.py # Interfaz web
├── requirements.txt # Dependencias del proyecto
└── README.md

---

## 🔍 Obtención y Procesamiento del Corpus

### Scraping automático
Se utiliza la librería `wikipediaapi` para extraer información relevante sobre **Procesamiento del Lenguaje Natural** en cada idioma.

Idiomas soportados:
- Español
- Inglés
- Francés
- Italiano

### Limpieza y procesamiento
El corpus pasa por:
- Eliminación de referencias `[1]`
- Limpieza de símbolos
- Segmentación por frases con NLTK
- Filtrado de frases cortas o irrelevantes
- Normalización lingüística (stopwords, stemming, lematización)

Esto garantiza un **corpus limpio, coherente y de alta calidad**.

---

## 🧠 Modelo NLP Utilizado

El chatbot utiliza un enfoque **clásico y explicable de PLN**, sin LLMs:

### Pipeline semántico
- **TF-IDF** → representación vectorial
- **LSA (TruncatedSVD)** → reducción semántica
- **Cosine Similarity** → selección de respuesta

Este enfoque permite:
- Control total del conocimiento
- Respuestas reproducibles
- Bajo coste computacional
- Facilidad de explicación académica

---

## 🎯 Detección de Intención

Se utiliza un sistema basado en **palabras clave por idioma**, configurable desde `languages.json`.

Intenciones soportadas:
- `definition` → ¿Qué es...?
- `usage` → ¿Para qué sirve...?
- `history` → Historia y origen
- `general` → Conversación abierta

La intención influye directamente en:
- El peso del contexto
- La consulta semántica
- El tipo de respuesta generada

---

## 😊 Análisis de Sentimiento

Sistema híbrido:
- **TextBlob** → polaridad base
- **Diccionarios manuales multilenguaje** → refuerzo semántico

Sentimientos detectados:
- Positive
- Neutral
- Negative

El sentimiento afecta al **fallback emocional** y al tono de la respuesta.

---

## 🗄️ Persistencia y Contexto

Todas las conversaciones se almacenan en una base de datos **SQLite**, guardando:
- Mensaje del usuario
- Respuesta del bot
- Idioma
- Sentimiento
- Polaridad

El bot utiliza los **últimos mensajes del usuario** como contexto para mejorar la coherencia conversacional.

---

## 🎨 Interfaz de Usuario (Streamlit)

La aplicación cuenta con:
- Modo oscuro
- Mensajes diferenciados (usuario / bot)
- Indicador de idioma y sentimiento
- Botón de nueva conversación
- Diseño limpio y moderno

Pensada tanto para **uso académico** como para **demostraciones profesionales**.

---

## ⚙️ Requisitos del Sistema

### Software
- Python 3.9+
- SQLite
- Navegador web moderno

### Dependencias principales

fastapi
uvicorn
streamlit
scikit-learn
nltk
textblob
langdetect
wikipedia-api
sqlalchemy

---

## ▶️ Ejecución del Proyecto

### 1. Instalar dependencias
```bash
pip install -r requirements.txt


