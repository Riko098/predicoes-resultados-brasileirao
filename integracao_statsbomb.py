"""
Integração com StatsBomb Open Data para enriquecer o projeto de predição
Documentação: https://github.com/hudl/open-data
"""

import requests
import json
import pandas as pd
import os
from pathlib import Path
import subprocess

class StatsBombIntegration:
    """Classe para gerenciar dados do StatsBomb Open Data"""
    
    def __init__(self, data_dir="statsbomb_data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.base_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
        
    def clonar_repositorio(self):
        """Clona o repositório StatsBomb localmente (opcional)"""
        print("Clonando StatsBomb Open Data...")
        if not (self.data_dir / ".git").exists():
            subprocess.run([
                "git", "clone", 
                "https://github.com/statsbomb/open-data.git",
                str(self.data_dir)
            ], capture_output=True)
        print("✓ Repositório clonado em:", self.data_dir)
    
    def carregar_competicoes(self):
        """Carrega todas as competições disponíveis"""
        print("\nCarregando competições...")
        url = f"{self.base_url}/competitions.json"
        response = requests.get(url)
        competicoes = response.json()
        
        df = pd.DataFrame(competicoes)
        print(f"✓ {len(df)} competições encontradas")
        print("\nCompetições disponíveis:")
        print(df[['competition_name', 'season_name']].to_string())
        return df
    
    def carregar_partidas_por_competicao(self, competition_id, season_id):
        """Carrega todas as partidas de uma competição/temporada"""
        print(f"\nCarregando partidas da competição {competition_id}, temporada {season_id}...")
        url = f"{self.base_url}/matches/{competition_id}/{season_id}.json"
        
        try:
            response = requests.get(url)
            partidas = response.json()
            df = pd.DataFrame(partidas)
            print(f"✓ {len(df)} partidas carregadas")
            return df
        except Exception as e:
            print(f"✗ Erro: {e}")
            return None
    
    def carregar_eventos_partida(self, match_id):
        """Carrega eventos detalhados de uma partida"""
        print(f"\nCarregando eventos da partida {match_id}...")
        url = f"{self.base_url}/events/{match_id}.json"
        
        try:
            response = requests.get(url)
            eventos = response.json()
            print(f"✓ {len(eventos)} eventos encontrados")
            return eventos
        except Exception as e:
            print(f"✗ Erro: {e}")
            return None
    
    def extrair_estatisticas_partida(self, eventos):
        """Extrai estatísticas agregadas de uma partida"""
        if not eventos:
            return None
        
        stats = {
            'total_passes': 0,
            'total_shots': 0,
            'total_tackles': 0,
            'total_fouls': 0,
            'total_corners': 0,
            'total_crosses': 0,
            'possessions': {},
            'passes_by_team': {},
            'shots_by_team': {}
        }
        
        for evento in eventos:
            tipo = evento.get('type', {}).get('name', '')
            time = evento.get('team', {}).get('name', 'Unknown')
            
            if tipo == 'Pass':
                stats['total_passes'] += 1
                stats['passes_by_team'][time] = stats['passes_by_team'].get(time, 0) + 1
            elif tipo == 'Shot':
                stats['total_shots'] += 1
                stats['shots_by_team'][time] = stats['shots_by_team'].get(time, 0) + 1
            elif tipo == 'Tackle':
                stats['total_tackles'] += 1
            elif tipo == 'Foul Committed':
                stats['total_fouls'] += 1
            elif tipo == 'Corner Awarded':
                stats['total_corners'] += 1
        
        return stats
    
    def criar_dataset_enriquecido(self, df_partidas, extrair_eventos=False):
        """
        Cria dataset enriquecido com estatísticas do StatsBomb
        
        Args:
            df_partidas: DataFrame com partidas
            extrair_eventos: Se True, extrai eventos detalhados (mais lento)
        """
        print("\nCriando dataset enriquecido...")
        
        dados_enriquecidos = []
        
        for idx, partida in df_partidas.iterrows():
            match_id = partida['match_id']
            
            linha = {
                'match_id': match_id,
                'date': partida.get('match_date'),
                'home_team': partida.get('home_team', {}).get('name'),
                'away_team': partida.get('away_team', {}).get('name'),
                'home_score': partida.get('home_score'),
                'away_score': partida.get('away_score'),
                'competition': partida.get('competition', {}).get('name'),
                'season': partida.get('season', {}).get('name'),
                'status': partida.get('status')
            }
            
            # Extrai estatísticas de eventos se disponível
            if extrair_eventos and partida.get('status') == 'complete':
                eventos = self.carregar_eventos_partida(match_id)
                stats = self.extrair_estatisticas_partida(eventos)
                
                if stats:
                    for time, passes in stats['passes_by_team'].items():
                        linha[f'{time}_passes'] = passes
                    for time, shots in stats['shots_by_team'].items():
                        linha[f'{time}_shots'] = shots
            
            dados_enriquecidos.append(linha)
        
        df_enriquecido = pd.DataFrame(dados_enriquecidos)
        print(f"✓ Dataset criado com {len(df_enriquecido)} partidas")
        return df_enriquecido
    
    def integrar_com_predictor(self, df_enriquecido, df_original):
        """
        Integra dados StatsBomb com seu dataset original de predição
        """
        print("\nIntegrando com dataset de predição...")
        
        # Merge dos dados
        df_merged = df_original.merge(
            df_enriquecido[['match_id', 'home_score', 'away_score']],
            on=['match_id'],
            how='left'
        )
        
        print(f"✓ {len(df_merged)} registros após integração")
        return df_merged


def exemplo_uso():
    """Exemplo de uso da integração"""
    print("=" * 60)
    print("INTEGRAÇÃO STATSBOMB OPEN DATA")
    print("=" * 60)
    
    # Inicializa integração
    sb = StatsBombIntegration()
    
    # 1. Carrega competições disponíveis
    competicoes = sb.carregar_competicoes()
    
    # 2. Filtra competições brasileiras (opcional)
    # Para encontrar: busque 'Série A', 'Campeonato Brasileiro', etc
    
    # 3. Exemplo: carregar partidas de uma competição
    # competition_id, season_id podem ser encontrados em competicoes.json
    # df_partidas = sb.carregar_partidas_por_competicao(competition_id=24, season_id=1)
    
    # 4. Criar dataset enriquecido
    # df_enriquecido = sb.criar_dataset_enriquecido(df_partidas, extrair_eventos=False)
    
    # 5. Salvar para análise
    # df_enriquecido.to_csv('dados_statsbomb_enriquecidos.csv', index=False)
    
    print("\n" + "=" * 60)
    print("PRÓXIMAS ETAPAS:")
    print("=" * 60)
    print("1. Ajuste competition_id e season_id conforme necessário")
    print("2. Mescle com seus dados de treinamento existentes")
    print("3. Re-treine o modelo com as novas features")
    print("4. Valide o desempenho com os dados enriquecidos")


if __name__ == "__main__":
    exemplo_uso()
