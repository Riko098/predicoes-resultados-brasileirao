# 🔧 Guia de Solução de Problemas

## Problemas Comuns e Soluções

---

## 1. Erro: "ModuleNotFoundError: No module named 'pandas'"

### Causa
Bibliotecas necessárias não estão instaladas.

### Solução
```bash
pip install -r requirements.txt
```

Ou instale individualmente:
```bash
pip install pandas numpy scikit-learn xgboost matplotlib seaborn jupyter
```

### Se o problema persistir
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar com flag de compatibilidade
pip install --upgrade -r requirements.txt --force-reinstall
```

---

## 2. Erro: "FileNotFoundError: campeonato-brasileiro-full.csv"

### Causa
Os arquivos CSV não estão no diretório correto.

### Solução
1. Verifique se está no diretório correto:
```bash
cd e:\Futebol\archive
dir *.csv
```

2. Confirme que os 4 arquivos CSV estão presentes:
   - `campeonato-brasileiro-full.csv`
   - `campeonato-brasileiro-estatisticas-full.csv`
   - `campeonato-brasileiro-gols.csv`
   - `campeonato-brasileiro-cartoes.csv`

3. Se faltam arquivos, copie-os de volta para o diretório.

---

## 3. Erro: "Kernel crashed" ou "Out of Memory" no Jupyter

### Causa
Dataset muito grande para a RAM disponível.

### Solução
#### Opção 1: Usar amostra dos dados (rápido)
```python
# No notebook, carregue apenas parte dos dados
df_matches = pd.read_csv('campeonato-brasileiro-full.csv', nrows=1000)
```

#### Opção 2: Aumentar memória do kernel
```bash
# Feche o Jupyter
# Execute com mais memória
jupyter notebook --NotebookApp.max_body_size=1000000000
```

#### Opção 3: Usar o script Python (mais eficiente)
```bash
python preditor_futebol.py
```

---

## 4. Erro: "ValueError: could not convert string to float"

### Causa
Dados corrompidos ou formato incorreto em uma coluna.

### Solução
O script já trata isto, mas se o erro persistir:

```python
# Adicione esta linha antes de treinar
df_matches = df_matches.replace([np.inf, -np.inf], np.nan)
df_matches = df_matches.dropna()
```

---

## 5. Predições Muito Ruins (Acurácia < 50%)

### Causa
Possíveis motivos:
- Dados corrompidos
- Features não normalizadas
- Modelo debalanceado
- Dados indiferentes

### Solução
1. **Verifique os dados**:
```python
df_matches.describe()
df_matches.isnull().sum()
```

2. **Rebalancear dados**:
```python
# No notebook, rebalancear classes
from sklearn.utils import class_weight
class_weights = class_weight.compute_class_weight('balanced', 
    np.unique(y_train), y_train)
```

3. **Treinar novamente com hiperparâmetros diferentes**:
```python
rf_model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
```

---

## 6. Jupyter Notebook Não Abre

### Causa
Jupyter não instalado ou porta bloqueada.

### Solução
```bash
# Instalar Jupyter
pip install jupyter ipykernel

# Executar em porta diferente
jupyter notebook --port=8889

# Ou verificar qual processo usa a porta
netstat -ano | findstr :8888  # Windows
lsof -i :8888                  # Linux/Mac
```

---

## 7. Script Python Muito Lento

### Causa
Treinamento de modelos é computacionalmente intensivo.

### Solução
1. **Use apenas dados de teste**:
```python
# Carregar menos dados
df_matches = df_matches.head(1000)
```

2. **Reduza o número de árvores**:
```python
rf_model = RandomForestClassifier(n_estimators=50, random_state=42)  # Ao invés de 100
```

3. **Use GPU** (se disponível):
```python
# Para XGBoost
xgb_model = xgb.XGBClassifier(tree_method='gpu_hist', gpu_id=0)
```

4. **Executar em paralelo**:
```python
rf_model = RandomForestClassifier(n_estimators=100, n_jobs=-1)  # Usar todos os cores
```

---

## 8. Erro: "UnicodeDecodeError" ao ler CSV

### Causa
Arquivo CSV com encoding diferente.

### Solução
```python
# Especificar encoding
df = pd.read_csv('arquivo.csv', encoding='latin-1')
# ou
df = pd.read_csv('arquivo.csv', encoding='utf-8')
# ou
df = pd.read_csv('arquivo.csv', encoding='iso-8859-1')
```

---

## 9. Modelos Salvos Não Carregam

### Causa
Arquivo pickle corrompido ou versão incompatível.

### Solução
```bash
# Treinar novamente
python preditor_futebol.py
# Irá salvar novo arquivo de modelos
```

Ou remover arquivo antigo:
```bash
rm modelos_futebol.pkl
python preditor_futebol.py
```

---

## 10. Predições Muito Genéricas (Sempre Mesma Classe)

### Causa
Classes desbalanceadas no dataset.

### Solução
1. **Verificar distribuição**:
```python
df_matches['Resultado'].value_counts()
```

2. **Usar stratify no split**:
```python
from sklearn.model_selection import train_test_split
train_test_split(X, y, stratify=y)
```

3. **Usar class weights**:
```python
rf_model = RandomForestClassifier(class_weight='balanced')
```

---

## 11. Erro ao Instalar XGBoost no Windows

### Causa
Falta de compilador C++.

### Solução
```bash
# Tente instalar a versão pré-compilada
pip install xgboost

