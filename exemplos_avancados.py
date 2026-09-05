"""
📚 EXEMPLOS AVANÇADOS DE USO DO PREDITOR DE FUTEBOL

Este arquivo contém exemplos de como usar o sistema de predição
em diferentes cenários e casos de uso.
"""

from preditor_futebol import PreditorFutebol
import json
from datetime import datetime

# ============================================================================
# EXEMPLO 1: Treinar e Salvar Modelos
# ============================================================================

def exemplo_1_treinar_modelos():
    """Treina e salva os modelos para uso futuro"""
    print("\n" + "=" * 80)
    print("EXEMPLO 1: Treinar e Salvar Modelos")
    print("=" * 80)
    
    preditor = PreditorFutebol()
    df_matches, df_stats, _, _ = preditor.carregar_dados()
    df_matches = preditor.preparar_features(df_matches, df_stats)
    preditor.treinar(df_matches)
    preditor.salvar_modelos('modelos_futebol_v1.pkl')
    
    print("✅ Modelos salvos com sucesso!")


# ============================================================================
# EXEMPLO 2: Carregar Modelos Treinados
# ============================================================================

def exemplo_2_carregar_modelos():
    """Carrega modelos já treinados para não precisar treinar novamente"""
    print("\n" + "=" * 80)
    print("EXEMPLO 2: Carregar Modelos Treinados")
    print("=" * 80)
    
    preditor = PreditorFutebol()
    
    try:
        preditor.carregar_modelos('modelos_futebol_v1.pkl')
        print("✅ Modelos carregados com sucesso!")
        return preditor
    except FileNotFoundError:
        print("⚠️  Arquivo de modelos não encontrado. Treinando novos modelos...")
        df_matches, df_stats, _, _ = preditor.carregar_dados()
        df_matches = preditor.preparar_features(df_matches, df_stats)
        preditor.treinar(df_matches)
        return preditor


# ============================================================================
# EXEMPLO 3: Predições em Lote
# ============================================================================

def exemplo_3_predicoes_em_lote():
    """Faz predições para múltiplas partidas de uma vez"""
    print("\n" + "=" * 80)
    print("EXEMPLO 3: Predições em Lote")
    print("=" * 80)
    
    preditor = exemplo_2_carregar_modelos()
    
    # Definir múltiplos cenários
    partidas = [
        {
            'nome': 'Flamengo vs Botafogo (Dominância Flamengo)',
            'features': {
                'mandante_chutes': 22, 'visitante_chutes': 6,
                'mandante_chutes_gol': 9, 'visitante_chutes_gol': 1,
                'mandante_posse': 70, 'visitante_posse': 30,
                'mandante_faltas': 10, 'visitante_faltas': 16,
                'mandante_escanteios': 8, 'visitante_escanteios': 1,
                'mandante_amarelos': 1, 'visitante_amarelos': 2,
                'mandante_vermelhos': 0, 'visitante_vermelhos': 0
            }
        },
        {
            'nome': 'São Paulo vs Corinthians (Clássico Equilibrado)',
            'features': {
                'mandante_chutes': 14, 'visitante_chutes': 13,
                'mandante_chutes_gol': 5, 'visitante_chutes_gol': 5,
                'mandante_posse': 51, 'visitante_posse': 49,
                'mandante_faltas': 15, 'visitante_faltas': 14,
                'mandante_escanteios': 4, 'visitante_escanteios': 5,
                'mandante_amarelos': 2, 'visitante_amarelos': 3,
                'mandante_vermelhos': 0, 'visitante_vermelhos': 0
            }
        },
        {
            'nome': 'Cruzeiro vs Santos (Visitante Forte)',
            'features': {
                'mandante_chutes': 10, 'visitante_chutes': 18,
                'mandante_chutes_gol': 2, 'visitante_chutes_gol': 7,
                'mandante_posse': 35, 'visitante_posse': 65,
                'mandante_faltas': 18, 'visitante_faltas': 12,
                'mandante_escanteios': 2, 'visitante_escanteios': 7,
                'mandante_amarelos': 3, 'visitante_amarelos': 1,
                'mandante_vermelhos': 0, 'visitante_vermelhos': 0
            }
        }
    ]
    
    # Fazer predições
    resultados = []
    for partida in partidas:
        pred = preditor.prever(partida['features'])
        resultados.append({
            'partida': partida['nome'],
            'predicao': pred
        })
    
    # Exibir resultados
    for resultado in resultados:
        print(f"\n🎯 {resultado['partida']}")
        pred = resultado['predicao']
        print(f"   Resultado: {pred['resultado']} (Confiança: {pred['confianca']:.1%})")
        print(f"   Placar: {pred['placar']}")
        print(f"   Escanteios: {pred['escanteios']} | Faltas: {pred['faltas']}")
        print(f"   Probabilidades: {pred['probabilidades']}")
    
    return resultados


