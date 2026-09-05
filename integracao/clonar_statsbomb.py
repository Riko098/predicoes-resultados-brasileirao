"""
Solução Alternativa: Clonar repositório StatsBomb para uso local
Mais confiável que acessar via HTTP
"""

import subprocess
import json
import pandas as pd
from pathlib import Path

def clonar_statsbomb():
    """Clona repositório do StatsBomb localmente"""
    print("=" * 60)
    print("CLONANDO REPOSITÓRIO STATSBOMB")
    print("=" * 60)
    
    repo_path = Path("statsbomb_data")
    
    if repo_path.exists():
        print(f"✓ Repositório já existe em: {repo_path}")
        return repo_path
    
    print("\nClonando estatsbomb/open-data...")
    print("(Isso pode levar alguns minutos)\n")
    
    try:
        subprocess.run([
            "git", "clone", "--depth", "1",
            "https://github.com/statsbomb/open-data.git",
            str(repo_path)
        ], check=True, capture_output=False)
        
        print("\n✓ Clone concluído!")
        return repo_path
        
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro ao clonar: {e}")
        return None

def explorar_competicoes(repo_path):
    """Explora competições disponíveis"""
    print("\n" + "=" * 60)
    print("COMPETIÇÕES DISPONÍVEIS")
    print("=" * 60)
    
    comp_file = repo_path / "data" / "competitions.json"
    
    with open(comp_file, 'r', encoding='utf-8') as f:
        competicoes = json.load(f)
    
    df = pd.DataFrame(competicoes)
    
    print(f"\n✓ {len(df)} competições encontradas\n")
    
    # Mostrar competições do Brasil
    brasil = df[df['competition_name'].str.contains('Serie|Brazil|Brasileir', case=False, na=False)]
    
    if len(brasil) > 0:
        print("🇧🇷 BRASIL:")
        print("-" * 60)
        for _, row in brasil.iterrows():
            print(f"ID: {row['competition_id']:4d} | {row['competition_name']:25s} | {row['season_name']}")
    
    # Mostrar outras competições disponíveis
    print("\n📊 OUTRAS COMPETIÇÕES:")
    print("-" * 60)
    outros = df[~df['competition_name'].str.contains('Serie|Brazil|Brasileir', case=False, na=False)]
    
    for _, row in outros.head(15).iterrows():
        print(f"ID: {row['competition_id']:4d} | {row['competition_name']:25s} | {row['season_name']}")
    
    print(f"\n... e mais {len(outros) - 15} competições")
    
    return df

def explorar_partidas(repo_path, competition_id, season_id):
    """Explora partidas de uma competição"""
    print("\n" + "=" * 60)
    print(f"PARTIDAS: Competition ID {competition_id}, Season {season_id}")
    print("=" * 60)
    
    match_file = repo_path / "data" / "matches" / str(competition_id) / f"{season_id}.json"
    
    if not match_file.exists():
        print(f"✗ Arquivo não encontrado: {match_file}")
        return None
    
    with open(match_file, 'r', encoding='utf-8') as f:
        partidas = json.load(f)
    
    df = pd.DataFrame(partidas)
    print(f"\n✓ {len(df)} partidas encontradas\n")
    
    # Mostrar primeiras
    for idx, row in df.head(5).iterrows():
        home = row['home_team']['name']
        away = row['away_team']['name']
        score_home = row['home_score']
        score_away = row['away_score']
        status = row['status']
        
        print(f"{home:20s} {score_home:2} x {score_away:<2} {away:20s} [{status}]")
    
    print(f"\n... e mais {len(df) - 5} partidas")
    
    return df

def explorar_eventos(repo_path, match_id):
    """Explora eventos de uma partida"""
    print("\n" + "=" * 60)
    print(f"EVENTOS: Match ID {match_id}")
    print("=" * 60)
    
    event_file = repo_path / "data" / "events" / f"{match_id}.json"
    
    if not event_file.exists():
        print(f"✗ Arquivo não encontrado: {event_file}")
        return None
    
    with open(event_file, 'r', encoding='utf-8') as f:
        eventos = json.load(f)
    
    print(f"\n✓ {len(eventos)} eventos encontrados\n")
    
    # Contar tipos de eventos
    tipos = {}
    for e in eventos:
        tipo = e['type']['name']
        tipos[tipo] = tipos.get(tipo, 0) + 1
    
    print("Tipos de eventos (Top 15):")
    print("-" * 40)
    for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True)[:15]:
        barra = "█" * (count // 10)
        print(f"{tipo:20s}: {count:4d} {barra}")
    
    return eventos

def main():
    print("\n")
    
    # 1. Clonar repositório
    repo_path = clonar_statsbomb()
    if not repo_path:
        return
    
    # 2. Explorar competições
    competicoes = explorar_competicoes(repo_path)
    
    # 3. Se houver Brasil, explorar partidas
    brasil = competicoes[competicoes['competition_name'].str.contains('Serie|Brazil', case=False, na=False)]
    
    if len(brasil) > 0:
        comp_id = brasil.iloc[0]['competition_id']
        season_id = brasil.iloc[0]['season_id']
        
        partidas = explorar_partidas(repo_path, comp_id, season_id)
        
        # 4. Se houver partidas, explorar eventos
        if partidas is not None and len(partidas) > 0:
            match_id = partidas.iloc[0]['match_id']
            eventos = explorar_eventos(repo_path, match_id)
    else:
        print("\n⚠️  Brasil não encontrado. Explorando outra competição...")
        comp_id = competicoes.iloc[5]['competition_id']
        season_id = competicoes.iloc[5]['season_id']
        
        partidas = explorar_partidas(repo_path, comp_id, season_id)
    
    print("\n" + "=" * 60)
    print("✓ EXPLORAÇÃO CONCLUÍDA!")
    print("=" * 60)
    print(f"\nDados salvos em: {repo_path}")
    print("\nPróximos passos:")
    print("1. Explore integracao_statsbomb.py para usar os dados")
    print("2. Crie features engineering com os dados locais")
    print("3. Integre com seu modelo de predição")

if __name__ == "__main__":
    main()
