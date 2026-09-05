# 📁 Estrutura do Projeto

## Organização das Pastas

```
predicoes-resultados-brasileirao/
│
├── 📊 dados/                              # Arquivos de dados (CSV)
│   ├── campeonato-brasileiro-full.csv             # Dados completos das partidas
│   ├── campeonato-brasileiro-estatisticas-full.csv # Estatísticas de jogo
│   ├── campeonato-brasileiro-gols.csv             # Dados de gols
│   ├── campeonato-brasileiro-cartoes.csv          # Dados de cartões
│   └── Legenda.txt                                # Dicionário de dados
│
├── 📚 documentacao/                       # Guias e documentação
│   ├── README.md (raiz)                       # Guia principal
│   ├── GUIA_INTERPRETACAO.md                  # Como interpretar os dados
│   ├── GUIA_PREDITOR_TIMES.py                 # Guia de uso
│   ├── GUIA_STATSBOMB_INTEGRATION.md          # Integração com StatsBomb
│   ├── LEIA_PRIMEIRO.txt                      # Ponto de partida
│   ├── COMECE_AQUI.txt                        # Instruções rápidas
│   ├── COMECE_AQUI_NOVO.txt                   # Versão atualizada
│   ├── NOVO_PREDITOR_TIMES.txt                # Info sobre novo preditor
│   ├── INICIO_RAPIDO.txt                      # Quick start
│   ├── AVISOS_WARNINGS.md                     # Avisos importantes
│   ├── SUMARIO.md                             # Sumário do projeto
│   ├── TROUBLESHOOTING.md                     # Resolução de problemas
│   └── requirements.txt                       # Dependências Python
│
├── 🤖 scripts/                            # Código principal executável
│   ├── preditor_futebol.py                    # Script principal de predição
│   ├── preditor_por_time.py                   # Predições por time específico
│   ├── teste_rapido.py                        # Testes rápidos
│   ├── demonstracao_predicoes.py              # Demonstrações
│   ├── exemplos_avancados.py                  # Exemplos complexos
│   └── inicio_rapido.py                       # Quick start script
│
├── 🔗 integracao/                         # Integração com APIs externas
│   ├── integracao_statsbomb.py                # Classe StatsBombIntegration
│   ├── clonar_statsbomb.py                    # Clonar repo StatsBomb
│   ├── teste_statsbomb.py                     # Testar integração
│   └── GUIA_STATSBOMB_INTEGRATION.md          # Documentação
│
├── 📓 exemplos/                           # Notebooks e demos
│   └── predicao_futebol.ipynb                 # Notebook Jupyter completo
│
├── 🎯 modelos/                            # Modelos treinados (pickle)
│   ├── modelos_futebol.pkl                    # Modelos principais
│   └── modelos_teste.pkl                      # Modelos de teste
│
├── 📈 analises/                           # Resultados de análises
│   └── (vazio - para análises customizadas)
│
├── 🔧 Arquivos de Configuração
│   ├── .gitignore                             # Arquivos ignorados por Git
│   ├── requirements.txt                       # Dependências (raiz)
│   └── ESTRUTURA_PROJETO.md                   # Este arquivo
│
└── 📖 README.md                           # Documentação principal
```

## 📂 Descrição de Cada Pasta

### 📊 `/dados`
Contém todos os arquivos de dados (CSV) e dicionários.
- **Arquivos CSV**: Dados brutos do Campeonato Brasileiro
- **Legenda.txt**: Explica o significado de cada coluna

**Uso:**
```python
import pandas as pd
df = pd.read_csv('dados/campeonato-brasileiro-full.csv')
```

### 📚 `/documentacao`
Guias, tutoriais e referências.
- **README**: Ponto de partida principal
- **GUIA_*.md**: Guias temáticos
- **COMECE_AQUI.txt**: Para iniciantes
- **TROUBLESHOOTING.md**: Solução de problemas

