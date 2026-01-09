# 🤖 Chatbot PLN Multilenguaje

Chatbot académico-profesional basado en **Procesamiento del Lenguaje Natural (PLN clásico)**, capaz de mantener **conversaciones multilingües**, analizar **sentimiento**, gestionar **contexto conversacional** y persistir interacciones.

Este proyecto ha sido diseñado con una **arquitectura extensible**, orientada a facilitar la incorporación de nuevos idiomas y funcionalidades avanzadas.

---

## ✨ Características principales

* 🌍 **Soporte multilingüe nativo** (ES, EN, FR, IT)
* 🧠 **PLN clásico** con TF-IDF + Similaridad del coseno
* 💬 **Gestión de contexto conversacional** (historial por sesión)
* 😊 **Análisis de sentimiento multilingüe** (con heurísticas léxicas)
* ❤️ **Respuestas empáticas automáticas** según emoción detectada
* 💾 **Persistencia en base de datos** (historial de conversaciones)
* 🪵 **Sistema de logging profesional**
* 🎨 **Interfaz web interactiva** con Streamlit
* ⚙️ **API REST** con FastAPI

---

## 🏗️ Arquitectura del proyecto

```
app/
├── api/            # Endpoints FastAPI
├── core/           # Lógica principal del chatbot (PLN)
│   ├── core.py
│   ├── preprocessing.py
│   ├── sentiment.py
│   └── language.py
├── db/             # Base de datos y CRUD
├── utils/          # Logger y utilidades
├── data/           # Corpus por idioma
├── streamlit.py    # Interfaz web
└── main.py         # Arranque FastAPI
```

---

## 🧠 Funcionamiento del Chatbot

1. **Detección automática del idioma** del mensaje del usuario.
2. **Normalización del texto** (tokenización, stopwords, stemming/lemmatización).
3. **Análisis de sentimiento** (TextBlob + diccionarios manuales por idioma).
4. **Recuperación del contexto conversacional** desde base de datos.
5. **Cálculo de similitud semántica** usando TF-IDF + cosine similarity.
6. **Selección de la mejor respuesta** desde el corpus.
7. **Fallback empático** si no se encuentra respuesta semántica válida.
8. **Persistencia y logging** de la interacción.

---

## 🌍 Idiomas soportados

| Idioma   | Código | Corpus | Sentimiento |
| -------- | ------ | ------ | ----------- |
| Español  | es     | ✅      | ✅           |
| Inglés   | en     | ✅      | ✅           |
| Francés  | fr     | ✅      | ✅           |
| Italiano | it     | ✅      | ✅           |

➡️ Añadir un nuevo idioma solo requiere:

* Un corpus (`data/corpus_xx.txt`)
* Stopwords y stemmer compatibles
* Diccionario emocional opcional

---

## 🚀 Instalación y ejecución

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tuusuario/chatbot-pln-multilenguaje.git
cd chatbot-pln-multilenguaje
```

### 2️⃣ Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4️⃣ Descargar recursos NLTK

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

### 5️⃣ Ejecutar API (FastAPI)

```bash
uvicorn app.main:app --reload
```

### 6️⃣ Ejecutar interfaz web (Streamlit)

```bash
streamlit run streamlit.py
```

---

## 🪵 Sistema de Logging

El proyecto incorpora **logging estructurado** para:

* Inicialización del chatbot
* Detección de idioma
* Análisis de sentimiento
* Selección de respuesta
* Errores y fallbacks
* Persistencia en base de datos

Esto facilita:

* Debugging
* Auditoría
* Escalabilidad

---

## 🎯 Casos de uso

* Chatbots educativos
* Sistemas de atención al cliente
* Prácticas académicas de PLN
* Análisis conversacional
* Prototipos de IA conversacional

---

## 📌 Tecnologías utilizadas

* **Python 3.10+**
* **FastAPI**
* **Streamlit**
* **NLTK**
* **Scikit-learn**
* **TextBlob**
* **SQLAlchemy**

---

## 📈 Posibles mejoras futuras

* Ranking de respuestas por confianza
* Integración con modelos transformer
* Soporte de voz (STT / TTS)
* Panel de analítica de conversaciones
* Dockerización

---

## 👩‍🎓 Contexto académico

Proyecto desarrollado como práctica avanzada de **Procesamiento del Lenguaje Natural**, enfocado en comprender y aplicar técnicas clásicas de PLN de forma estructurada y extensible.

---

## 👤 Autora

**Estefania**
Estudiante de Inteligencia Artificial

📫 *Contacto y redes disponibles en GitHub / LinkedIn*

---

⭐ Si te gusta este proyecto, ¡no olvides dejar una estrella en GitHub!