# ============================================================================
# EXEMPLO 4: Análise de Sensibilidade
# ============================================================================

def exemplo_4_analise_sensibilidade():
    """Analisa como mudanças em features afetam as predições"""
    print("\n" + "=" * 80)
    print("EXEMPLO 4: Análise de Sensibilidade")
    print("=" * 80)
    
    preditor = exemplo_2_carregar_modelos()
    
    # Cenário base
    cenario_base = {
        'mandante_chutes': 15, 'visitante_chutes': 10,
        'mandante_chutes_gol': 5, 'visitante_chutes_gol': 3,
        'mandante_posse': 55, 'visitante_posse': 45,
        'mandante_faltas': 15, 'visitante_faltas': 15,
        'mandante_escanteios': 5, 'visitante_escanteios': 3,
        'mandante_amarelos': 2, 'visitante_amarelos': 2,
        'mandante_vermelhos': 0, 'visitante_vermelhos': 0
    }
    
    print("\n📊 Cenário Base:")
    pred_base = preditor.prever(cenario_base)
    print(f"   Resultado: {pred_base['resultado']}")
    print(f"   Placar: {pred_base['placar']}")
    
    # Variações: Aumentar posse do mandante
    print("\n📊 Impacto do Aumento de Posse do Mandante:")
    for posse in [45, 55, 65, 75]:
        cenario = cenario_base.copy()
        cenario['mandante_posse'] = posse
        cenario['visitante_posse'] = 100 - posse
        pred = preditor.prever(cenario)
        print(f"   Posse {posse}%: {pred['resultado']} ({pred['placar']}) - Confiança: {pred['confianca']:.1%}")
    
    # Variações: Aumentar chutes do visitante
    print("\n📊 Impacto do Aumento de Chutes do Visitante:")
    for chutes in [5, 10, 15, 20]:
        cenario = cenario_base.copy()
        cenario['visitante_chutes'] = chutes
        pred = preditor.prever(cenario)
        print(f"   {chutes} chutes: {pred['resultado']} ({pred['placar']}) - Confiança: {pred['confianca']:.1%}")


# ============================================================================
# EXEMPLO 5: Gerar Relatório JSON
# ============================================================================

