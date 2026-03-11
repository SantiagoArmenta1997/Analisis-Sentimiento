import pyodbc
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Configuración de conexión
conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=localhost;'
    r'DATABASE=PortfolioProjects;'
    r'Trusted_Connection=yes;'
)

def process_sentiment():
    conn = pyodbc.connect(conn_str)
    
    # 1. Leer datos de SQL
    query = "SELECT id, title FROM RawNews"
    df = pd.read_sql(query, conn)
    
    # 2. Inicializar analizador de sentimiento
    analyzer = SentimentIntensityAnalyzer()
    
    results = []
    
    for index, row in df.iterrows():
        # Analizar el título (suele ser más preciso que el contenido cortado de la API)
        score = analyzer.polarity_scores(row['title'])['compound']
        
        # Clasificar
        if score >= 0.05:
            label = 'Positivo'
        elif score <= -0.05:
            label = 'Negativo'
        else:
            label = 'Neutral'
            
        results.append((row['id'], row['title'], score, label))
    
    # 3. Guardar resultados en la nueva tabla
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO ProcessedNews (id, title, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?)
    """, results)
    
    conn.commit()
    print(f"Procesamiento completado: {len(results)} filas analizadas.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    process_sentiment()