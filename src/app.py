import streamlit as st
import pyodbc
import pandas as pd
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Sentiment Analysis Dashboard", layout="wide")
st.title("📊 Dashboard de Sentimiento de Noticias")

# Conexión a SQL Server
def get_data():
    conn_str = (
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost;'
        r'DATABASE=PortfolioProjects;'
        r'Trusted_Connection=yes;'
    )
    conn = pyodbc.connect(conn_str)
    query = "SELECT * FROM ProcessedNews"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = get_data()

# --- Layout de Streamlit ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución de Sentimientos")
    sentiment_counts = df['sentiment_label'].value_counts()
    st.bar_chart(sentiment_counts)

with col2:
    st.subheader("Métricas Clave")
    avg_score = df['sentiment_score'].mean()
    st.metric("Score Promedio", f"{avg_score:.2f}")
    st.write("Un score cercano a 1 es muy positivo, cercano a -1 es muy negativo.")

st.divider()

st.subheader("Detalle de las Noticias")
st.dataframe(df[['title', 'sentiment_label', 'sentiment_score']], width='stretch')