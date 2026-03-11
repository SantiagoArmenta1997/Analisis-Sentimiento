import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("mssql+pyodbc://localhost/PortfolioProjects?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

st.set_page_config(layout="wide") # Importante para que quepan las 3 tablas
st.title("⚽ Central de Inteligencia de Fútbol")

# Selector
liga_cod = st.selectbox("Seleccionar Liga", ["PL", "PD", "BL1"], 
                         format_func=lambda x: {"PL": "Premier League", "PD": "La Liga", "BL1": "Bundesliga"}[x])

# Carga de datos
df_pos = pd.read_sql(f"SELECT * FROM LeagueStandings WHERE league='{liga_cod}'", engine)
df_gol = pd.read_sql(f"SELECT * FROM LeagueScorers WHERE league='{liga_cod}'", engine)
df_ast = pd.read_sql(f"SELECT * FROM LeagueAssists WHERE league='{liga_cod}'", engine)

# Renderizado en 3 columnas
c1, c2, c3 = st.columns(3)

with c1:
    st.subheader("🏆 Posiciones (Top 3)")
    if not df_pos.empty:
        df_pos['form'] = df_pos['form'].str.replace('W','✅').str.replace('L','❌').str.replace('D','➖').str.replace(',','')
        st.dataframe(df_pos[['team', 'points', 'gd', 'form']], hide_index=True)

with c2:
    st.subheader("🎯 Máximos Goleadores")
    st.dataframe(df_gol[['player', 'goals', 'team']], hide_index=True)

with c3:
    st.subheader("🅰️ Máximos Asistidores")
    st.dataframe(df_ast[['player', 'assists', 'team']], hide_index=True)