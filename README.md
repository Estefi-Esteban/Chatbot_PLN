# 🤖 Chatbot PLN Multilenguaje con Análisis Semántico y Emocional

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Status](https://img.shields.io/badge/Status-Terminado-success?style=for-the-badge)

Proyecto avanzado de **Procesamiento del Lenguaje Natural (PLN)** que implementa un **chatbot multilenguaje** capaz de comprender preguntas técnicas, detectar intención, analizar sentimiento y responder utilizando **búsqueda semántica** sobre corpus reales obtenidos automáticamente desde Wikipedia.

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

## 📁 Estructura del Proyecto

CHATBOT_PLN/
│
├── app/
│   ├── __pycache__/
│   │
│   ├── api/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   └── routes.py              # Endpoints FastAPI del chatbot
│   │
│   ├── chatbot/
│   │   ├── __pycache__/
│   │   ├── core.py                # Núcleo del chatbot (LSA + contexto + emociones)
│   │   ├── language.py            # Detección de idioma (heurísticas + langdetect)
│   │   ├── preprocessing.py       # Normalización y limpieza de texto
│   │   └── sentiment.py           # Análisis de sentimiento multilenguaje
│   │
│   ├── db/
│   │   ├── __pycache__/
│   │   ├── crud.py                # Operaciones CRUD para la base de datos
│   │   ├── database.py            # Configuración SQLite
│   │   ├── models.py              # Modelos ORM
│   │   └── __init__.py
│   │
│   ├── utils/
│   │   ├── __pycache__/
│   │   ├── logger.py              # Sistema de logging
│   │   └── download_nltk.py       # Descarga automática de recursos NLTK
│   │
│   ├── main.py                    # Punto de entrada FastAPI
│   └── schemas.py                 # Esquemas Pydantic
│
├── data/
│   ├── config/
│   │   └── languages.json         # Intents y keywords por idioma
│   │
│   ├── corpora/
│   │   ├── processed/             # Corpus limpio y tokenizado
│   │   │   ├── corpus_en.txt
│   │   │   ├── corpus_es.txt
│   │   │   ├── corpus_fr.txt
│   │   │   └── corpus_it.txt
│   │   │
│   │   └── raw/                   # Corpus original extraído de Wikipedia
│   │       ├── corpus_en_api.txt
│   │       ├── corpus_es_api.txt
│   │       ├── corpus_fr_api.txt
│   │       └── corpus_it_api.txt
│   │       
│   ├── corpus_processor.py        # Procesamiento del corpus
│   └── scrapper/
│       └── wikipedia_scrapper.py  # Scraping automático de Wikipedia
│
├── frontend/
│   └── streamlit_app.py           # Interfaz gráfica con Streamlit
│
├── chatbot.db                     # Base de datos SQLite
├── requirements.txt               # Dependencias del proyecto
├── README.md                      # Documentación del proyecto
├── .gitignore
└── venv/                          # Entorno virtual


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

## 🛠️ Cómo ampliar el conocimiento (Corpus)

El chatbot puede aprender sobre nuevos temas fácilmente añadiendo nuevas fuentes de Wikipedia. Para ello, sigue este flujo de trabajo:

### 1. Añadir nuevas fuentes
Modifica el archivo `data/scrapper/wikipedia_scrapper.py`. Busca la lista de temas/títulos y añade las páginas de Wikipedia que desees (ej. *"Deep Learning"*, *"Transformer (machine learning model)"*).

### 2. Ejecutar el Scraper
Descarga la información en bruto ("raw") ejecutando:
```bash
python data/cropora/corpus_processor.py
```

### 3. Procesar y Limpiar el Corpus
Es **crucial** ejecutar el procesador después del scraping. Este script normaliza el texto, elimina ruidoy prepara los datos para el modelo TF-IDF:
```bash
python data/corpora/corpus_processor.py 
```
**Nota**: Si no ejecutas este paso, el bot no "verá" los nuevos datos añadidos.

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
```

### 2. Ejecutar el backend
```bash
uvicorn app.main:app --reload
```

### 3. Ejecutar la interfaz
```bash
streamlit run streamlit_app.py
```

---

## 🧪 Ejemplos de Uso

- 📌 **Preguntas técnicas**
  - ¿Qué es el procesamiento del lenguaje natural?
  - *What are NLP applications?*

- 💬 **Conversación emocional**
  - *Hoy es un día horrible*

- 🌍 **Multilenguaje**
  - *Aujourd’hui est une mauvaise journée*
  - *Oggi mi sento triste*

---

## 📦 Repositorio

El código fuente completo está disponible en GitHub y puede ampliarse fácilmente con:

* Nuevos idiomas
* Más fuentes de datos
* Modelos híbridos (PLN + LLM)
* Integración de Transformers de Hugging Face

---

## 👩‍🎓 Autora

**Estefanía**

Estudiante de Inteligencia Artificial  
Proyecto de Procesamiento del Lenguaje Natural
