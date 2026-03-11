import requests
import pandas as pd
from sqlalchemy import create_engine

# ==========================================================
# CONFIGURACIÓN DE USUARIO - INGRESA TU INFORMACIÓN AQUÍ
# ==========================================================
API_KEY = 'TU_API_KEY_AQUÍ'  # Obtén una gratis en https://www.football-data.org/
SERVER = 'localhost'         # Tu servidor de SQL Server (ej. localhost o nombre de instancia)
DATABASE = 'PortfolioProjects'
# ==========================================================

HEADERS = {'X-Auth-Token': API_KEY}
LEAGUES = {'PL': 'Premier League', 'PD': 'La Liga', 'BL1': 'Bundesliga'}

# Conexión a SQL Server usando Autenticación de Windows
engine = create_engine(f"mssql+pyodbc://{SERVER}/{DATABASE}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes")

def get_league_data(league_code):
    """Consulta la API para obtener posiciones y goleadores de una liga específica."""
    
    # 1. Obtener Tabla de Posiciones
    url_standings = f"https://api.football-data.org/v2/competitions/{league_code}/standings"
    res_s = requests.get(url_standings, headers=HEADERS).json()
    standings = []
    if 'standings' in res_s:
        for team in res_s['standings'][0]['table'][:3]: # Top 3 equipos
            standings.append({
                'league': league_code,
                'team': team['team']['name'],
                'played': team['playedGames'],
                'gd': team['goalDifference'],
                'points': team['points'],
                'form': team.get('form', 'N/A')
            })

    # 2. Obtener Máximos Goleadores
    url_scorers = f"https://api.football-data.org/v2/competitions/{league_code}/scorers"
    res_sc = requests.get(url_scorers, headers=HEADERS).json()
    scorers = []
    if 'scorers' in res_sc:
        for s in res_sc['scorers'][:3]: # Top 3 goleadores
            scorers.append({
                'league': league_code,
                'player': s['player']['name'],
                'team': s['team']['name'],
                'goals': s['numberOfGoals']
            })
            
    # 3. Datos de Asistidores (Enriquecimiento manual debido a limitaciones de API gratuita)
    assists_map = {
        'PL': [{'player': 'Mohamed Salah', 'team': 'Liverpool', 'assists': 10}, {'player': 'Cole Palmer', 'team': 'Chelsea', 'assists': 9}],
        'PD': [{'player': 'Lamine Yamal', 'team': 'Barcelona', 'assists': 8}, {'player': 'Raphinha', 'team': 'Barcelona', 'assists': 7}],
        'BL1': [{'player': 'Harry Kane', 'team': 'Bayern', 'assists': 7}, {'player': 'Omar Marmoush', 'team': 'Frankfurt', 'assists': 7}]
    }
    assists = [{'league': league_code, **a} for a in assists_map.get(league_code, [])]
            
    return standings, scorers, assists

def run_ingesta():
    """Ejecuta el pipeline de ingesta para todas las ligas configuradas."""
    all_standings, all_scorers, all_assists = [], [], []
    
    for code in LEAGUES.keys():
        print(f"Extrayendo datos de: {LEAGUES[code]}...")
        s, sc, a = get_league_data(code)
        all_standings.extend(s)
        all_scorers.extend(sc)
        all_assists.extend(a)
    
    # Carga de DataFrames a SQL Server (Reemplaza los datos existentes)
    pd.DataFrame(all_standings).to_sql('LeagueStandings', engine, if_exists='replace', index=False)
    pd.DataFrame(all_scorers).to_sql('LeagueScorers', engine, if_exists='replace', index=False)
    pd.DataFrame(all_assists).to_sql('LeagueAssists', engine, if_exists='replace', index=False)
    print("✅ Proceso completado: SQL Server actualizado.")

if __name__ == "__main__":
    run_ingesta()