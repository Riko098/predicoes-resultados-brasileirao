"""
Solucao Alternativa: Clonar repositorio StatsBomb para uso local
Mais confiavel que acessar via HTTP
"""

import subprocess
import json
import pandas as pd
from pathlib import Path
import sys
import os

# Configurar encoding UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

def clonar_statsbomb():
    """Clona repositorio do StatsBomb localmente"""
    print("=" * 60)
    print("CLONANDO REPOSITORIO STATSBOMB")
    print("=" * 60)
    
    repo_path = Path("statsbomb_data")
    
    if repo_path.exists():
        print(f"[OK] Repositorio ja existe em: {repo_path}")
        return repo_path
    
    print("\nClonando statsbomb/open-data...")
    print("(Isso pode levar alguns minutos)\n")
    
    try:
        subprocess.run([
            "git", "clone", "--depth", "1",
            "https://github.com/statsbomb/open-data.git",
            str(repo_path)
        ], check=True, capture_output=False)
        
        print("\n[OK] Clone concluido!")
        return repo_path
        
    except subprocess.CalledProcessError as e:
        print(f"[ERRO] Ao clonar: {e}")
        return None

def explorar_competicoes(repo_path):
    """Explora competicoes disponiveis"""
    print("\n" + "=" * 60)
    print("COMPETICOES DISPONIVEIS")
    print("=" * 60)
    
    comp_file = repo_path / "data" / "competitions.json"
    
    with open(comp_file, 'r', encoding='utf-8') as f:
        competicoes = json.load(f)
    
    df = pd.DataFrame(competicoes)
    
    print(f"\n[OK] {len(df)} competicoes encontradas\n")
    
    # Mostrar competições do Brasil
    brasil = df[df['competition_name'].str.contains('Serie|Brazil|Brasileir', case=False, na=False)]
    
    if len(brasil) > 0:
        print("[BRASIL - SERIE A]:")
        print("-" * 60)
        for _, row in brasil.iterrows():
            print(f"ID: {row['competition_id']:4d} | {row['competition_name']:25s} | {row['season_name']}")
    
    # Mostrar outras competições disponíveis
    print("\n[OUTRAS COMPETICOES]:")
    print("-" * 60)
    outros = df[~df['competition_name'].str.contains('Serie|Brazil|Brasileir', case=False, na=False)]
    
    for _, row in outros.head(15).iterrows():
        print(f"ID: {row['competition_id']:4d} | {row['competition_name']:25s} | {row['season_name']}")
    
    print(f"\n... e mais {len(outros) - 15} competicoes")
    
    return df

def explorar_partidas(repo_path, competition_id, season_id):
    """Explora partidas de uma competição"""
    print("\n" + "=" * 60)
    print(f"PARTIDAS: Competition ID {competition_id}, Season {season_id}")
    print("=" * 60)
    
    match_file = repo_path / "data" / "matches" / str(competition_id) / f"{season_id}.json"
    
    if not match_file.exists():
        print(f"[ERRO] Arquivo nao encontrado: {match_file}")
        return None
    
    try:
        with open(match_file, 'r', encoding='utf-8') as f:
            partidas = json.load(f)
        
        df = pd.DataFrame(partidas)
        print(f"\n[OK] {len(df)} partidas encontradas\n")
        
        # Mostrar primeiras - com tratamento robusto
        for idx, row in df.head(5).iterrows():
            try:
                # Tenta acessar o nome do time
                if isinstance(row.get('home_team'), dict):
                    home = row['home_team'].get('name', 'Unknown')
                else:
                    home = str(row.get('home_team', 'Unknown'))
                    
                if isinstance(row.get('away_team'), dict):
                    away = row['away_team'].get('name', 'Unknown')
                else:
                    away = str(row.get('away_team', 'Unknown'))
                
                score_home = row.get('home_score', '-')
                score_away = row.get('away_score', '-')
                status = row.get('status', 'unknown')
                
                print(f"{home:20s} {score_home:2} x {score_away:<2} {away:20s} [{status}]")
            except Exception as e:
                print(f"  Erro ao processar linha: {e}")
                continue
        
        if len(df) > 5:
            print(f"\n... e mais {len(df) - 5} partidas")
        
        return df
        
    except Exception as e:
        print(f"[ERRO] Ao carregar partidas: {e}")
        print(f"   Arquivo: {match_file}")
        return None

def explorar_eventos(repo_path, match_id):
    """Explora eventos de uma partida"""
    print("\n" + "=" * 60)
    print(f"EVENTOS: Match ID {match_id}")
    print("=" * 60)
    
    event_file = repo_path / "data" / "events" / f"{match_id}.json"
    
    if not event_file.exists():
        print(f"[ERRO] Arquivo nao encontrado: {event_file}")
        return None
    
    try:
        with open(event_file, 'r', encoding='utf-8') as f:
            eventos = json.load(f)
        
        print(f"\n[OK] {len(eventos)} eventos encontrados\n")
        
        # Contar tipos de eventos com tratamento robusto
        tipos = {}
        for e in eventos:
            try:
                tipo = e.get('type', {})
                if isinstance(tipo, dict):
                    tipo_nome = tipo.get('name', 'Unknown')
                else:
                    tipo_nome = str(tipo)
                tipos[tipo_nome] = tipos.get(tipo_nome, 0) + 1
            except:
                tipos['Unknown'] = tipos.get('Unknown', 0) + 1
        
        print("Tipos de eventos (Top 15):")
        print("-" * 40)
        for tipo, count in sorted(tipos.items(), key=lambda x: x[1], reverse=True)[:15]:
            barra = "#" * (count // 10)
            print(f"{tipo:20s}: {count:4d} {barra}")
        
        return eventos
        
    except Exception as e:
        print(f"[ERRO] Ao carregar eventos: {e}")
        return None

def main():
    print("\n")
    
    # 1. Clonar repositório (se ainda não existe)
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
            # Procurar primeira partida completa com eventos
            for idx, row in partidas.iterrows():
                match_id = row.get('match_id')
                if match_id:
                    event_file = repo_path / "data" / "events" / f"{match_id}.json"
                    if event_file.exists():
                        eventos = explorar_eventos(repo_path, match_id)
                        break
    else:
        print("\n[AVISO] Brasil nao encontrado. Explorando outra competicao...")
        if len(competicoes) > 5:
            comp_id = competicoes.iloc[5]['competition_id']
            season_id = competicoes.iloc[5]['season_id']
            
            partidas = explorar_partidas(repo_path, comp_id, season_id)
    
    print("\n" + "=" * 60)
    print("[OK] EXPLORACAO CONCLUIDA!")
    print("=" * 60)
    print(f"\nDados salvos em: {repo_path}")
    print("\nProximos passos:")
    print("1. Explore integracao/integracao_statsbomb.py para usar os dados")
    print("2. Crie features engineering com os dados locais")
    print("3. Integre com seu modelo de predicao")

if __name__ == "__main__":
    main()
