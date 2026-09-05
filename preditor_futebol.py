"""
🏆 Sistema de Predição de Resultados de Futebol - Campeonato Brasileiro
Uso: python preditor_futebol.py

Este script treina modelos de machine learning para prever:
- Vencedor da partida
- Quantidade de gols
- Escanteios e faltas

IMPORTANTE (v2): As features usadas são construídas apenas com dados
ANTERIORES a cada partida (médias móveis históricas + rating Elo).
Isso evita "vazamento de dados" (usar estatísticas do próprio jogo para
prever o resultado dele mesmo) e garante que as predições de jogos
futuros usem exatamente o mesmo tipo de informação vista no treino.
"""

import pandas as pd
import numpy as np
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor,
    GradientBoostingRegressor, VotingRegressor
)
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error
import pickle

# Constantes do rating Elo
ELO_INICIAL = 1500
ELO_K = 20
ELO_VANTAGEM_CASA = 100

# Janela de jogos recentes usada para calcular a "forma atual" de um time.
# Usar toda a carreira do time (2003-hoje) dilui demais a forma atual, já que
# elencos mudam completamente ao longo dos anos. Uma janela recente captura
# melhor o nível atual do time.
ROLLING_WINDOW = 10

# Estatísticas brutas por partida usadas para construir o histórico
STAT_COLS = ['chutes', 'chutes_gol', 'posse', 'faltas', 'escanteios', 'amarelos', 'vermelhos',
             'gols_marcados', 'gols_sofridos']


