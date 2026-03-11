# ⚽ Football News Sentiment Analysis Pipeline

Este proyecto es un pipeline de datos (ETL) automatizado que extrae noticias de fútbol en tiempo real, realiza un análisis de sentimiento utilizando Procesamiento de Lenguaje Natural (NLP) y visualiza los resultados en un dashboard interactivo.



## 🚀 Características Principales

* **Ingesta Automatizada:** Extracción de noticias mediante NewsAPI con carga directa a **SQL Server**.
* **Análisis de Sentimiento:** Procesamiento con la librería **VADER** para clasificar el tono de la prensa deportiva (Positivo, Negativo, Neutral).
* **Orquestación:** Script maestro (`main.py`) que gestiona el flujo de ejecución y manejo de rutas absolutas.
* **Dashboard BI:** Visualización dinámica construida en **Streamlit** con métricas clave de sentimiento.

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.11+
* **Base de Datos:** Microsoft SQL Server (T-SQL)
* **Librerías:** Pandas, SQLAlchemy, PyODBC, VaderSentiment, Streamlit, Requests.
* **Entorno:** VS Code & Anaconda.

## 📁 Estructura del Proyecto

```text
Proyecto-Analisis-Sentimiento/
├── main.py                # Orquestador principal (Entry point)
├── requirements.txt       # Dependencias del proyecto
├── .gitignore             # Archivos excluidos (Credenciales, __pycache__)
└── src/                   # Código fuente
    ├── Ingesta.py         # Extracción de API a SQL
    ├── Procesar.py        # Análisis de sentimiento y actualización de SQL
    └── app.py             # Dashboard de Streamlit