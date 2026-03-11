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
    cursor = conn.cursor()
    
    # 1. Leer datos de la tabla de Fútbol
    query = "SELECT id, title FROM RawFootballNews"
    df = pd.read_sql(query, conn)
    
    # 2. Inicializar analizador
    analyzer = SentimentIntensityAnalyzer()
    results = []
    
    for index, row in df.iterrows():
        score = analyzer.polarity_scores(row['title'])['compound']
        
        if score >= 0.05:
            label = 'Positivo'
        elif score <= -0.05:
            label = 'Negativo'
        else:
            label = 'Neutral'
            
        results.append((row['id'], row['title'], score, label))
    
    # 3. Limpiar tabla de destino para evitar errores de ID duplicado (Truncate)
    # Esto asegura que tu dashboard siempre tenga la versión más fresca
    cursor.execute("TRUNCATE TABLE ProcessedFootballSentiment")
    
    # 4. Guardar resultados en la tabla correcta
    cursor.executemany("""
        INSERT INTO ProcessedFootballSentiment (id, title, sentiment_score, sentiment_label)
        VALUES (?, ?, ?, ?)
    """, results)
    
    conn.commit()
    print(f"⚽ Procesamiento de Fútbol completado: {len(results)} filas analizadas.")
    
    cursor.close()
    conn.close()

if __name__ == "__main__":
    process_sentiment()