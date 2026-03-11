import requests
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

# 1. Configuración
API_KEY = '039ebdb3691f41b6867081f1f97e7e05' 
TOPICO = 'Football'

# 2. Conexión a SQL Server
connection_url = (
    "mssql+pyodbc://localhost/PortfolioProjects?"
    "driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes"
)
engine = create_engine(connection_url)

def traer_noticias(query):
    # Calculamos la fecha de hace 30 días para obtener el histórico mensual
    fecha_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    print(f"🔍 Buscando noticias sobre: {query} desde el {fecha_inicio}...")
    
    # Configuramos la URL con el filtro de fecha y relevancia
    url = (
        f'https://newsapi.org/v2/everything?q={query}'
        f'&from={fecha_inicio}'
        f'&language=en'
        f'&sortBy=relevancy'
        f'&pageSize=40' 
        f'&apiKey={API_KEY}'
    )
    
    response = requests.get(url)
    if response.status_code == 200:
        articulos = response.json().get('articles', [])
        return articulos
    else:
        print(f"❌ Error en la API: {response.status_code}")
        return []

def guardar_en_sql(lista_articulos):
    if not lista_articulos:
        print("⚠️ No hay noticias nuevas para guardar.")
        return

    datos = []
    for art in lista_articulos:
        datos.append({
            'source_name': art['source']['name'],
            'author': art.get('author', 'N/A'),
            'title': art['title'],
            'description': art.get('description', ''),
            'url': art['url'],
            'published_at': art['publishedAt'][:19].replace('T', ' '),
            'content': art.get('content', '')
        })
    
    df = pd.DataFrame(datos)

    # --- MANEJO DE DUPLICADOS (TRUNCATE) ---
    with engine.connect() as conn:
        print("🧹 Limpiando tabla RawFootballNews para nuevos datos mensuales...")
        conn.execute(text("TRUNCATE TABLE RawFootballNews"))
        conn.commit()
    
    df.to_sql('RawFootballNews', con=engine, if_exists='append', index=False)
    print(f"✅ Se han guardado {len(df)} noticias del último mes en RawFootballNews.")

if __name__ == "__main__":
    noticias = traer_noticias(TOPICO)
    guardar_en_sql(noticias)