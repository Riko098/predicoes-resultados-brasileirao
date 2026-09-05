# Guia: Integração StatsBomb Open Data

## 📊 Sobre o StatsBomb Open Data

O repositório [StatsBomb Open Data](https://github.com/statsbomb/open-data) fornece:

- **Dados de partidas** completas com resultados
- **Eventos detalhados** (passes, chutes, dribles, etc.)
- **Escalações** de jogadores
- **Dados 360** (posicionamento espacial)
- **Múltiplas ligasas**: Premier League, LaLiga, Serie A, Bundesliga, Ligue 1, e outras

## 🚀 Como Usar

### Opção 1: Via Script Python (Recomendado)

```python
from integracao_statsbomb import StatsBombIntegration

# Inicializar
sb = StatsBombIntegration()

# 1. Ver competições disponíveis
competicoes = sb.carregar_competicoes()

# 2. Carregar partidas
df_partidas = sb.carregar_partidas_por_competicao(
    competition_id=24,  # Ajuste conforme a competição
    season_id=1
)

# 3. Criar dataset enriquecido
df_enriquecido = sb.criar_dataset_enriquecido(df_partidas, extrair_eventos=True)

# 4. Salvar
df_enriquecido.to_csv('dados_enriquecidos.csv', index=False)
```

### Opção 2: Clonar Repositório Inteiro

```bash
git clone https://github.com/statsbomb/open-data.git
```

Estrutura de pastas:
```
open-data/
├── data/
│   ├── competitions.json
│   ├── matches/14/1.json (La Liga 2020/21)
│   ├── events/
│   ├── lineups/
│   └── three-sixty/
```

## 💡 Casos de Uso para Seu Projeto

### 1. **Head-to-Head Automático**
```python
# Encontrar todos os confrontos históricos entre dois times
def get_head_to_head(team1, team2):
    # Filtrar eventos onde ambos os times jogaram
    pass
```

### 2. **Análise de Posse de Bola**
```python
# Extrair estatísticas de passes por time
stats['home_passes'] = contar_passes_por_time('home')
stats['away_passes'] = contar_passes_por_time('away')
```

### 3. **Chutes em Direção ao Gol**
```python
# Diferenciar chutes (shots) com/sem xG (expected goals)
eventos = [e for e in eventos if e['type']['name'] == 'Shot']
```

### 4. **Padrões de Desempenho**
```python
# Combinar com seu preditor:
- Posse de bola anterior
- Chutes em direção ao gol
- Qualidade de passes
- Falta cometidas
```

## 📦 Instalação de Dependências

```bash
pip install requests pandas
```

## ⚙️ Integração com Seu Modelo

```python
import pickle
from integracao_statsbomb import StatsBombIntegration

# Carregue seu modelo existente
with open('preditor_futebol.pkl', 'rb') as f:
    modelo = pickle.load(f)

# Obtenha dados enriquecidos
sb = StatsBombIntegration()
dados = sb.criar_dataset_enriquecido(...)

# Combine features
df_final = combinar_com_features_antigas(dados)

# Faça predições
predicoes = modelo.predict(df_final)
```

## 🔍 Exploração dos Dados

### Ver Competições Disponíveis:
```python
sb = StatsBombIntegration()
competicoes = sb.carregar_competicoes()
print(competicoes[['competition_name', 'season_name']])
```

### Carregar Eventos de Uma Partida:
```python
eventos = sb.carregar_eventos_partida(match_id=3788741)

# Listar tipos de eventos disponíveis
tipos = set([e['type']['name'] for e in eventos])
print(tipos)
# {'Pass', 'Shot', 'Tackle', 'Foul Committed', 'Duel', ...}
```

### Extrair Metadados de Escalação:
```python
# Informações de jogadores, posição, número
lineups = sb.carregar_lineups(match_id)
```

## 📈 Métricas que Pode Extrair

| Métrica | Como Extrair | Valor Preditivo |
|---------|-------------|-----------------|
| **Posse (%)** | Contar passes | Muito Alto |
| **Chutes** | Filter 'Shot' events | Alto |
| **xG (Expected Goals)** | Campo 'statistic' | Muito Alto |
| **Passes Completos (%)** | Pass accuracy | Alto |
| **Defesas** | Filter 'Tackle' events | Médio |
| **Faltas** | Filter 'Foul Committed' | Médio |
| **Escancaros** | Filter 'Corner Awarded' | Baixo |

## ⚠️ Limitações

- ❌ Brasileirão **não está** nos dados abertos (dados são principalmente europeus)
- ⏱️ Carregamento de eventos é lento (use cache/local storage)
- 📍 Dados podem ter delay de alguns dias

## 🎯 Próximos Passos Recomendados

1. **Combinar com API-Football** para dados do Brasileirão
2. **Cache Local**: Baixe dados do StatsBomb uma vez e reutilize
3. **Feature Engineering**: Crie features lag (últimos N jogos)
4. **Validação Cruzada**: Teste modelo com dados históricos

## 📚 Documentação Completa

- [Guia de Eventos](https://github.com/statsbomb/open-data/tree/master/doc)
- [JSON Format](https://github.com/statsbomb/open-data/blob/master/doc/stats_data_json_specification.md)
- [xG Methodology](https://statsbomb.com/resource-centre/)

---
**Próximo**: Integrar com API-Football para dados em tempo real do Brasileirão!