class PreditorFutebol:
    """Classe para predição de resultados de futebol (features 100% pré-jogo)"""

    def __init__(self, data_dir='.'):
        self.data_dir = data_dir
        self.models = {}
        self.scaler = StandardScaler()
        self.times = []
        self.estado_atual = {}   # time -> médias históricas mais recentes
        self.elo_final = {}      # time -> rating Elo mais recente
        self.medias_globais = {}  # fallback para times sem histórico suficiente

        self.feature_cols = [
            'elo_mandante', 'elo_visitante', 'elo_diff',
            'mandante_chutes_media', 'visitante_chutes_media',
            'mandante_chutes_gol_media', 'visitante_chutes_gol_media',
            'mandante_posse_media', 'visitante_posse_media',
            'mandante_faltas_media', 'visitante_faltas_media',
            'mandante_escanteios_media', 'visitante_escanteios_media',
            'mandante_amarelos_media', 'visitante_amarelos_media',
            'mandante_vermelhos_media', 'visitante_vermelhos_media',
            'mandante_gols_marcados_media', 'mandante_gols_sofridos_media',
            'visitante_gols_marcados_media', 'visitante_gols_sofridos_media',
            'mandante_forma_pontos', 'visitante_forma_pontos',
        ]

    # ------------------------------------------------------------------
    # Carregamento e preparação de dados
    # ------------------------------------------------------------------
    def carregar_dados(self):
        """Carrega e processa os arquivos CSV"""
        print("📥 Carregando dados...")

        df_matches = pd.read_csv(f'{self.data_dir}/campeonato-brasileiro-full.csv')
        df_stats = pd.read_csv(f'{self.data_dir}/campeonato-brasileiro-estatisticas-full.csv')
        df_goals = pd.read_csv(f'{self.data_dir}/campeonato-brasileiro-gols.csv')
        df_cards = pd.read_csv(f'{self.data_dir}/campeonato-brasileiro-cartoes.csv')

        print(f"✅ Dados carregados: {len(df_matches)} partidas")
        return df_matches, df_stats, df_goals, df_cards

    def preparar_features(self, df_matches, df_stats):
        """Constrói as features históricas (pré-jogo) e o rating Elo."""
        print("🔧 Preparando features históricas (sem vazamento de dados)...")

        df_matches = df_matches.copy()
        df_matches['data'] = pd.to_datetime(df_matches['data'], format='%d/%m/%Y', errors='coerce')
        df_matches = df_matches.dropna(subset=['data', 'vencedor', 'mandante_Placar', 'visitante_Placar'])
        df_matches = df_matches.sort_values(['data', 'ID']).reset_index(drop=True)

        # Normalizar estatísticas brutas da partida
        stats = df_stats.copy()
        stats['posse_de_bola'] = pd.to_numeric(
            stats['posse_de_bola'].astype(str).str.replace('%', ''), errors='coerce'
        )
        for c in ['chutes', 'chutes_no_alvo', 'faltas', 'cartao_amarelo', 'cartao_vermelho', 'escanteios']:
            stats[c] = pd.to_numeric(stats[c], errors='coerce')

        # BUG DE DADOS: partidas sem estatísticas coletadas (comuns em
        # temporadas antigas, ~2003-2012, e em alguns jogos pontuais mais
        # recentes) aparecem no CSV com 'posse_de_bola' em branco MAS com
        # chutes/faltas/escanteios/cartões preenchidos como "0" literal —
        # um placeholder de "sem dado", não um zero real de jogo. Sem essa
        # correção, times com jogos assim na janela recente (ex.: recém-
        # promovidos, jogos com falha de coleta) tinham médias zeradas.
        # Tratamos essas linhas (posse ausente) como totalmente ausentes,
        # deixando o fillna com a média global do dataset resolver depois.
        stats_ausentes = stats['posse_de_bola'].isna()
        for c in ['chutes', 'chutes_no_alvo', 'faltas', 'cartao_amarelo', 'cartao_vermelho', 'escanteios']:
            stats.loc[stats_ausentes, c] = np.nan

        rename_map = {
            'chutes': 'chutes', 'chutes_no_alvo': 'chutes_gol', 'posse_de_bola': 'posse',
            'faltas': 'faltas', 'cartao_amarelo': 'amarelos', 'cartao_vermelho': 'vermelhos',
            'escanteios': 'escanteios'
        }
        raw_cols = list(rename_map.keys())

        home_stats = stats.rename(columns={c: f'h_{rename_map[c]}' for c in raw_cols})
        away_stats = stats.rename(columns={c: f'a_{rename_map[c]}' for c in raw_cols})
        h_cols = [f'h_{rename_map[c]}' for c in raw_cols]
        a_cols = [f'a_{rename_map[c]}' for c in raw_cols]

        df_matches = df_matches.merge(
            home_stats[['partida_id', 'clube'] + h_cols],
            left_on=['ID', 'mandante'], right_on=['partida_id', 'clube'], how='left'
        ).drop(columns=['partida_id', 'clube'])

        df_matches = df_matches.merge(
            away_stats[['partida_id', 'clube'] + a_cols],
            left_on=['ID', 'visitante'], right_on=['partida_id', 'clube'], how='left'
        ).drop(columns=['partida_id', 'clube'])

        # Preencher estatísticas de jogo ausentes com a média global da coluna
        for c in h_cols + a_cols:
            df_matches[c] = df_matches[c].fillna(df_matches[c].mean())

        # Alvos de regressão (valores REAIS do próprio jogo, usados só como target)
        df_matches['escanteios_total'] = df_matches['h_escanteios'] + df_matches['a_escanteios']
        df_matches['faltas_total'] = df_matches['h_faltas'] + df_matches['a_faltas']
        df_matches['amarelos_total'] = df_matches['h_amarelos'] + df_matches['a_amarelos']
        df_matches['vermelhos_total'] = df_matches['h_vermelhos'] + df_matches['a_vermelhos']

        # Resultado (classe alvo)
        def encode_result(row):
            if row['vencedor'] == '-':
                return 'Empate'
            elif row['vencedor'] == row['mandante']:
                return 'Mandante'
            else:
                return 'Visitante'
        df_matches['Resultado'] = df_matches.apply(encode_result, axis=1)

        # --------------------------------------------------------------
        # Construir tabela "longa" (uma linha por time por partida)
        # para calcular médias móveis causais (sem olhar o futuro)
        # --------------------------------------------------------------
        home_long = pd.DataFrame({
            'ID': df_matches['ID'], 'data': df_matches['data'], 'time': df_matches['mandante'],
            'chutes': df_matches['h_chutes'], 'chutes_gol': df_matches['h_chutes_gol'],
            'posse': df_matches['h_posse'], 'faltas': df_matches['h_faltas'],
            'escanteios': df_matches['h_escanteios'], 'amarelos': df_matches['h_amarelos'],
            'vermelhos': df_matches['h_vermelhos'],
            'gols_marcados': df_matches['mandante_Placar'], 'gols_sofridos': df_matches['visitante_Placar'],
        })
        home_long['pontos'] = np.where(
            df_matches['vencedor'] == df_matches['mandante'], 3,
            np.where(df_matches['vencedor'] == '-', 1, 0)
        )

        away_long = pd.DataFrame({
            'ID': df_matches['ID'], 'data': df_matches['data'], 'time': df_matches['visitante'],
            'chutes': df_matches['a_chutes'], 'chutes_gol': df_matches['a_chutes_gol'],
            'posse': df_matches['a_posse'], 'faltas': df_matches['a_faltas'],
            'escanteios': df_matches['a_escanteios'], 'amarelos': df_matches['a_amarelos'],
            'vermelhos': df_matches['a_vermelhos'],
            'gols_marcados': df_matches['visitante_Placar'], 'gols_sofridos': df_matches['mandante_Placar'],
        })
        away_long['pontos'] = np.where(
            df_matches['vencedor'] == df_matches['visitante'], 3,
            np.where(df_matches['vencedor'] == '-', 1, 0)
        )

        long = pd.concat([home_long, away_long], ignore_index=True)
        long = long.sort_values(['time', 'data', 'ID']).reset_index(drop=True)

        # Médias históricas causais: só usam jogos ANTERIORES (shift(1)),
        # dentro de uma janela recente (ROLLING_WINDOW jogos) para refletir
        # a forma atual do time em vez da carreira inteira
        grp = long.groupby('time')
        for c in STAT_COLS:
            long[f'{c}_media'] = grp[c].transform(
                lambda s: s.shift(1).rolling(ROLLING_WINDOW, min_periods=3).mean()
            )
        long['forma_pontos'] = grp['pontos'].transform(lambda s: s.shift(1).rolling(5, min_periods=1).sum())

        # Fallback para o primeiro jogo de cada time (sem histórico ainda)
        self.medias_globais = {c: float(long[c].mean()) for c in STAT_COLS}
        self.medias_globais['forma_pontos'] = float(long['forma_pontos'].mean())
        for c in STAT_COLS:
            long[f'{c}_media'] = long[f'{c}_media'].fillna(self.medias_globais[c])
        long['forma_pontos'] = long['forma_pontos'].fillna(self.medias_globais['forma_pontos'])

        # --------------------------------------------------------------
        # Rating Elo (sequencial, calculado ANTES de saber o resultado)
        # --------------------------------------------------------------
        elo = {}
        elo_mandante_list, elo_visitante_list = [], []
        for _, row in df_matches.iterrows():
            m, v = row['mandante'], row['visitante']
            elo_m = elo.get(m, ELO_INICIAL)
            elo_v = elo.get(v, ELO_INICIAL)
            elo_mandante_list.append(elo_m)
            elo_visitante_list.append(elo_v)

            esperado_m = 1 / (1 + 10 ** (-((elo_m + ELO_VANTAGEM_CASA) - elo_v) / 400))
            if row['vencedor'] == m:
                score_m = 1.0
            elif row['vencedor'] == '-':
                score_m = 0.5
            else:
                score_m = 0.0

            dif_gols = abs(row['mandante_Placar'] - row['visitante_Placar'])
            multiplicador = 1 + min(dif_gols, 3) * 0.15
            elo[m] = elo_m + ELO_K * multiplicador * (score_m - esperado_m)
            elo[v] = elo_v + ELO_K * multiplicador * ((1 - score_m) - (1 - esperado_m))

        df_matches['elo_mandante'] = elo_mandante_list
        df_matches['elo_visitante'] = elo_visitante_list
        df_matches['elo_diff'] = df_matches['elo_mandante'] - df_matches['elo_visitante']
        self.elo_final = elo

        # --------------------------------------------------------------
        # Mesclar médias históricas de volta na tabela de partidas
        # --------------------------------------------------------------
        media_cols = [f'{c}_media' for c in STAT_COLS] + ['forma_pontos']

        home_feat = long[['ID', 'time'] + media_cols].rename(
            columns={**{f'{c}_media': f'mandante_{c}_media' for c in STAT_COLS},
                     'forma_pontos': 'mandante_forma_pontos'}
        )
        df_matches = df_matches.merge(
            home_feat, left_on=['ID', 'mandante'], right_on=['ID', 'time'], how='left'
        ).drop(columns=['time'])

        away_feat = long[['ID', 'time'] + media_cols].rename(
            columns={**{f'{c}_media': f'visitante_{c}_media' for c in STAT_COLS},
                     'forma_pontos': 'visitante_forma_pontos'}
        )
        df_matches = df_matches.merge(
            away_feat, left_on=['ID', 'visitante'], right_on=['ID', 'time'], how='left'
        ).drop(columns=['time'])

        df_matches = df_matches.dropna(subset=self.feature_cols)

        # --------------------------------------------------------------
        # Estado atual (mais recente) de cada time, usado para prever
        # confrontos futuros com as MESMAS features do treino
        # --------------------------------------------------------------
        self.times = sorted(long['time'].unique().tolist())
        for time, g in long.groupby('time'):
            g = g.sort_values(['data', 'ID'])
            estado = {f'{c}_media': float(g[c].tail(ROLLING_WINDOW).mean()) for c in STAT_COLS}
            estado['forma_pontos'] = float(g['pontos'].tail(5).sum())
            estado['elo'] = float(elo.get(time, ELO_INICIAL))
            self.estado_atual[time] = estado

        return df_matches

    # ------------------------------------------------------------------
    # Treinamento
    # ------------------------------------------------------------------
    def treinar(self, df_matches):
        """Treina todos os modelos usando um split cronológico (treina no
        passado, valida no futuro — como acontece na vida real)."""
        print("🚀 Treinando modelos...\n")

        df_matches = df_matches.sort_values(['data', 'ID']).reset_index(drop=True)
        split_idx = int(len(df_matches) * 0.85)

        X = df_matches[self.feature_cols].copy()
        self.scaler.fit(X.iloc[:split_idx])
        X_scaled = pd.DataFrame(self.scaler.transform(X), columns=self.feature_cols)

        X_train, X_test = X_scaled.iloc[:split_idx], X_scaled.iloc[split_idx:]
        y_train_result = df_matches['Resultado'].iloc[:split_idx]
        y_test_result = df_matches['Resultado'].iloc[split_idx:]

        # ---------------- Vencedor (classificação) ----------------
        # Testes empíricos (split cronológico) mostraram que balancear as
        # classes (Empate/Visitante têm menos exemplos) reduz a acurácia
        # real, pois o time mandante realmente vence com mais frequência.
        # Um RandomForest simples, sem balanceamento, teve o melhor resultado.
        print("  🏆 Treinando modelo de Vencedor (RandomForest)...")
        clf = RandomForestClassifier(n_estimators=400, max_depth=14, min_samples_leaf=5,
                                      random_state=42, n_jobs=-1)
        clf.fit(X_train, y_train_result)
        self.models['resultado'] = clf

        acc = accuracy_score(y_test_result, clf.predict(X_test))
        f1 = f1_score(y_test_result, clf.predict(X_test), average='macro')
        baseline = y_test_result.value_counts(normalize=True).max()
        print(f"     ✅ Acurácia (jogos futuros): {acc:.2%} | F1-macro: {f1:.2%} "
              f"(baseline ingênuo 'sempre mandante': {baseline:.2%})")

        # ---------------- Gols (regressão) ----------------
        print("  ⚽ Treinando modelos de Gols...")
        y_train_gm = df_matches['mandante_Placar'].iloc[:split_idx]
        y_test_gm = df_matches['mandante_Placar'].iloc[split_idx:]
        y_train_gv = df_matches['visitante_Placar'].iloc[:split_idx]
        y_test_gv = df_matches['visitante_Placar'].iloc[split_idx:]

        self.models['gols_mandante'] = self._treinar_regressor(X_train, y_train_gm)
        self.models['gols_visitante'] = self._treinar_regressor(X_train, y_train_gv)

        mae_m = mean_absolute_error(y_test_gm, self.models['gols_mandante'].predict(X_test))
        mae_v = mean_absolute_error(y_test_gv, self.models['gols_visitante'].predict(X_test))
        print(f"     ✅ MAE Mandante: {mae_m:.2f}, MAE Visitante: {mae_v:.2f}")

        # ---------------- Escanteios e Faltas (regressão) ----------------
        print("  🎲 Treinando modelos de Escanteios e Faltas...")
        y_train_esc = df_matches['escanteios_total'].iloc[:split_idx]
        y_test_esc = df_matches['escanteios_total'].iloc[split_idx:]
        y_train_fal = df_matches['faltas_total'].iloc[:split_idx]
        y_test_fal = df_matches['faltas_total'].iloc[split_idx:]

        self.models['escanteios'] = self._treinar_regressor(X_train, y_train_esc)
        self.models['faltas'] = self._treinar_regressor(X_train, y_train_fal)

        mae_esc = mean_absolute_error(y_test_esc, self.models['escanteios'].predict(X_test))
        mae_fal = mean_absolute_error(y_test_fal, self.models['faltas'].predict(X_test))
        print(f"     ✅ MAE Escanteios: {mae_esc:.2f}, MAE Faltas: {mae_fal:.2f}")

        # ---------------- Cartões (regressão) ----------------
        print("  🟨 Treinando modelos de Cartões...")
        y_train_am = df_matches['amarelos_total'].iloc[:split_idx]
        y_test_am = df_matches['amarelos_total'].iloc[split_idx:]
        y_train_ve = df_matches['vermelhos_total'].iloc[:split_idx]
        y_test_ve = df_matches['vermelhos_total'].iloc[split_idx:]

        self.models['amarelos'] = self._treinar_regressor(X_train, y_train_am)
        self.models['vermelhos'] = self._treinar_regressor(X_train, y_train_ve)

        mae_am = mean_absolute_error(y_test_am, self.models['amarelos'].predict(X_test))
        mae_ve = mean_absolute_error(y_test_ve, self.models['vermelhos'].predict(X_test))
        print(f"     ✅ MAE Amarelos: {mae_am:.2f}, MAE Vermelhos: {mae_ve:.2f}")

        print("\n✨ Todos os modelos treinados com sucesso!\n")
    @staticmethod
    def _treinar_regressor(X_train, y_train):
        """Ensemble de RandomForest + GradientBoosting para regressão."""
        rf = RandomForestRegressor(n_estimators=300, max_depth=10, min_samples_leaf=3,
                                    random_state=42, n_jobs=-1)
        gbr = GradientBoostingRegressor(n_estimators=200, max_depth=3, learning_rate=0.05,
                                         random_state=42)
        ensemble = VotingRegressor(estimators=[('rf', rf), ('gbr', gbr)])
        ensemble.fit(X_train, y_train)
        return ensemble

    # ------------------------------------------------------------------
    # Predição
    # ------------------------------------------------------------------
    def calcular_features_confronto(self, mandante, visitante):
        """Monta o vetor de features para um confronto hipotético usando
        o estado (forma + Elo) mais recente conhecido de cada time — o
        MESMO tipo de dado usado no treino, sem misturar com estatísticas
        reais de um jogo que ainda não aconteceu."""
        if mandante not in self.estado_atual or visitante not in self.estado_atual:
            return None

        em = self.estado_atual[mandante]
        ev = self.estado_atual[visitante]
        elo_m = em['elo']
        elo_v = ev['elo']

        features = {
            'elo_mandante': elo_m, 'elo_visitante': elo_v, 'elo_diff': elo_m - elo_v,
            'mandante_chutes_media': em['chutes_media'], 'visitante_chutes_media': ev['chutes_media'],
            'mandante_chutes_gol_media': em['chutes_gol_media'], 'visitante_chutes_gol_media': ev['chutes_gol_media'],
            'mandante_posse_media': em['posse_media'], 'visitante_posse_media': ev['posse_media'],
            'mandante_faltas_media': em['faltas_media'], 'visitante_faltas_media': ev['faltas_media'],
            'mandante_escanteios_media': em['escanteios_media'], 'visitante_escanteios_media': ev['escanteios_media'],
            'mandante_amarelos_media': em['amarelos_media'], 'visitante_amarelos_media': ev['amarelos_media'],
            'mandante_vermelhos_media': em['vermelhos_media'], 'visitante_vermelhos_media': ev['vermelhos_media'],
            'mandante_gols_marcados_media': em['gols_marcados_media'],
            'mandante_gols_sofridos_media': em['gols_sofridos_media'],
            'visitante_gols_marcados_media': ev['gols_marcados_media'],
            'visitante_gols_sofridos_media': ev['gols_sofridos_media'],
            'mandante_forma_pontos': em['forma_pontos'], 'visitante_forma_pontos': ev['forma_pontos'],
        }
        return features

    def prever(self, features_dict):
        """Faz predição para um novo jogo a partir de um dicionário de features."""
        features = pd.DataFrame(
            [[features_dict.get(col, 0) for col in self.feature_cols]],
            columns=self.feature_cols
        )
        features_normalized = pd.DataFrame(
            self.scaler.transform(features), columns=self.feature_cols
        )

        resultado = self.models['resultado'].predict(features_normalized)[0]
        resultado_proba = self.models['resultado'].predict_proba(features_normalized)[0]

        gols_m_esperado = max(0.0, float(self.models['gols_mandante'].predict(features_normalized)[0]))
        gols_v_esperado = max(0.0, float(self.models['gols_visitante'].predict(features_normalized)[0]))
        escanteios_esperado = max(0.0, float(self.models['escanteios'].predict(features_normalized)[0]))
        faltas_esperado = max(0.0, float(self.models['faltas'].predict(features_normalized)[0]))
        amarelos_esperado = max(0.0, float(self.models['amarelos'].predict(features_normalized)[0]))
        vermelhos_esperado = max(0.0, float(self.models['vermelhos'].predict(features_normalized)[0]))

        gols_m = int(round(gols_m_esperado))
        gols_v = int(round(gols_v_esperado))
        escanteios = int(round(escanteios_esperado))
        faltas = int(round(faltas_esperado))
        amarelos = int(round(amarelos_esperado))
        vermelhos = int(round(vermelhos_esperado))

        return {
            'resultado': resultado,
            'confianca': float(max(resultado_proba)),
            'probabilidades': dict(zip(self.models['resultado'].classes_, [float(p) for p in resultado_proba])),
            'gols_mandante': gols_m,
            'gols_visitante': gols_v,
            'gols_mandante_esperado': gols_m_esperado,
            'gols_visitante_esperado': gols_v_esperado,
            'placar': f"{gols_m} x {gols_v}",
            'escanteios': escanteios,
            'faltas': faltas,
            'amarelos': amarelos,
            'vermelhos': vermelhos,
            'escanteios_esperado': escanteios_esperado,
            'faltas_esperado': faltas_esperado,
            'amarelos_esperado': amarelos_esperado,
            'vermelhos_esperado': vermelhos_esperado,
        }

    def prever_confronto(self, mandante, visitante):
        """Atalho: calcula as features e já retorna a predição do confronto."""
        features = self.calcular_features_confronto(mandante, visitante)
        if features is None:
            return None, None
        return features, self.prever(features)

    def simular_confronto(self, mandante, visitante, n_simulacoes=1000, seed=None):
        """Simula o confronto várias vezes (Monte Carlo) para dar uma
        sensação real de variabilidade jogo a jogo, em vez de um único
        resultado determinístico.

        Os gols de cada time são amostrados de uma distribuição de Poisson
        cuja média é o número de gols esperado previsto pelo modelo de
        regressão (mesma abordagem usada em modelos estatísticos de futebol
        como Dixon-Coles). O placar de cada simulação define o vencedor,
        então times parelhos naturalmente produzem resultados variados
        entre as simulações, enquanto o favorito tende a vencer mais vezes.
        """
        features = self.calcular_features_confronto(mandante, visitante)
        if features is None:
            return None

        predicao = self.prever(features)
        lam_m = predicao['gols_mandante_esperado']
        lam_v = predicao['gols_visitante_esperado']
        lam_esc = predicao['escanteios_esperado']
        lam_fal = predicao['faltas_esperado']
        lam_am = predicao['amarelos_esperado']
        lam_ve = predicao['vermelhos_esperado']

        rng = np.random.default_rng(seed)
        gols_m_sim = rng.poisson(max(lam_m, 0.05), n_simulacoes)
        gols_v_sim = rng.poisson(max(lam_v, 0.05), n_simulacoes)
        escanteios_sim = rng.poisson(max(lam_esc, 0.05), n_simulacoes)
        faltas_sim = rng.poisson(max(lam_fal, 0.05), n_simulacoes)
        amarelos_sim = rng.poisson(max(lam_am, 0.05), n_simulacoes)
        vermelhos_sim = rng.poisson(max(lam_ve, 0.01), n_simulacoes)

        vitorias_mandante = int(np.sum(gols_m_sim > gols_v_sim))
        empates = int(np.sum(gols_m_sim == gols_v_sim))
        vitorias_visitante = int(np.sum(gols_m_sim < gols_v_sim))

        contagem_placares = Counter(zip(gols_m_sim.tolist(), gols_v_sim.tolist()))
        placares_mais_comuns = [
            (f"{gm} x {gv}", cont, cont / n_simulacoes * 100)
            for (gm, gv), cont in contagem_placares.most_common(5)
        ]

        contagem_escanteios = Counter(escanteios_sim.tolist())
        escanteios_mais_comuns = [
            (qtd, cont, cont / n_simulacoes * 100)
            for qtd, cont in contagem_escanteios.most_common(3)
        ]

        contagem_amarelos = Counter(amarelos_sim.tolist())
        amarelos_mais_comuns = [
            (qtd, cont, cont / n_simulacoes * 100)
            for qtd, cont in contagem_amarelos.most_common(3)
        ]

        return {
            'n_simulacoes': n_simulacoes,
            'pct_vitoria_mandante': vitorias_mandante / n_simulacoes * 100,
            'pct_empate': empates / n_simulacoes * 100,
            'pct_vitoria_visitante': vitorias_visitante / n_simulacoes * 100,
            'gols_mandante_medio': float(np.mean(gols_m_sim)),
            'gols_visitante_medio': float(np.mean(gols_v_sim)),
            'placares_mais_comuns': placares_mais_comuns,
            'escanteios_medio': float(np.mean(escanteios_sim)),
            'escanteios_mais_comuns': escanteios_mais_comuns,
            'faltas_medio': float(np.mean(faltas_sim)),
            'amarelos_medio': float(np.mean(amarelos_sim)),
            'amarelos_mais_comuns': amarelos_mais_comuns,
            'vermelhos_medio': float(np.mean(vermelhos_sim)),
            'pct_pelo_menos_1_vermelho': float(np.mean(vermelhos_sim >= 1) * 100),
            'predicao_modelo': predicao,
        }

    # ------------------------------------------------------------------
    # Persistência
    # ------------------------------------------------------------------
    def salvar_modelos(self, path='modelos_futebol.pkl'):
        """Salva os modelos treinados e o estado dos times"""
        with open(path, 'wb') as f:
            pickle.dump({
                'models': self.models,
                'scaler': self.scaler,
                'feature_cols': self.feature_cols,
                'times': self.times,
                'estado_atual': self.estado_atual,
                'elo_final': self.elo_final,
                'medias_globais': self.medias_globais,
            }, f)
        print(f"✅ Modelos salvos em {path}")

    def carregar_modelos(self, path='modelos_futebol.pkl'):
        """Carrega modelos salvos"""
        with open(path, 'rb') as f:
            data = pickle.load(f)
            self.models = data['models']
            self.scaler = data['scaler']
            self.feature_cols = data['feature_cols']
            self.times = data.get('times', [])
            self.estado_atual = data.get('estado_atual', {})
            self.elo_final = data.get('elo_final', {})
            self.medias_globais = data.get('medias_globais', {})
        print(f"✅ Modelos carregados de {path}")


