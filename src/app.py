import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Conexión
engine = create_engine("mssql+pyodbc://localhost/PortfolioProjects?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

st.set_page_config(layout="wide", page_title="Football Intelligence") 
st.title("⚽ Central de Inteligencia de Fútbol")

# 1. Configuración del Selector
opciones_ligas = {"PL": "Premier League", "PD": "La Liga", "BL1": "Bundesliga"}

liga_cod = st.selectbox(
    "Seleccionar Liga", 
    options=list(opciones_ligas.keys()), 
    format_func=lambda x: opciones_ligas[x]
)

# 2. Carga de datos desde SQL
try:
    df_pos = pd.read_sql(f"SELECT * FROM LeagueStandings WHERE league='{liga_cod}'", engine)
    df_gol = pd.read_sql(f"SELECT * FROM LeagueScorers WHERE league='{liga_cod}'", engine)
    df_ast = pd.read_sql(f"SELECT * FROM LeagueAssists WHERE league='{liga_cod}'", engine)

    # 3. Renderizado en 3 columnas
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("🏆 Standings (Top 3)")
        if not df_pos.empty:
            # Limpieza segura de la forma (Last 5 en inglés)
            df_pos['form'] = (df_pos['form']
                              .fillna('N/A') # Evita errores si hay nulos
                              .str.replace(',', '', regex=False)
                              .str.slice(-5))
            
            st.dataframe(df_pos[['team', 'points', 'gd', 'form']], 
                         hide_index=True,
                         column_config={"team": "Team", "points": "Pts", "gd": "GD", "form": "Form"})
        else:
            st.info("No hay datos de posiciones para esta liga.")

    with c2:
        st.subheader("🎯 Top Scorers")
        if not df_gol.empty:
            st.dataframe(df_gol[['player', 'goals', 'team']], hide_index=True)
        else:
            st.info("No hay datos de goleadores.")

    with c3:
        st.subheader("🅰️ Top Assists")
        if not df_ast.empty:
            st.dataframe(df_ast[['player', 'assists', 'team']], hide_index=True)
        else:
            st.info("No hay datos de asistencias.")

except Exception as e:
    st.error(f"Error de conexión o de tabla: {e}")
    st.warning("Asegúrate de haber ejecutado 'python src/Ingesta_Stats.py' primero.")