def exemplo_5_relatorio_json():
    """Gera um relatório de predições em formato JSON"""
    print("\n" + "=" * 80)
    print("EXEMPLO 5: Gerar Relatório em JSON")
    print("=" * 80)
    
    preditor = exemplo_2_carregar_modelos()
    
    # Dados da rodada
    rodada = {
        'numero': 30,
        'data': datetime.now().isoformat(),
        'partidas': [
            {
                'id': 1,
                'mandante': 'Flamengo',
                'visitante': 'Botafogo',
                'features': {
                    'mandante_chutes': 20, 'visitante_chutes': 7,
                    'mandante_chutes_gol': 8, 'visitante_chutes_gol': 2,
                    'mandante_posse': 68, 'visitante_posse': 32,
                    'mandante_faltas': 11, 'visitante_faltas': 16,
                    'mandante_escanteios': 7, 'visitante_escanteios': 2,
                    'mandante_amarelos': 1, 'visitante_amarelos': 2,
                    'mandante_vermelhos': 0, 'visitante_vermelhos': 0
                }
            },
            {
                'id': 2,
                'mandante': 'São Paulo',
                'visitante': 'Palmeiras',
                'features': {
                    'mandante_chutes': 16, 'visitante_chutes': 14,
                    'mandante_chutes_gol': 5, 'visitante_chutes_gol': 5,
                    'mandante_posse': 54, 'visitante_posse': 46,
                    'mandante_faltas': 14, 'visitante_faltas': 13,
                    'mandante_escanteios': 5, 'visitante_escanteios': 4,
                    'mandante_amarelos': 2, 'visitante_amarelos': 2,
                    'mandante_vermelhos': 0, 'visitante_vermelhos': 0
                }
            }
        ]
    }
    
    # Gerar predições
    relatorio = {
        'titulo': 'Rodada ' + str(rodada['numero']),
        'data_geracao': rodada['data'],
        'partidas': []
    }
    
    for partida in rodada['partidas']:
        pred = preditor.prever(partida['features'])
        relatorio['partidas'].append({
            'id': partida['id'],
            'mandante': partida['mandante'],
            'visitante': partida['visitante'],
            'predicao': {
                'resultado': pred['resultado'],
                'placar': pred['placar'],
                'confianca': f"{pred['confianca']:.1%}",
                'probabilidades': pred['probabilidades'],
                'escanteios': pred['escanteios'],
                'faltas': pred['faltas']
            }
        })
    
    # Salvar relatório
    with open('relatorio_predicoes.json', 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print("\n✅ Relatório salvo em 'relatorio_predicoes.json'")
    print("\nConteúdo do Relatório:")
    print(json.dumps(relatorio, ensure_ascii=False, indent=2))


# ============================================================================
# EXEMPLO 6: Comparar Modelos
# ============================================================================

def exemplo_6_compare_modelos():
    """Compara as predições de diferentes versões de modelos"""
    print("\n" + "=" * 80)
    print("EXEMPLO 6: Comparar Modelos")
    print("=" * 80)
    
    cenario_teste = {
        'mandante_chutes': 18, 'visitante_chutes': 9,
        'mandante_chutes_gol': 6, 'visitante_chutes_gol': 2,
        'mandante_posse': 62, 'visitante_posse': 38,
        'mandante_faltas': 12, 'visitante_faltas': 16,
        'mandante_escanteios': 6, 'visitante_escanteios': 2,
        'mandante_amarelos': 2, 'visitante_amarelos': 2,
        'mandante_vermelhos': 0, 'visitante_vermelhos': 0
    }
    
    print("\n🎯 Cenário de Teste - Mandante em Vantagem")
    print(f"   Chutes: 18 x 9")
    print(f"   Posse: 62% x 38%")
    
    try:
        preditor = exemplo_2_carregar_modelos()
        pred = preditor.prever(cenario_teste)
        
        print(f"\n📊 Predição do Modelo:")
        print(f"   Resultado: {pred['resultado']}")
        print(f"   Placar: {pred['placar']}")
        print(f"   Confiança: {pred['confianca']:.1%}")
        print(f"   Escanteios: {pred['escanteios']}")
        print(f"   Faltas: {pred['faltas']}")
    except Exception as e:
        print(f"❌ Erro ao carregar modelos: {e}")


# ============================================================================
# MAIN - Executar Todos os Exemplos
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🏆 EXEMPLOS AVANÇADOS - PREDITOR DE FUTEBOL")
    print("=" * 80)
    
    # Executar exemplos
    try:
        # Exemplo 2: Carregar ou treinar modelos
        print("\n1️⃣  Carregando/Treinando modelos...")
        preditor = exemplo_2_carregar_modelos()
        
        # Exemplo 3: Predições em lote
        print("\n2️⃣  Fazendo predições em lote...")
        exemplo_3_predicoes_em_lote()
        
        # Exemplo 4: Análise de sensibilidade
        print("\n3️⃣  Análise de sensibilidade...")
        exemplo_4_analise_sensibilidade()
        
        # Exemplo 5: Gerar relatório JSON
        print("\n4️⃣  Gerando relatório JSON...")
        exemplo_5_relatorio_json()
        
        # Exemplo 6: Comparar modelos
        print("\n5️⃣  Comparando modelos...")
        exemplo_6_compare_modelos()
        
        print("\n" + "=" * 80)
        print("✅ Todos os exemplos executados com sucesso!")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
