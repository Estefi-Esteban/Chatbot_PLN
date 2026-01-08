# 🤖 Chatbot PLN Multilenguaje

Chatbot basado en **Procesamiento del Lenguaje Natural (PLN clásico)** que incorpora contexto conversacional, análisis de sentimiento, persistencia de memoria y soporte multilenguaje. El sistema utiliza técnicas tradicionales como **TF-IDF** y **cosine similarity**, integrando un backend con **FastAPI** y un frontend interactivo con **Streamlit**.

---

## ✨ Características principales

* PLN clásico (TF-IDF + similitud coseno)
* Contexto conversacional con persistencia (SQLite)
* Análisis de sentimiento (TextBlob + corrección manual en español)
* Soporte multilenguaje (ES, EN, FR, IT)
* Respuestas empáticas según sentimiento
* Frontend tipo chat (Streamlit)
* API REST con FastAPI
* Arquitectura modular y extensible

---

## 🏗️ Arquitectura del proyecto

```
Chatbot_PLN/
│
├── app/
│   ├── api/            # Rutas FastAPI
│   ├── chatbot/        # Núcleo PLN
│   ├── db/             # Base de datos SQLite
│   └── main.py         # Entrada FastAPI
│
├── data/               # Corpus multilenguaje
├── streamlit.py        # Interfaz gráfica
├── requirements.txt
└── README.md
```

---

## 🚀 Cómo ejecutar el proyecto

### 1️⃣ Crear entorno virtual

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3️⃣ Ejecutar backend (FastAPI)

```bash
uvicorn app.main:app --reload
```

Backend disponible en:

```
http://127.0.0.1:8000
```

Swagger UI:

```
http://127.0.0.1:8000/docs
```

### 4️⃣ Ejecutar frontend (Streamlit)

```bash
streamlit run streamlit.py
```

---

## 🧠 Tecnologías utilizadas

* Python 3.12
* FastAPI
* Streamlit
* Scikit-learn
* NLTK
* TextBlob
* SQLite

---

## 📊 Ejemplo de uso

* Preguntas informativas sobre PLN o IA
* Conversaciones encadenadas usando contexto
* Detección automática de idioma
* Respuestas adaptadas al sentimiento del usuario

---

## ⚠️ Limitaciones

* No utiliza modelos generativos (LLMs)
* Dependencia de similitud léxica (TF-IDF)
* No comprensión semántica profunda

Estas limitaciones son propias del enfoque clásico y se abordan en la memoria del proyecto.

---

## 👩‍🎓 Autora

**Estefanía**
Estudiante de Inteligencia Artificial

---

✨ Proyecto académico desarrollado con fines educativos.