**Uso:** Leia os arquivos `.txt` e `.md` conforme necessidade.

### 🤖 `/scripts`
Código Python executável pronto para usar.
- **preditor_futebol.py**: Script principal
- **teste_rapido.py**: Testes rápidos
- **exemplos_avancados.py**: Casos complexos

**Uso:**
```bash
python scripts/preditor_futebol.py
python scripts/teste_rapido.py
```

### 🔗 `/integracao`
Arquivos de integração com APIs externas (StatsBomb, etc.).
- **integracao_statsbomb.py**: Classe para usar StatsBomb
- **clonar_statsbomb.py**: Download de dados StatsBomb
- **teste_statsbomb.py**: Teste de funcionalidades

**Uso:**
```python
from integracao.integracao_statsbomb import StatsBombIntegration
sb = StatsBombIntegration()
```

### 📓 `/exemplos`
Notebooks Jupyter e demonstrações interativas.
- **predicao_futebol.ipynb**: Notebook completo com análises

**Uso:**
```bash
jupyter notebook exemplos/predicao_futebol.ipynb
```

### 🎯 `/modelos`
Modelos de Machine Learning treinados (formato pickle).
- **modelos_futebol.pkl**: Modelos principais
- **modelos_teste.pkl**: Modelos para testes

**Uso:**
```python
import pickle
with open('modelos/modelos_futebol.pkl', 'rb') as f:
    modelos = pickle.load(f)
```

### 📈 `/analises`
Pasta reservada para análises customizadas e resultados.
- Crie subpastas conforme necessário
- Salve resultados de análises

## 🚀 Como Começar

### 1️⃣ Leitura Inicial
```bash
# Comece por aqui
cat documentacao/LEIA_PRIMEIRO.txt
cat documentacao/COMECE_AQUI.txt
```

### 2️⃣ Explorar Dados
```bash
# Veja o dicionário de dados
cat dados/Legenda.txt

# Carregue os dados em Python
python scripts/teste_rapido.py
```

### 3️⃣ Executar Predições
```bash
# Run principal script
python scripts/preditor_futebol.py

# Ou abra o notebook
jupyter notebook exemplos/predicao_futebol.ipynb
```

### 4️⃣ Usar StatsBomb
```bash
# Clone os dados
python integracao/clonar_statsbomb.py

# Ou faça um teste rápido
python integracao/teste_statsbomb.py
```

## 📦 Estrutura de Imports

Após essa organização, atualize seus imports:

### Antes:
```python
import preditor_futebol
df = pd.read_csv('campeonato-brasileiro-full.csv')
```

### Depois:
```python
from scripts import preditor_futebol
df = pd.read_csv('dados/campeonato-brasileiro-full.csv')
from integracao.integracao_statsbomb import StatsBombIntegration
```

## 🔄 Adicionar Novos Arquivos

Quando adicionar novos arquivos, coloque-os na pasta apropriada:

- **Novo script Python?** → `/scripts`
- **Novo guia/documentação?** → `/documentacao`
- **Novo dataset CSV?** → `/dados`
- **Novo notebook?** → `/exemplos`
- **Nova integração?** → `/integracao`
- **Análise resultado?** → `/analises`

## 📝 Manutenção

### Atualizar requirements.txt
```bash
pip freeze > requirements.txt
```

### Limpar cache Python
```bash
rm -r __pycache__ .ipynb_checkpoints
```

### Fazer backup
```bash
git add .
git commit -m "Descrição das mudanças"
git push origin main
```

## ✅ Vantagens dessa Estrutura

✓ **Organização clara** - Fácil encontrar arquivos
✓ **Escalabilidade** - Cresce com o projeto
✓ **Colaboração** - Outros entenderão a estrutura
✓ **Profissionalismo** - Padrão da indústria
✓ **Manutenibilidade** - Fácil fazer updates
✓ **Documentação** - Tudo bem documentado

---

**Data**: Setembro 2026
**Estrutura versão**: 1.0
