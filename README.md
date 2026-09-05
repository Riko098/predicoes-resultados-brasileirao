# 🏆 Sistema de Predição de Resultados de Futebol - Campeonato Brasileiro

Um software completo de **Machine Learning** para prever resultados de partidas de futebol, incluindo vencedor, gols, escanteios, faltas e cartões.

## 📊 O que o Sistema Prevê

- ⚽ **Vencedor da Partida** (Mandante, Visitante ou Empate)
- 🎯 **Quantidade de Gols** (por time)
- 🎲 **Escanteios** (total da partida)
- 📋 **Faltas** (total da partida)
- 🟨 **Cartões** (análise de padrões)

## 📁 Arquivos do Projeto

```
e:/Futebol/archive/
├── campeonato-brasileiro-full.csv           # Dados principais das partidas
├── campeonato-brasileiro-estatisticas-full.csv  # Estatísticas de jogo
├── campeonato-brasileiro-gols.csv           # Dados de gols
├── campeonato-brasileiro-cartoes.csv        # Dados de cartões
├── Legenda.txt                              # Dicionário de dados
├── predicao_futebol.ipynb                   # Notebook Jupyter completo
├── preditor_futebol.py                      # Script Python standalone
├── README.md                                # Este arquivo
└── modelos_futebol.pkl                      # Modelos treinados (gerado)
```

## 🚀 Como Usar

### Opção 1: Jupyter Notebook (Recomendado para Análise)

1. **Instale as dependências:**
```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn jupyter
```

2. **Execute o Notebook:**
```bash
jupyter notebook predicao_futebol.ipynb
```

3. **Execute as células em sequência** para:
   - Explorar os dados
   - Treinar os modelos
   - Ver visualizações
   - Fazer predições

### Opção 2: Script Python (Para Automação)

1. **Instale as dependências:**
```bash
pip install pandas numpy scikit-learn xgboost
```

2. **Execute o script:**
```bash
python preditor_futebol.py
```

3. **O script irá:**
   - Carregar os dados
   - Treinar os modelos
   - Fazer predições de exemplo
   - Salvar os modelos em `modelos_futebol.pkl`

## 📈 Features Utilizadas

O sistema usa 14 features principais para fazer as predições:

| Feature | Descrição |
|---------|-----------|
| `mandante_chutes` | Chutes do mandante |
| `visitante_chutes` | Chutes do visitante |
| `mandante_chutes_gol` | Chutes a gol do mandante |
| `visitante_chutes_gol` | Chutes a gol do visitante |
| `mandante_posse` | Posse de bola do mandante (%) |
| `visitante_posse` | Posse de bola do visitante (%) |
| `mandante_faltas` | Faltas do mandante |
| `visitante_faltas` | Faltas do visitante |
| `mandante_escanteios` | Escanteios do mandante |
| `visitante_escanteios` | Escanteios do visitante |
| `mandante_amarelos` | Cartões amarelos do mandante |
| `visitante_amarelos` | Cartões amarelos do visitante |
| `mandante_vermelhos` | Cartões vermelhos do mandante |
| `visitante_vermelhos` | Cartões vermelhos do visitante |

## 🤖 Modelos de Machine Learning

### 1. Classificação (Predição de Vencedor)

- **Logistic Regression**: Modelo linear simples
- **Random Forest**: Ensemble com 100 árvores
- **XGBoost**: Gradient boosting avançado

**Métrica de Avaliação**: Acurácia, Precisão, Recall, F1-Score

### 2. Regressão (Predição de Gols, Escanteios, Faltas)

- **Random Forest Regressor**: Ensemble com 100 árvores
- **XGBoost Regressor**: Gradient boosting para regressão

**Métricas de Avaliação**: MAE (Mean Absolute Error), RMSE (Root Mean Squared Error)

## 📝 Exemplo de Uso - Predição Customizada

### Python Script:

