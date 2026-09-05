#!/usr/bin/env python3
"""
⚡ DEMONSTRAÇÃO DO PREDITOR INTERATIVO
Mostra exemplos de predições com diferentes times
"""

from preditor_por_time import PreditorInterativo
import warnings
warnings.filterwarnings('ignore')

def demonstracao():
    """Executa demonstração com vários exemplos"""
    print("\n" + "=" * 80)
    print("🎯 DEMONSTRAÇÃO - PREDITOR INTERATIVO DE TIMES")
    print("=" * 80)
    
    # Carregar preditor
    preditor = PreditorInterativo()
    if not preditor.carregar_dados():
        return
    
    # Exemplos de matchups
    exemplos = [
        ("Flamengo", "Botafogo-RJ", "Clássico Carioca"),
        ("Sao Paulo", "Corinthians", "Clássico Paulista"),
        ("Gremio", "Internacional", "Gre-Nal"),
        ("Palmeiras", "Santos", "Clássico Paulista"),
        ("Vasco", "Fluminense", "Clássico Carioca"),
    ]
    
    for i, (mandante, visitante, nome_classico) in enumerate(exemplos, 1):
        print(f"\n\n{'=' * 80}")
        print(f"EXEMPLO {i}: {nome_classico}")
        print(f"{'=' * 80}")
        
        # Calcular features
        features = preditor.calcular_features(mandante, visitante)
        
        if features is None:
            print(f"❌ Não foi possível fazer predição para {mandante} x {visitante}")
            continue
        
        # Fazer predição
        resultado = preditor.fazer_predicao(features)
        
        # Exibir
        preditor.exibir_predicao(mandante, visitante, features, resultado)
    
    print("\n\n" + "=" * 80)
    print("✅ DEMONSTRAÇÃO CONCLUÍDA!")
    print("=" * 80)
    print("\n🎉 Agora é sua vez!")
    print("\nExecute: python preditor_por_time.py")
    print("\nE escolha seus próprios times para fazer predições!\n")


if __name__ == '__main__':
    try:
        demonstracao()
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
