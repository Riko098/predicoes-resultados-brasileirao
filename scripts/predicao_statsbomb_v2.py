"""
Predicao com Dados StatsBomb - Versao Melhorada
Usa estrutura correta do modelo com ELO e medias
"""

import json
import pandas as pd
import pickle
import numpy as np
from pathlib import Path
import os

os.environ['PYTHONIOENCODING'] = 'utf-8'

class PreditorStatsBombAvancado:
    """Preditor avancado integrando StatsBomb com modelo treinado"""
    
    def __init__(self, caminho_modelos='modelos/modelos_futebol.pkl'):
        """Inicializa com modelos treinados"""
        self.config_modelo = None
        self.carrega_modelos(caminho_modelos)
    
    def carrega_modelos(self, caminho):
        """Carrega configuracao e modelos"""
        try:
            with open(caminho, 'rb') as f:
                self.config_modelo = pickle.load(f)
            print(f"[OK] Modelos carregados")
            print(f"     {len(self.config_modelo.get('models', {}))} modelos disponiveis")
        except Exception as e:
            print(f"[ERRO] {e}")
            self.config_modelo = None
    
    def extrai_stats_estatsbomb(self, eventos, home_team, away_team):
        """Extrai estatisticas do StatsBomb"""
        
        stats = {
            'home_chutes': 0, 'away_chutes': 0,
            'home_chutes_gol': 0, 'away_chutes_gol': 0,
            'home_passes': 0, 'away_passes': 0,
            'home_faltas': 0, 'away_faltas': 0,
            'home_escanteios': 0, 'away_escanteios': 0,
            'total_passes': 0
        }
        
        for evento in eventos:
            try:
                tipo = evento.get('type', {}).get('name', '')
                team = evento.get('team', {}).get('name', '')
                
                # Tenta identificar lado (home/away)
                is_home = (team == home_team or 'home' in str(evento).lower())
                
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
            
            except:
                continue
        
        # Calcula posse
        home_posse = (stats['home_passes'] / stats['total_passes'] * 100) if stats['total_passes'] > 0 else 0
        
        return {
            'home_team': home_team,
            'away_team': away_team,
            'home_chutes': stats['home_chutes'],
            'away_chutes': stats['away_chutes'],
            'home_posse': round(home_posse, 1),
            'away_posse': round(100 - home_posse, 1),
            'home_faltas': stats['home_faltas'],
            'away_faltas': stats['away_faltas'],
            'home_escanteios': stats['home_escanteios'],
            'away_escanteios': stats['away_escanteios'],
        }
    
    def cria_features_com_defaults(self, home_team, away_team, stats_estatsbomb):
        """Cria feature vector com valores padrao e dados do StatsBomb"""
        
        if not self.config_modelo:
            return None
        
        # Valores padrao
        elo_padrao = 1600
        
        # Medias globais
        medias = self.config_modelo.get('medias_globais', {})
        
        # Valores padrao para features
        features = {
            'elo_mandante': elo_padrao,
            'elo_visitante': elo_padrao,
            'elo_diff': 0,
            'mandante_chutes_media': stats_estatsbomb.get('home_chutes', 12),
            'visitante_chutes_media': stats_estatsbomb.get('away_chutes', 12),
            'mandante_chutes_gol_media': max(1, stats_estatsbomb.get('home_chutes', 12) // 3),
            'visitante_chutes_gol_media': max(1, stats_estatsbomb.get('away_chutes', 12) // 3),
            'mandante_posse_media': stats_estatsbomb.get('home_posse', 50),
            'visitante_posse_media': stats_estatsbomb.get('away_posse', 50),
            'mandante_faltas_media': stats_estatsbomb.get('home_faltas', 12),
            'visitante_faltas_media': stats_estatsbomb.get('away_faltas', 12),
            'mandante_escanteios_media': stats_estatsbomb.get('home_escanteios', 5),
            'visitante_escanteios_media': stats_estatsbomb.get('away_escanteios', 5),
            'mandante_amarelos_media': 1.5,
            'visitante_amarelos_media': 1.5,
            'mandante_vermelhos_media': 0.1,
            'visitante_vermelhos_media': 0.1,
            'mandante_gols_marcados_media': medias.get('mandante_gols_marcados', 1.5),
            'mandante_gols_sofridos_media': medias.get('mandante_gols_sofridos', 1.2),
            'visitante_gols_marcados_media': medias.get('visitante_gols_marcados', 1.4),
            'visitante_gols_sofridos_media': medias.get('visitante_gols_sofridos', 1.4),
            'mandante_forma_pontos': 6,
            'visitante_forma_pontos': 6,
        }
        
        return features
    
    def prever(self, home_team, away_team, features_dict):
        """Faz predicao completa"""
        
        if not self.config_modelo:
            return None
        
        try:
            # Obtem colunas esperadas
            feature_cols = self.config_modelo.get('feature_cols', [])
            models = self.config_modelo.get('models', {})
            scaler = self.config_modelo.get('scaler')
            
            # Cria DataFrame
            X = pd.DataFrame([features_dict])
            X = X[feature_cols]  # Garante ordem correta
            
            # Normaliza se houver scaler
            if scaler:
                try:
                    X = pd.DataFrame(
                        scaler.transform(X),
                        columns=feature_cols
                    )
                except:
                    pass
            
            resultado = {
                'home_team': home_team,
                'away_team': away_team,
            }
            
            # Resultado final
            if 'resultado' in models:
                try:
                    pred = models['resultado'].predict(X)
                    # Pode ser array ou valor direto
                    if isinstance(pred, np.ndarray):
                        pred_class = pred[0]
                    else:
                        pred_class = pred
                    
                    # Trata como número ou string
                    if isinstance(pred_class, str):
                        resultado['resultado'] = pred_class
                    else:
                        classe_map = {0: 'Empate', 1: 'Mandante', 2: 'Visitante'}
                        resultado['resultado'] = classe_map.get(int(pred_class), 'Unknown')
                    
                    proba = models['resultado'].predict_proba(X)[0]
                    resultado['confianca'] = float(max(proba))
                except Exception as e:
                    resultado['resultado'] = 'Erro'
                    resultado['confianca'] = 0.0
            
            # Gols
            if 'gols_mandante' in models:
                try:
                    gols_home = models['gols_mandante'].predict(X)[0]
                    resultado['gols_mandante'] = max(0, int(round(float(gols_home))))
                except:
                    resultado['gols_mandante'] = 1
            
            if 'gols_visitante' in models:
                try:
                    gols_away = models['gols_visitante'].predict(X)[0]
                    resultado['gols_visitante'] = max(0, int(round(float(gols_away))))
                except:
                    resultado['gols_visitante'] = 1
            
            # Outras predicoes
            if 'escanteios' in models:
                try:
                    escanteios = models['escanteios'].predict(X)[0]
                    resultado['escanteios'] = max(0, int(round(float(escanteios))))
                except:
                    resultado['escanteios'] = 6
            
            if 'faltas' in models:
                try:
                    faltas = models['faltas'].predict(X)[0]
                    resultado['faltas'] = max(0, int(round(float(faltas))))
                except:
                    resultado['faltas'] = 24
            
            return resultado
        
        except Exception as e:
            print(f"[ERRO] Ao prever: {e}")
            return None

def main():
    print("\n" + "=" * 80)
    print("PREDICAO COM DADOS STATSBOMB - VERSAO AVANCADA")
    print("=" * 80 + "\n")
    
    repo_path = "statsbomb_data"
    
    if not Path(repo_path).exists():
        print("[ERRO] statsbomb_data nao encontrado")
        print("Execute: python integracao/clonar_statsbomb.py")
        return
    
    # Inicializa preditor
    print("Carregando modelos treinados...")
    preditor = PreditorStatsBombAvancado()
    
    if not preditor.config_modelo:
        return
    
    # Parametros
    competition_id = 12
    season_id = 27
    
    # Carrega partidas
    match_file = Path(repo_path) / "data" / "matches" / str(competition_id) / f"{season_id}.json"
    
    try:
        with open(match_file, 'r', encoding='utf-8') as f:
            partidas = json.load(f)
        
        print(f"[OK] {len(partidas)} partidas disponiveis")
        print("Processando primeiras 5 partidas com eventos...\n")
        
        predicoes = []
        count = 0
        
        for partida in partidas:
            match_id = partida.get('match_id')
            event_file = Path(repo_path) / "data" / "events" / f"{match_id}.json"
            
            if not event_file.exists():
                continue
            
            # Carrega eventos
            with open(event_file, 'r', encoding='utf-8') as f:
                eventos = json.load(f)
            
            # Extrai info da partida com fallback seguro
            try:
                home_team = partida.get('home_team', {})
                if isinstance(home_team, dict):
                    home_team = home_team.get('name', f'Time {count}')
                else:
                    home_team = str(home_team)
            except:
                home_team = f'Time {count}'
            
            try:
                away_team = partida.get('away_team', {})
                if isinstance(away_team, dict):
                    away_team = away_team.get('name', f'Time {count+1}')
                else:
                    away_team = str(away_team)
            except:
                away_team = f'Time {count+1}'
            
            # Extrai nomes dos times dos eventos se possivel
            for evento in eventos[:20]:  # Verifica primeiros eventos
                try:
                    team_info = evento.get('team', {})
                    if isinstance(team_info, dict):
                        team_name = team_info.get('name', '')
                        if not home_team or 'Time' in home_team:
                            # Tenta usar time do primeiro evento
                            home_team = team_name if team_name else f'Time {count}'
                        break
                except:
                    continue
            
            print(f"[{count+1}] {home_team:30s} vs {away_team:30s}", end='')
            
            # Extrai stats do StatsBomb
            stats = preditor.extrai_stats_estatsbomb(eventos, home_team, away_team)
            
            # Cria features
            features = preditor.cria_features_com_defaults(home_team, away_team, stats)
            
            # Faz predicao
            pred = preditor.prever(home_team, away_team, features)
            
            if pred:
                print(f" | {pred.get('resultado', 'N/A'):12s} {pred.get('gols_mandante', 0)}x{pred.get('gols_visitante', 0)} "
                      f"({pred.get('confianca', 0):.1%})")
                
                predicoes.append(pred)
            else:
                print(" [ERRO]")
            
            count += 1
            if count >= 5:
                break
        
        # Salva resultados
        if predicoes:
            df_preds = pd.DataFrame(predicoes)
            output_file = 'analises/predicoes_statsbomb.csv'
            df_preds.to_csv(output_file, index=False)
            print(f"\n[OK] {len(predicoes)} predicoes salvas em: {output_file}")
            print("\nResumo:")
            print(df_preds[['home_team', 'away_team', 'resultado', 'gols_mandante', 'gols_visitante', 'confianca']].to_string())
    
    except Exception as e:
        print(f"[ERRO] {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
