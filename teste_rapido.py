#!/usr/bin/env python3
"""
⚡ TESTE RÁPIDO - Validar que tudo funciona
"""

import pandas as pd
import numpy as np
from preditor_futebol import PreditorFutebol

def teste_rapido():
    """Executa um teste rápido do sistema"""
    print("\n" + "=" * 80)
    print("⚡ TESTE RÁPIDO DO SISTEMA")
    print("=" * 80)
    
    try:
        # 1. Criar preditor
        print("\n1️⃣  Criando preditor...")
        preditor = PreditorFutebol()
        print("   ✅ Preditor criado")
        
        # 2. Carregar dados
        print("\n2️⃣  Carregando dados...")
        df_matches, df_stats, _, _ = preditor.carregar_dados()
        print(f"   ✅ {len(df_matches)} partidas carregadas")
        
        # 3. Preparar features
        print("\n3️⃣  Preparando features...")
        df_matches = preditor.preparar_features(df_matches, df_stats)
        print(f"   ✅ Features preparadas para {len(df_matches)} partidas")
        
        # 4. Treinar (sem mostrar warnings)
        print("\n4️⃣  Treinando modelos (pode levar 1-2 minutos)...")
        import warnings
        warnings.filterwarnings('ignore')
        preditor.treinar(df_matches)
        warnings.filterwarnings('default')
        print("   ✅ Modelos treinados com sucesso!")
        
        # 5. Fazer uma predição
        print("\n5️⃣  Fazendo predição de teste...")
        teste = {
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
        
        resultado = preditor.prever(teste)
        
        print("\n" + "=" * 80)
        print("📊 RESULTADO DA PREDIÇÃO")
        print("=" * 80)
        print(f"\n  ⚽ Resultado: {resultado['resultado']}")
        print(f"  🎯 Confiança: {resultado['confianca']:.1%}")
        print(f"  📋 Placar: {resultado['placar']}")
        print(f"  🎲 Escanteios: {resultado['escanteios']}")
        print(f"  📋 Faltas: {resultado['faltas']}")
        print(f"\n  Probabilidades:")
        for classe, prob in resultado['probabilidades'].items():
            print(f"    - {classe}: {prob:.1%}")
        
        # 6. Salvar modelos
        print("\n6️⃣  Salvando modelos...")
        preditor.salvar_modelos('modelos_teste.pkl')
        print("   ✅ Modelos salvos")
        
        print("\n" + "=" * 80)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 80)
        print("\n🎉 O sistema está funcionando perfeitamente!")
        print("\nPróximos passos:")
        print("  1. Execute o Jupyter Notebook para análise completa:")
        print("     python -m jupyter notebook predicao_futebol.ipynb")
        print("\n  2. Ou use o menu interativo:")
        print("     python inicio_rapido.py")
        print("\n  3. Ou execute os exemplos avançados:")
        print("     python exemplos_avancados.py")
        
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


if __name__ == '__main__':
    import sys
    sucesso = teste_rapido()
    sys.exit(0 if sucesso else 1)
