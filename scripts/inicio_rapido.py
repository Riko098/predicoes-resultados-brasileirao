#!/usr/bin/env python3
"""
⚡ GUIA DE INÍCIO RÁPIDO - PREDITOR DE FUTEBOL

Execute este script para começar em segundos!
"""

import os
import sys
from pathlib import Path

def verificar_ambiente():
    """Verifica se o ambiente está pronto"""
    print("=" * 80)
    print("⚡ VERIFICAÇÃO DO AMBIENTE")
    print("=" * 80)
    
    # Verificar Python
    print(f"✅ Python: {sys.version.split()[0]}")
    
    # Verificar se está no diretório correto
    arquivos_necessarios = [
        'campeonato-brasileiro-full.csv',
        'campeonato-brasileiro-estatisticas-full.csv',
        'campeonato-brasileiro-gols.csv',
        'campeonato-brasileiro-cartoes.csv'
    ]
    
    print("\n📂 Verificando arquivos de dados...")
    todos_presentes = True
    for arquivo in arquivos_necessarios:
        if os.path.exists(arquivo):
            print(f"   ✅ {arquivo}")
        else:
            print(f"   ❌ {arquivo} - NÃO ENCONTRADO")
            todos_presentes = False
    
    if not todos_presentes:
        print("\n⚠️  Alguns arquivos não foram encontrados!")
        print("   Certifique-se de estar no diretório com os dados CSV.")
        return False
    
    # Verificar dependências
    print("\n📦 Verificando dependências...")
    dependencias = ['pandas', 'numpy', 'sklearn', 'xgboost']
    todas_ok = True
    
    for dep in dependencias:
        try:
            __import__(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep} - NÃO INSTALADO")
            todas_ok = False
    
    if not todas_ok:
        print("\n⚠️  Instale as dependências com:")
        print("   pip install -r requirements.txt")
        return False
    
    print("\n✅ Ambiente pronto para usar!")
    return True


def menu_principal():
    """Exibe o menu principal"""
    print("\n" + "=" * 80)
    print("🏆 PREDITOR DE FUTEBOL - CAMPEONATO BRASILEIRO")
    print("=" * 80)
    
    opcoes = {
        '1': ('Treinar Modelos e Fazer Predições', executar_predicoes),
        '2': ('Ver Exemplos Avançados', executar_exemplos),
        '3': ('Ler Documentação', ler_documentacao),
        '4': ('Abrir Notebook Jupyter', abrir_notebook),
        '0': ('Sair', sair)
    }
    
    print("\nO que você deseja fazer?\n")
    for key, (desc, _) in opcoes.items():
        print(f"  {key} - {desc}")
    
    escolha = input("\nEscolha uma opção (0-4): ").strip()
    
    if escolha in opcoes:
        _, funcao = opcoes[escolha]
        funcao()
    else:
        print("❌ Opção inválida!")
        menu_principal()


def executar_predicoes():
    """Executa o script principal de predições"""
    print("\n" + "=" * 80)
    print("🚀 EXECUTANDO PREDIÇÕES")
    print("=" * 80 + "\n")
    
    try:
        os.system('python preditor_futebol.py')
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")
    
    input("\nPressione ENTER para continuar...")
    menu_principal()


def executar_exemplos():
    """Executa os exemplos avançados"""
    print("\n" + "=" * 80)
    print("📚 EXEMPLOS AVANÇADOS")
    print("=" * 80 + "\n")
    
    try:
        os.system('python exemplos_avancados.py')
    except Exception as e:
        print(f"❌ Erro ao executar: {e}")
    
    input("\nPressione ENTER para continuar...")
    menu_principal()


def ler_documentacao():
    """Mostra a documentação"""
    print("\n" + "=" * 80)
    print("📖 DOCUMENTAÇÃO")
    print("=" * 80)
    
    opcoes = {
        '1': ('README.md - Visão Geral', 'README.md'),
        '2': ('GUIA_INTERPRETACAO.md - Como Entender Resultados', 'GUIA_INTERPRETACAO.md'),
        '3': ('Legenda.txt - Dicionário de Dados', 'Legenda.txt'),
        '0': ('Voltar', None)
    }
    
    print("\nQual documentação você deseja ler?\n")
    for key, (desc, _) in opcoes.items():
        print(f"  {key} - {desc}")
    
    escolha = input("\nEscolha uma opção: ").strip()
    
    if escolha == '0':
        menu_principal()
        return
    
    if escolha in opcoes and opcoes[escolha][1]:
        arquivo = opcoes[escolha][1]
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                conteudo = f.read()
            
            print("\n" + "=" * 80)
            print(conteudo)
            print("=" * 80)
        except FileNotFoundError:
            print(f"❌ Arquivo {arquivo} não encontrado!")
    else:
        print("❌ Opção inválida!")
    
    input("\nPressione ENTER para continuar...")
    menu_principal()


def abrir_notebook():
    """Abre o Jupyter Notebook"""
    print("\n" + "=" * 80)
    print("📓 NOTEBOOK JUPYTER")
    print("=" * 80 + "\n")
    
    if not os.path.exists('predicao_futebol.ipynb'):
        print("❌ Arquivo predicao_futebol.ipynb não encontrado!")
        input("\nPressione ENTER para continuar...")
        menu_principal()
        return
    
    print("🚀 Abrindo Jupyter Notebook...")
    print("   Comando: jupyter notebook predicao_futebol.ipynb\n")
    
    try:
        os.system('jupyter notebook predicao_futebol.ipynb')
    except Exception as e:
        print(f"❌ Erro ao abrir Jupyter: {e}")
        print("\n💡 Dica: Você pode executar manualmente com:")
        print("   jupyter notebook predicao_futebol.ipynb")
    
    menu_principal()


def sair():
    """Sair do programa"""
    print("\n" + "=" * 80)
    print("👋 Até logo!")
    print("=" * 80 + "\n")
    sys.exit(0)


def introducao():
    """Exibe a introdução"""
    print("""
    
    ╔════════════════════════════════════════════════════════════════════════════╗
    ║                                                                            ║
    ║        🏆  PREDITOR DE RESULTADOS DE FUTEBOL                             ║
    ║            Campeonato Brasileiro                                          ║
    ║                                                                            ║
    ║  Usando Machine Learning para Prever:                                    ║
    ║    ⚽ Vencedor da Partida                                                 ║
    ║    🎯 Quantidade de Gols                                                  ║
    ║    🎲 Escanteios                                                          ║
    ║    📋 Faltas                                                              ║
    ║    🟨 Cartões                                                             ║
    ║                                                                            ║
    ╚════════════════════════════════════════════════════════════════════════════╝
    
    """)


def main():
    """Função principal"""
    introducao()
    
    # Verificar ambiente
    if not verificar_ambiente():
        print("\n❌ Ambiente não está pronto.")
        print("   Por favor, instale as dependências:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Mostrar menu
    while True:
        menu_principal()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido. Até logo!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