# Se falhar, use:
conda install -c conda-forge xgboost

# Ou instale versão específica
pip install xgboost==1.7.0
```

---

## 12. Jupyter Notebook Muito Lento

### Causa
Muitas células executadas, kernel sobrecarregado.

### Solução
1. **Reiniciar kernel**: `Kernel > Restart`
2. **Limpar output**: `Cell > All Output > Clear`
3. **Salvar e reabrir**: Feche e abra novamente

---

## 13. Permissão Negada ao Salvar Arquivos

### Causa
Diretório protegido ou arquivo em uso.

### Solução
```bash
# Verificar permissões
ls -l  # Linux/Mac

# Se necessário, mudar para diretório com permissão
cd C:\Users\{seu_usuario}\Desktop  # Windows
```

---

## 14. Importação de Módulo Falha em Script

### Causa
Script está em diretório diferente do módulo.

### Solução
```python
import sys
sys.path.append('e:/Futebol/archive')

from preditor_futebol import PreditorFutebol
```

Ou execute do diretório correto:
```bash
cd e:\Futebol\archive
python seu_script.py
```

---

## 15. Predições Muito Diferentes do Esperado

### Causa
Features de entrada fora do padrão.

### Solução
1. **Verificar intervalo de features**:
```python
print(X_train.describe())
```

2. **Validar entrada**:
```python
# Chutes não devem ser negativos
assert features['mandante_chutes'] >= 0
# Posse de bola entre 0-100
assert 0 <= features['mandante_posse'] <= 100
```

3. **Normalizar manualmente**:
```python
features_norm = scaler.transform(features)
```

---

## 🆘 Problema Não Listado?

### Passos de Debugging

1. **Ativar modo verboso**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

2. **Adicionar prints**:
```python
print(f"DEBUG: {variavel}")
```

3. **Usar debugger**:
```python
import pdb; pdb.set_trace()
```

4. **Verificar versões**:
```bash
python --version
pip list
```

---

## 📞 Recursos de Ajuda

### Documentação
- [Pandas Docs](https://pandas.pydata.org/docs/)
- [Scikit-Learn Docs](https://scikit-learn.org/stable/)
- [XGBoost Docs](https://xgboost.readthedocs.io/)

### Stack Overflow
- Procure por "[python] [pandas] seu erro"
- Procure por "[machine-learning] seu erro"

### Comunidades
- r/MachineLearning
- r/Python
- Stack Overflow

---

## ✅ Checklist de Diagnóstico

Se algo não funciona, siga esta ordem:

- [ ] Python versão 3.7+?
- [ ] Pip atualizado?
- [ ] `pip install -r requirements.txt` executado?
- [ ] CSVs no diretório correto?
- [ ] Espaço em disco disponível (> 1GB)?
- [ ] RAM suficiente (> 2GB)?
- [ ] Firewall não bloqueia Jupyter?
- [ ] Arquivos não corrompidos?
- [ ] Codificação de arquivo correta?

---

## 🚀 Reiniciar Tudo (Nuclear Option)

Se tudo falhar:

```bash
# 1. Deletar ambientes Python antigos
pip uninstall -y -r requirements.txt

# 2. Reinstalar dependências
pip install --upgrade -r requirements.txt --force-reinstall

# 3. Limpar cache
pip cache purge

# 4. Reimportar dados se necessário

# 5. Treinar modelos novamente
python preditor_futebol.py
```

---

**Última atualização**: Agosto 2026

**Lembre-se**: A maioria dos problemas tem solução simples. Leia as mensagens de erro com atenção!