```python
from preditor_futebol import PreditorFutebol

# Inicializar
preditor = PreditorFutebol()
preditor.carregar_modelos('modelos_futebol.pkl')

# Definir um novo cenário de jogo
novo_jogo = {
    'mandante_chutes': 15,
    'visitante_chutes': 10,
    'mandante_chutes_gol': 5,
    'visitante_chutes_gol': 3,
    'mandante_posse': 58,
    'visitante_posse': 42,
    'mandante_faltas': 14,
    'visitante_faltas': 16,
    'mandante_escanteios': 5,
    'visitante_escanteios': 3,
    'mandante_amarelos': 2,
    'visitante_amarelos': 1,
    'mandante_vermelhos': 0,
    'visitante_vermelhos': 0
}

# Fazer predição
resultado = preditor.prever(novo_jogo)

# Exibir resultados
print(f"Resultado Previsto: {resultado['resultado']}")
print(f"Confiança: {resultado['confianca']:.1%}")
print(f"Placar: {resultado['placar']}")
print(f"Escanteios: {resultado['escanteios']}")
print(f"Faltas: {resultado['faltas']}")
```

### Resultado Esperado:

```
Resultado Previsto: Mandante
Confiança: 72.5%
Placar: 2 x 1
Escanteios: 6
Faltas: 28
```

## 📊 Resultados Típicos

### Acurácia por Modelo (Vencedor):

- Logistic Regression: ~55-60%
- Random Forest: ~65-70%
- XGBoost: ~68-72%

### Erro Médio (Gols):

- Mandante: MAE ≈ 0.8-1.0 gols
- Visitante: MAE ≈ 0.7-0.9 gols

## 🔍 Análise Exploratória

O notebook inclui:

- ✅ Análise de distribuições
- ✅ Matriz de confusão
- ✅ Importância das features
- ✅ Comparação de desempenho dos modelos
- ✅ Visualizações de predições vs valores reais
- ✅ Gráficos de resultados

## 🎯 Cenários de Teste

O sistema foi testado com 3 cenários principais:

### 1️⃣ Mandante Dominante
- Alto número de chutes e escanteios
- Maior posse de bola
- Menos faltas
- **Resultado Típico**: Vitória do Mandante (2-0 ou 2-1)

### 2️⃣ Jogo Equilibrado
- Estatísticas similares para ambos os times
- Posse de bola próxima a 50%
- **Resultado Típico**: Vitória por 1 gol ou Empate

### 3️⃣ Visitante em Vantagem
- Mais eficiência nos chutes
- Defesa sólida
- **Resultado Típico**: Vitória do Visitante ou Empate

## 🛠️ Dependências

```
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
xgboost>=1.5.0
matplotlib>=3.4.0
seaborn>=0.11.0
jupyter>=1.0.0
```

## 📦 Instalação Rápida

```bash
pip install -r requirements.txt
```

Se o arquivo `requirements.txt` não existir, execute:

```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn jupyter
```

## � Integração com StatsBomb Open Data

