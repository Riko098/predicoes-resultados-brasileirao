"""
Analise Avancada de Predicoes com StatsBomb
Processa multiplas partidas e gera estatisticas
"""

import json
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

def carregar_modelos(caminho='modelos/modelos_futebol.pkl'):
    """Carrega configuracao e modelos"""
    try:
        with open(caminho, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"[ERRO] {e}")
        return None

def extrai_nomes_times(partida, eventos):
    """Extrai nomes dos times da partida e eventos"""
    home_team = None
    away_team = None
    
    try:
        home_data = partida.get('home_team', {})
        if isinstance(home_data, dict):
            home_team = home_data.get('name')
    except:
        pass
    
    try:
        away_data = partida.get('away_team', {})
        if isinstance(away_data, dict):
            away_team = away_data.get('name')
    except:
        pass
    
    # Tenta extrair dos eventos se nao encontrou
    times_encontrados = set()
    for evento in eventos:
        try:
            team_info = evento.get('team', {})
            if isinstance(team_info, dict):
                team_name = team_info.get('name', '')
                if team_name:
                    times_encontrados.add(team_name)
                    if len(times_encontrados) >= 2:
                        break
        except:
            continue
    
    if len(times_encontrados) >= 2:
        times_list = sorted(list(times_encontrados))
        if not home_team:
            home_team = times_list[0]
        if not away_team:
            away_team = times_list[1] if len(times_list) > 1 else times_list[0]
    
    return home_team or 'Time Desconhecido', away_team or 'Time Desconhecido'

def extrai_stats(eventos):
    """Extrai estatisticas dos eventos"""
    stats = {
        'chutes': 0, 'passes': 0, 'faltas': 0, 
        'escanteios': 0, 'cartoes_amarelos': 0, 'cartoes_vermelhos': 0
    }
    
    for evento in eventos:
        try:
            tipo = evento.get('type', {}).get('name', '')
            
            if tipo == 'Shot':
                stats['chutes'] += 1
            elif tipo == 'Pass':
                stats['passes'] += 1
            elif tipo == 'Foul Committed':
                stats['faltas'] += 1
            elif tipo == 'Corner Awarded':
                stats['escanteios'] += 1
            elif tipo == 'Card':
                card_type = evento.get('card', {}).get('name', '')
                if 'Yellow' in card_type:
                    stats['cartoes_amarelos'] += 1
                elif 'Red' in card_type:
                    stats['cartoes_vermelhos'] += 1
        except:
            continue
    
    return stats

def main():
    print("\n" + "=" * 100)
    print("ANALISE AVANCADA DE PREDICOES COM STATSBOMB")
    print("=" * 100 + "\n")
    
    repo_path = "statsbomb_data"
    
    if not Path(repo_path).exists():
        print("[ERRO] statsbomb_data nao encontrado")
        return
    
    config = carregar_modelos()
    if not config:
        return
    
    # Parametros
    competition_id = 12
    season_id = 27
    match_file = Path(repo_path) / "data" / "matches" / str(competition_id) / f"{season_id}.json"
    
    try:
        with open(match_file, 'r', encoding='utf-8') as f:
            partidas = json.load(f)
        
        print(f"Competicao: Brasil Serie A 2015/2016")
        print(f"Total de partidas: {len(partidas)}")
        print(f"Processando: Primeiras 20 partidas\n")
        
        stats_gerais = []
        count = 0
        
        for partida in partidas:
            match_id = partida.get('match_id')
            event_file = Path(repo_path) / "data" / "events" / f"{match_id}.json"
            
            if not event_file.exists():
                continue
            
            # Carrega eventos
            with open(event_file, 'r', encoding='utf-8') as f:
                eventos = json.load(f)
            
            # Extrai nomes
            home_team, away_team = extrai_nomes_times(partida, eventos)
            
            # Extrai estatisticas
            stats = extrai_stats(eventos)
            total_eventos = len(eventos)
            
            # Calcula metricas
            posse_aprox = (stats['passes'] / (stats['passes'] + 5)) * 100 if stats['passes'] > 0 else 50
            
            info = {
                'match_id': match_id,
                'home_team': home_team,
                'away_team': away_team,
                'total_eventos': total_eventos,
                'passes': stats['passes'],
                'chutes': stats['chutes'],
                'faltas': stats['faltas'],
                'escanteios': stats['escanteios'],
                'amarelos': stats['cartoes_amarelos'],
                'vermelhos': stats['cartoes_vermelhos'],
            }
            
            print(f"[{count+1:2d}] {home_team:25s} vs {away_team:25s} | "
                  f"Eventos: {total_eventos:4d} | Passes: {stats['passes']:4d} | "
                  f"Chutes: {stats['chutes']:2d} | Escanteios: {stats['escanteios']:2d}")
            
            stats_gerais.append(info)
            
            count += 1
            if count >= 20:
                break
        
        # Analisa dados
        print("\n" + "=" * 100)
        print("RESUMO ESTATISTICO")
        print("=" * 100 + "\n")
        
        df = pd.DataFrame(stats_gerais)
        
        print("Estatisticas Gerais:")
        print(f"  Total de partidas analisadas: {len(df)}")
        print(f"  Eventos por partida: {df['total_eventos'].mean():.0f} (media)")
        print(f"  Passes por partida: {df['passes'].mean():.0f} (media)")
        print(f"  Chutes por partida: {df['chutes'].mean():.1f} (media)")
        print(f"  Faltas por partida: {df['faltas'].mean():.1f} (media)")
        print(f"  Escanteios por partida: {df['escanteios'].mean():.1f} (media)")
        
        print("\nDistribuicao de Eventos:")
        print(f"  Minimo de chutes: {df['chutes'].min()}")
        print(f"  Maximo de chutes: {df['chutes'].max()}")
        print(f"  Minimo de escanteios: {df['escanteios'].min()}")
        print(f"  Maximo de escanteios: {df['escanteios'].max()}")
        
        print("\nTop 5 Partidas por Chutes:")
        top_chutes = df.nlargest(5, 'chutes')[['home_team', 'away_team', 'chutes', 'escanteios']]
        for idx, row in top_chutes.iterrows():
            print(f"  {row['home_team']:25s} vs {row['away_team']:25s} | "
                  f"{row['chutes']:2d} chutes | {row['escanteios']} escanteios")
        
        # Salva analise
        output_file = 'analises/analise_estatsbomb_20partidas.csv'
        df.to_csv(output_file, index=False)
        print(f"\n[OK] Analise salva em: {output_file}")
        
        # Mostra correlacoes
        print("\nCorrelacoes entre Eventos:")
        corr = df[['passes', 'chutes', 'faltas', 'escanteios']].corr()
        print(corr)
        
    except Exception as e:
        print(f"[ERRO] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
