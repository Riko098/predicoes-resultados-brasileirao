"""
Exemplo Rápido: Baixar e Explorar Dados StatsBomb
Execute: python teste_statsbomb.py
"""

import requests
import json
import pandas as pd

def teste_rapido():
    print("=" * 60)
    print("TESTE RÁPIDO: STATSBOMB OPEN DATA")
    print("=" * 60)
    
    # 1. Carregar competições
    print("\n[1] Carregando competições disponíveis...")
    url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/competitions.json"
    
    try:
        response = requests.get(url, timeout=10)
        competicoes = response.json()
        
        df = pd.DataFrame(competicoes)
        print(f"✓ {len(df)} competições encontradas\n")
        
        # Mostrar primeiras
        print("Primeiras 10 competições:")
        print("-" * 60)
        for idx, row in df.head(10).iterrows():
            print(f"ID: {row['competition_id']:2d} | {row['competition_name']:20s} | Temporada: {row['season_name']}")
        
        # Mostrar se há Brasil
        brasil = df[df['competition_name'].str.contains('Brazil|Serie|Brasileir', case=False, na=False)]
        if len(brasil) > 0:
            print("\n✓ Dados de Brasil encontrados:")
            print(brasil[['competition_id', 'competition_name', 'season_name']])
        else:
            print("\n⚠️  Dados de Brasil não encontrados (dados são principalmente europeus)")
        
        # 2. Carregar exemplo de partidas (Serie A Brasil)
        print("\n" + "-" * 60)
        print("[2] Carregando exemplo: Serie A Brasil (2015/2016)...")
        
        # Serie A (Brasil) tem competition_id=12
        match_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/12/1.json"
        match_response = requests.get(match_url, timeout=10)
        
        try:
            partidas = match_response.json()
        except json.JSONDecodeError:
            # Tenta outra competição
            print("  Tentando LaLiga...")
            match_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/matches/4/44.json"
            match_response = requests.get(match_url, timeout=10)
            partidas = match_response.json()
        
        df_partidas = pd.DataFrame(partidas)
        print(f"✓ {len(df_partidas)} partidas carregadas")
        
        # Mostrar exemplo
        if len(df_partidas) > 0:
            primeira = df_partidas.iloc[0]
            print(f"\nExemplo de partida:")
            print(f"  Data: {primeira['match_date']}")
            print(f"  {primeira['home_team']['name']} vs {primeira['away_team']['name']}")
            print(f"  Placar: {primeira['home_score']} x {primeira['away_score']}")
            print(f"  Status: {primeira['status']}")
            print(f"  Match ID: {primeira['match_id']}")
        
        # 3. Carregar eventos de uma partida
        print("\n" + "-" * 60)
        print("[3] Carregando eventos de uma partida...")
        
        if len(df_partidas) > 0 and df_partidas.iloc[0]['status'] == 'complete':
            match_id = df_partidas.iloc[0]['match_id']
            eventos_url = f"https://raw.githubusercontent.com/statsbomb/open-data/master/data/events/{match_id}.json"
            
            eventos_response = requests.get(eventos_url, timeout=10)
            eventos = eventos_response.json()
            
            print(f"✓ {len(eventos)} eventos encontrados")
            
            # Tipos de eventos
            tipos_evento = {}
            for evento in eventos:
                tipo = evento['type']['name']
                tipos_evento[tipo] = tipos_evento.get(tipo, 0) + 1
            
            print("\nTipos de eventos:")
            for tipo, count in sorted(tipos_evento.items(), key=lambda x: x[1], reverse=True)[:10]:
                print(f"  {tipo:25s}: {count:4d}")
            
            # Estatísticas por time
            print("\nEstatísticas por time:")
            for team_name in [df_partidas.iloc[0]['home_team']['name'], 
                             df_partidas.iloc[0]['away_team']['name']]:
                events_team = [e for e in eventos if e.get('team', {}).get('name') == team_name]
                passes = len([e for e in events_team if e['type']['name'] == 'Pass'])
                shots = len([e for e in events_team if e['type']['name'] == 'Shot'])
                tackles = len([e for e in events_team if e['type']['name'] == 'Tackle'])
                
                print(f"  {team_name:20s}: Passes={passes:4d}, Shots={shots:2d}, Tackles={tackles:2d}")
        
        print("\n" + "=" * 60)
        print("✓ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        print("\nPróximos passos:")
        print("1. Revisar integracao_statsbomb.py para uso completo")
        print("2. Combinar com dados do Brasileirão (via API-Football)")
        print("3. Enriquecer seu modelo com novas features")
        
        return True
        
    except requests.exceptions.Timeout:
        print("✗ Timeout: Sem internet ou servidor lento")
        return False
    except Exception as e:
        print(f"✗ Erro: {e}")
        return False

if __name__ == "__main__":
    teste_rapido()