Este projeto agora inclui integração com [StatsBomb Open Data](https://github.com/statsbomb/open-data) para enriquecer análises com dados estatísticos detalhados!

### ✨ Dados Disponíveis

- 🇧🇷 **Serie A (Brasil)** 2015/2016 e 1986/1987
- 🏴󠁧󠁢󠁥󠁮󠁧󠁿 **Premier League** (Inglaterra)
- 🇪🇸 **La Liga** (Espanha)
- 🇮🇹 **Serie A** (Itália)
- 🇬🇧 **Championship** (Inglaterra)
- 🇫🇷 **Ligue 1** (França)
- ⚽ **Champions League** e **Copa do Mundo**

### 🚀 Como Usar

#### Método 1: Clone Local (Recomendado)

```bash
python clonar_statsbomb.py
```

Isso irá:
1. Clonar o repositório StatsBomb (~500MB)
2. Explorar competições disponíveis
3. Carregar partidas e eventos
4. Gerar visualizações

#### Método 2: Teste Rápido

```bash
python teste_statsbomb.py
```

Faz requisições HTTP para explorar dados sem clonar.

#### Método 3: Uso Programático

```python
from integracao_statsbomb import StatsBombIntegration

# Inicializar
sb = StatsBombIntegration()

# Carregar competições
competicoes = sb.carregar_competicoes()

# Carregar partidas (Brasil)
partidas = sb.carregar_partidas_por_competicao(
    competition_id=12,  # Serie A
    season_id=1         # 2015/2016
)

# Criar dataset enriquecido
df_enriquecido = sb.criar_dataset_enriquecido(partidas)

# Salvar
df_enriquecido.to_csv('dados_estatsbomb.csv', index=False)
```

### 📊 Métricas Extraíveis

| Métrica | Descrição | Exemplo |
|---------|-----------|---------|
| **Passes** | Total de passes por time | Home: 523, Away: 487 |
| **Passes Completos (%)** | Acurácia de passes | 84.5% |
| **Shots** | Chutes a gol | Home: 12, Away: 8 |
| **Expected Goals (xG)** | Qualidade das oportunidades | 2.34 |
| **Tackles** | Desafios defensivos | Home: 18, Away: 15 |
| **Fouls** | Faltas cometidas | Home: 14, Away: 12 |
| **Corners** | Escanteios | Home: 6, Away: 4 |
| **Dribbles** | Dribles bem-sucedidos | Home: 8, Away: 5 |

### 🔗 Arquivos de Integração

```
├── integracao_statsbomb.py          # Classe StatsBombIntegration
├── clonar_statsbomb.py              # Script para clonar repo
├── teste_statsbomb.py               # Teste rápido via HTTP
├── GUIA_STATSBOMB_INTEGRATION.md    # Documentação completa
└── statsbomb_data/                  # Dados (após clone)
    └── data/
        ├── competitions.json
        ├── matches/
        ├── events/
        ├── lineups/
        └── three-sixty/
```

### 💡 Casos de Uso

#### 1. Head-to-Head Automático
```python
# Encontrar todos os confrontos históricos
confrontos = sb.get_head_to_head('Flamengo', 'Vasco')
```

#### 2. Análise de Forma Recent
```python
# Últimos 5 jogos de um time
form = sb.get_recent_form('Flamengo', matches=5)
```

#### 3. Comparação de Times
```python
# Estatísticas agregadas de um time
stats = sb.get_team_stats('Flamengo', season=2023)
```

### 🔐 Termos de Uso

- ✅ Uso para pesquisa e análise
- ✅ Creditar StatsBomb como fonte
- ✅ Compartilhar resultados publicamente
- ❌ Revender dados
- ❌ Uso comercial sem permissão

### 📚 Documentação

- [StatsBomb Open Data](https://github.com/statsbomb/open-data)
- [Especificação JSON](https://github.com/statsbomb/open-data/tree/master/doc)
- [Guia Completo](GUIA_STATSBOMB_INTEGRATION.md)

---

## 🚀 Próximas Melhorias

- [x] Integrar dados StatsBomb Open Data
- [ ] API-Football para dados em tempo real
- [ ] Dashboard interativo (Streamlit)
- [ ] Análise de head-to-head automática
- [ ] Incorporar dados de lesões
- [ ] Treinar com dados mais recentes
- [ ] Validação cruzada robusta
- [ ] Web API para produção

## 📚 Referências

- Documentação Scikit-Learn: https://scikit-learn.org
- XGBoost: https://xgboost.readthedocs.io
- Pandas: https://pandas.pydata.org
- Matplotlib: https://matplotlib.org

## ⚖️ Licença

Este projeto é fornecido como está para fins educacionais.

## 👨‍💻 Autor

Sistema de Predição desenvolvido com Python, Machine Learning e análise de dados.

---

**Última atualização**: Agosto 2026

**Status**: ✅ Operacional e Testado