def main():
    """Função principal"""
    print("=" * 80)
    print("🏆 PREDITOR DE RESULTADOS DE FUTEBOL - CAMPEONATO BRASILEIRO")
    print("=" * 80)
    print()

    preditor = PreditorFutebol()

    df_matches, df_stats, _, _ = preditor.carregar_dados()
    df_matches = preditor.preparar_features(df_matches, df_stats)
    preditor.treinar(df_matches)

    print("=" * 80)
    print("EXEMPLOS DE PREDIÇÃO (confrontos reais, com forma atual dos times)")
    print("=" * 80)

    exemplos = [('Flamengo', 'Botafogo-RJ'), ('Palmeiras', 'Santos'), ('Gremio', 'Internacional')]
    for mandante, visitante in exemplos:
        features, pred = preditor.prever_confronto(mandante, visitante)
        if pred is None:
            continue
        print(f"\n📌 {mandante} x {visitante}")
        print(f"  Resultado: {pred['resultado']} (Confiança: {pred['confianca']:.1%})")
        print(f"  Placar: {pred['placar']}")
        print(f"  Escanteios: {pred['escanteios']} | Faltas: {pred['faltas']}")

    preditor.salvar_modelos()

    print("\n" + "=" * 80)
    print("✅ Predições concluídas!")
    print("=" * 80)


if __name__ == '__main__':
    main()
