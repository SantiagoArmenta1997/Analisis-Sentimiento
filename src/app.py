import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# ==========================================================
# CONFIGURACIÓN DE USUARIO - INGRESA TU INFORMACIÓN AQUÍ
# ==========================================================
SERVER = 'localhost'
DATABASE = 'PortfolioProjects'
# ==========================================================

engine = create_engine(f"mssql+pyodbc://{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

st.set_page_config(layout="wide", page_title="Football Intel Dashboard") 
st.title("⚽ Central de Inteligencia de Fútbol")

# Mapeo de Ligas para el Selector
opciones_ligas = {"PL": "Premier League", "PD": "La Liga", "BL1": "Bundesliga"}

liga_cod = st.selectbox(
    "Seleccionar Liga", 
    options=list(opciones_ligas.keys()), 
    format_func=lambda x: opciones_ligas[x]
)

try:
    # Consulta de datos filtrados por la liga seleccionada
    df_pos = pd.read_sql(f"SELECT * FROM LeagueStandings WHERE league='{liga_cod}'", engine)
    df_gol = pd.read_sql(f"SELECT * FROM LeagueScorers WHERE league='{liga_cod}'", engine)
    df_ast = pd.read_sql(f"SELECT * FROM LeagueAssists WHERE league='{liga_cod}'", engine)

    # Organización en 3 columnas
    c1, c2, c3 = st.columns(3)

    with c1:
        st.subheader("🏆 Standings (Top 3)")
        if not df_pos.empty:
            # Lógica para ocultar columna 'form' si no hay datos de la API
            columnas_visibles = ['team', 'points', 'gd']
            if not (df_pos['form'].isna().all() or (df_pos['form'] == 'N/A').all()):
                df_pos['form'] = df_pos['form'].str.replace(',', '', regex=False).str.slice(-5)
                columnas_visibles.append('form')
            
            st.dataframe(df_pos[columnas_visibles], hide_index=True,
                         column_config={"team": "Club", "points": "Pts", "gd": "GD", "form": "Last 5"})

    with c2:
        st.subheader("🎯 Top Scorers")
        if not df_gol.empty:
            st.dataframe(df_gol[['player', 'goals', 'team']], hide_index=True,
                         column_config={"player": "Player", "goals": "Goals", "team": "Club"})

    with c3:
        st.subheader("🅰️ Top Assists")
        if not df_ast.empty:
            st.dataframe(df_ast[['player', 'assists', 'team']], hide_index=True,
                         column_config={"player": "Player", "assists": "Assists", "team": "Club"})

except Exception as e:
    st.error(f"Error al cargar datos de SQL Server: {e}")