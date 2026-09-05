"""
Predicao Completa - Todas as 380 Partidas do Brasil 2015/2016
Processa dataset inteiro com barra de progresso
"""

import json
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
import os
import sys

os.environ['PYTHONIOENCODING'] = 'utf-8'

class PreditorCompleto:
    """Preditor para 380 partidas com progresso"""
    
    def __init__(self, caminho_modelos='modelos/modelos_futebol.pkl'):
        """Inicializa com modelos treinados"""
        self.config_modelo = None
        self.carrega_modelos(caminho_modelos)
    
    def carrega_modelos(self, caminho):
        """Carrega configuracao e modelos"""
        try:
            with open(caminho, 'rb') as f:
                self.config_modelo = pickle.load(f)
            print(f"[OK] Modelos carregados com sucesso")
        except Exception as e:
            print(f"[ERRO] Falha ao carregar modelos: {e}")
            self.config_modelo = None
    
    def extrai_stats(self, eventos):
        """Extrai estatisticas dos eventos"""
        stats = {
            'home_chutes': 0, 'away_chutes': 0,
            'home_passes': 0, 'away_passes': 0,
            'home_faltas': 0, 'away_faltas': 0,
            'home_escanteios': 0, 'away_escanteios': 0,
            'home_amarelos': 0, 'away_amarelos': 0,
            'home_vermelhos': 0, 'away_vermelhos': 0,
            'total_passes': 0
        }
        
        for evento in eventos:
            try:
                tipo = evento.get('type', {}).get('name', '')
                team = evento.get('team', {}).get('name', '')
                is_home = True  # Assume home por defaut
                
                if tipo == 'Shot':
                    if is_home:
                        stats['home_chutes'] += 1
                    else:
                        stats['away_chutes'] += 1
                
                elif tipo == 'Pass':
                    stats['total_passes'] += 1
                    if is_home:
                        stats['home_passes'] += 1
                    else:
                        stats['away_passes'] += 1
                
                elif tipo == 'Foul Committed':
                    if is_home:
                        stats['home_faltas'] += 1
                    else:
                        stats['away_faltas'] += 1
                
                elif tipo == 'Corner Awarded':
                    if is_home:
                        stats['home_escanteios'] += 1
                    else:
                        stats['away_escanteios'] += 1
                
                elif tipo == 'Card':
                    card_type = evento.get('card', {}).get('name', '')
                    if 'Yellow' in card_type:
                        if is_home:
                            stats['home_amarelos'] += 1
                        else:
                            stats['away_amarelos'] += 1
                    elif 'Red' in card_type:
                        if is_home:
                            stats['home_vermelhos'] += 1
                        else:
                            stats['away_vermelhos'] += 1
            except:
                continue
        
        home_posse = (stats['home_passes'] / stats['total_passes'] * 100) if stats['total_passes'] > 0 else 50
        
        return {
            'home_chutes': stats['home_chutes'],
            'away_chutes': stats['away_chutes'],
            'home_posse': round(home_posse, 1),
            'away_posse': round(100 - home_posse, 1),
            'home_faltas': stats['home_faltas'],
            'away_faltas': stats['away_faltas'],
            'home_escanteios': stats['home_escanteios'],
            'away_escanteios': stats['away_escanteios'],
            'home_amarelos': stats['home_amarelos'],
            'away_amarelos': stats['away_amarelos'],
            'home_vermelhos': stats['home_vermelhos'],
            'away_vermelhos': stats['away_vermelhos'],
        }
    
    def extrai_times(self, partida, eventos):
        """Extrai nomes dos times"""
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
        
        # Fallback
        if not home_team or not away_team:
            times_encontrados = set()
            for evento in eventos[:50]:
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
                    away_team = times_list[1]
        
        return home_team or 'Unknown', away_team or 'Unknown'
    
    def cria_features(self, stats):
        """Cria feature vector"""
        medias = self.config_modelo.get('medias_globais', {})
        
        features = {
            'elo_mandante': 1600,
            'elo_visitante': 1600,
            'elo_diff': 0,
            'mandante_chutes_media': stats.get('home_chutes', 12),
            'visitante_chutes_media': stats.get('away_chutes', 12),
            'mandante_chutes_gol_media': max(1, stats.get('home_chutes', 12) // 3),
            'visitante_chutes_gol_media': max(1, stats.get('away_chutes', 12) // 3),
            'mandante_posse_media': stats.get('home_posse', 50),
            'visitante_posse_media': stats.get('away_posse', 50),
            'mandante_faltas_media': stats.get('home_faltas', 12),
            'visitante_faltas_media': stats.get('away_faltas', 12),
            'mandante_escanteios_media': stats.get('home_escanteios', 5),
            'visitante_escanteios_media': stats.get('away_escanteios', 5),
            'mandante_amarelos_media': stats.get('home_amarelos', 1.5),
            'visitante_amarelos_media': stats.get('away_amarelos', 1.5),
            'mandante_vermelhos_media': stats.get('home_vermelhos', 0.1),
            'visitante_vermelhos_media': stats.get('away_vermelhos', 0.1),
            'mandante_gols_marcados_media': medias.get('mandante_gols_marcados', 1.5),
            'mandante_gols_sofridos_media': medias.get('mandante_gols_sofridos', 1.2),
            'visitante_gols_marcados_media': medias.get('visitante_gols_marcados', 1.4),
            'visitante_gols_sofridos_media': medias.get('visitante_gols_sofridos', 1.4),
            'mandante_forma_pontos': 6,
            'visitante_forma_pontos': 6,
        }
        
        return features
    
    def prever(self, features_dict):
        """Faz predicao"""
        if not self.config_modelo:
            return None
        
        try:
            feature_cols = self.config_modelo.get('feature_cols', [])
            models = self.config_modelo.get('models', {})
            scaler = self.config_modelo.get('scaler')
            
            X = pd.DataFrame([features_dict])
            X = X[feature_cols]
            
            if scaler:
                try:
                    X = pd.DataFrame(scaler.transform(X), columns=feature_cols)
                except:
                    pass
            
            resultado = {}
            
            # Resultado
            if 'resultado' in models:
                try:
                    pred = models['resultado'].predict(X)
                    pred_class = pred[0] if isinstance(pred, np.ndarray) else pred
                    
                    if isinstance(pred_class, str):
                        resultado['resultado'] = pred_class
                    else:
                        classe_map = {0: 'Empate', 1: 'Mandante', 2: 'Visitante'}
                        resultado['resultado'] = classe_map.get(int(pred_class), 'Unknown')
                    
                    proba = models['resultado'].predict_proba(X)[0]
                    resultado['confianca'] = float(max(proba))
                except:
                    resultado['resultado'] = 'Erro'
                    resultado['confianca'] = 0.0
            
            # Gols
            if 'gols_mandante' in models:
                try:
                    gols = models['gols_mandante'].predict(X)[0]
                    resultado['gols_mandante'] = max(0, int(round(float(gols))))
                except:
                    resultado['gols_mandante'] = 1
            
            if 'gols_visitante' in models:
                try:
                    gols = models['gols_visitante'].predict(X)[0]
                    resultado['gols_visitante'] = max(0, int(round(float(gols))))
                except:
                    resultado['gols_visitante'] = 1
            
            # Escanteios e faltas
            if 'escanteios' in models:
                try:
                    resultado['escanteios'] = max(0, int(round(float(models['escanteios'].predict(X)[0]))))
                except:
                    resultado['escanteios'] = 6
            
            if 'faltas' in models:
                try:
                    resultado['faltas'] = max(0, int(round(float(models['faltas'].predict(X)[0]))))
                except:
                    resultado['faltas'] = 24
            
            return resultado
        
        except Exception as e:
            return None

def mostra_progresso(atual, total):
    """Barra de progresso"""
    percent = (atual / total) * 100
    barra = int(percent / 2)
    sys.stdout.write(f"\r[{'=' * barra}{' ' * (50 - barra)}] {percent:.1f}% ({atual}/{total})")
    sys.stdout.flush()

def main():
    print("\n" + "=" * 100)
    print("PREDICOES PARA TODAS AS 380 PARTIDAS - BRASIL 2015/2016")
    print("=" * 100 + "\n")
    
    repo_path = "statsbomb_data"
    
    if not Path(repo_path).exists():
        print("[ERRO] statsbomb_data nao encontrado")
        return
    
    print("Inicializando preditor...")
    preditor = PreditorCompleto()
    
    if not preditor.config_modelo:
        return
    
    competition_id = 12
    season_id = 27
    match_file = Path(repo_path) / "data" / "matches" / str(competition_id) / f"{season_id}.json"
    
    try:
        with open(match_file, 'r', encoding='utf-8') as f:
            partidas = json.load(f)
        
        print(f"Total de partidas: {len(partidas)}")
        print(f"Processando...\n")
        
        predicoes = []
        erros = []
        count = 0
        
        for partida in partidas:
            match_id = partida.get('match_id')
            event_file = Path(repo_path) / "data" / "events" / f"{match_id}.json"
            
            if not event_file.exists():
                continue
            
            try:
                with open(event_file, 'r', encoding='utf-8') as f:
                    eventos = json.load(f)
                
                home_team, away_team = preditor.extrai_times(partida, eventos)
                stats = preditor.extrai_stats(eventos)
                features = preditor.cria_features(stats)
                pred = preditor.prever(features)
                
                if pred:
                    resultado = {
                        'match_id': match_id,
                        'home_team': home_team,
                        'away_team': away_team,
                        'resultado': pred.get('resultado', 'N/A'),
                        'confianca': pred.get('confianca', 0),
                        'gols_mandante': pred.get('gols_mandante', 0),
                        'gols_visitante': pred.get('gols_visitante', 0),
                        'escanteios': pred.get('escanteios', 0),
                        'faltas': pred.get('faltas', 0),
                    }
                    predicoes.append(resultado)
                
                count += 1
                mostra_progresso(count, len(partidas))
            
            except Exception as e:
                erros.append((match_id, str(e)))
                count += 1
                mostra_progresso(count, len(partidas))
        
        print("\n\n" + "=" * 100)
        print("PROCESSAMENTO COMPLETO")
        print("=" * 100 + "\n")
        
        print(f"Partidas processadas: {len(predicoes)}")
        print(f"Erros encontrados: {len(erros)}")
        
        if predicoes:
            df = pd.DataFrame(predicoes)
            
            # Salva CSV
            output_file = 'analises/predicoes_completas_380.csv'
            df.to_csv(output_file, index=False)
            print(f"\n[OK] Predicoes salvas em: {output_file}")
            
            # Estatisticas
            print("\n" + "=" * 100)
            print("RESUMO ESTATISTICO")
            print("=" * 100 + "\n")
            
            print(f"Total de predicoes: {len(df)}")
            print(f"\nDistribuicao de Resultados:")
            print(df['resultado'].value_counts().to_string())
            
            print(f"\n\nConfianca Media: {df['confianca'].mean():.1%}")
            print(f"Confianca Min/Max: {df['confianca'].min():.1%} / {df['confianca'].max():.1%}")
            
            print(f"\nGols Mandante - Media: {df['gols_mandante'].mean():.2f}")
            print(f"Gols Visitante - Media: {df['gols_visitante'].mean():.2f}")
            
            print(f"\nEscanteios - Media: {df['escanteios'].mean():.1f}")
            print(f"Faltas - Media: {df['faltas'].mean():.1f}")
            
            # Top partidas por confianca
            print("\n\nTop 10 Predicoes com Maior Confianca:")
            top = df.nlargest(10, 'confianca')[['home_team', 'away_team', 'resultado', 'confianca']]
            for idx, row in top.iterrows():
                print(f"  {row['home_team']:25s} vs {row['away_team']:25s} | "
                      f"{row['resultado']:12s} ({row['confianca']:.1%})")
            
            # Salva estatisticas
            stats_file = 'analises/resumo_predicoes_380.txt'
            with open(stats_file, 'w', encoding='utf-8') as f:
                f.write("RESUMO DE PREDICOES - 380 PARTIDAS\n")
                f.write("=" * 80 + "\n\n")
                f.write(f"Total de predicoes: {len(df)}\n")
                f.write(f"Confianca media: {df['confianca'].mean():.1%}\n")
                f.write(f"Gols mandante media: {df['gols_mandante'].mean():.2f}\n")
                f.write(f"Gols visitante media: {df['gols_visitante'].mean():.2f}\n")
                f.write(f"\nDistribuicao de Resultados:\n")
                f.write(df['resultado'].value_counts().to_string())
            
            print(f"\n[OK] Resumo salvo em: {stats_file}")
        
        print("\n" + "=" * 100)
    
    except Exception as e:
        print(f"[ERRO] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
