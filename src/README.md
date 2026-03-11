# 📊 Análisis de Sentimiento de Noticias con SQL Server & NLP

Este proyecto es un pipeline de datos completo (ETL) que extrae noticias globales, las almacena en una base de datos relacional, procesa el sentimiento del texto mediante Inteligencia Artificial y visualiza los resultados en un dashboard interactivo.

## 🛠️ Tecnologías Utilizadas
* **Lenguaje:** Python 3.x
* **Base de Datos:** SQL Server (T-SQL)
* **Librerías de Datos:** Pandas, PyODBC, SQLAlchemy
* **NLP:** VADER Sentiment Analysis / Hugging Face
* **Visualización:** Streamlit

## 🏗️ Arquitectura del Proyecto
1. **Ingesta:** Script en Python que consume la API de NewsAPI y carga los datos crudos en **SQL Server**.
2. **Procesamiento:** Script de limpieza y análisis de sentimiento que lee desde SQL y actualiza las métricas en una tabla de resultados.
3. **Consumo:** Dashboard en **Streamlit** que se conecta en tiempo real a SQL Server para mostrar KPIs y distribución de sentimientos.

## 🚀 Cómo ejecutar
1. Clonar el repositorio.
2. Configurar la base de datos con el script SQL adjunto.
3. Instalar dependencias: `pip install -r requirements.txt`
4. Ejecutar el dashboard: `streamlit run app.py`

---
*Proyecto desarrollado por Santiago Armenta - Ingeniero de Datos / Data Scientist*