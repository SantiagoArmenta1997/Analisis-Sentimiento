# ⚽ Football Intelligence & Sentiment Analysis Pipeline

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) ![SQL Server](https://img.shields.io/badge/SQL_Server-2019+-red.svg) ![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-orange.svg)

Este proyecto es un **Pipeline de Datos End-to-End** diseñado para integrar información subjetiva (sentimiento de prensa) con datos objetivos (estadísticas reales de liga). Automatiza la extracción, limpieza, almacenamiento y visualización de datos de las principales ligas europeas: **Premier League, La Liga y Bundesliga.**



## 🚀 Funcionalidades
* **Ingesta Multi-Fuente:** Extracción de noticias vía `NewsAPI` y estadísticas deportivas vía `Football-Data.org`.
* **Arquitectura SQL Server:** Almacenamiento robusto en tablas relacionales (`LeagueStandings`, `LeagueScorers`, `LeagueAssists`).
* **Análisis de Sentimiento (NLP):** Uso de la librería `VADER` para clasificar el impacto de las noticias en el entorno futbolístico.
* **Dashboard Interactivo:** Interfaz en **Streamlit** con filtros dinámicos por liga y visualización en tres columnas (Posiciones, Goleadores, Asistidores).
* **Data Enrichment:** Lógica programada para manejar limitaciones de APIs y asegurar la integridad visual del dashboard.

## 🏗️ Estructura del Proyecto

```text
├── src/
│   ├── Ingesta.py          # Extracción de noticias (NewsAPI)
│   ├── Ingesta_Stats.py    # Extracción de estadísticas (Football-Data API)
│   ├── Procesar.py         # Lógica de NLP y Sentimiento
│   └── app.py              # Dashboard de Streamlit
├── main.py                 # Orquestador principal del pipeline
├── requirements.txt        # Dependencias del proyecto
└── README.md

## ⚙️ Personalización y Configuración

Para que el proyecto funcione en tu entorno local, debes modificar los siguientes campos en los scripts:

1.  **API Keys:**
    * En `src/Ingesta.py`: Ingresa tu API Key de NewsAPI.
    * En `src/Ingesta_Stats.py`: Ingresa tu API Key de Football-Data.org en la variable `API_KEY`.

2.  **Base de Datos (SQL Server):**
    * Los scripts `src/Ingesta_Stats.py` y `src/app.py` contienen variables `SERVER` y `DATABASE`. 
    * Por defecto, `SERVER` es `localhost`. Si tu instancia tiene un nombre específico (ej. `SQLEXPRESS`), cámbialo allí.
    * Asegúrate de tener instalado el **ODBC Driver 17 for SQL Server**.

3.  **Lógica de Negocio:**
    * Si deseas agregar más ligas, simplemente expande el diccionario `LEAGUES` en los scripts de ingesta y ajusta el mapeo en el dashboard.