#!/usr/bin/env python3
"""
🏆 PREDITOR INTERATIVO DE PARTIDAS
Escolha os times e veja a predição!

Este script é apenas uma interface de linha de comando. Todo o cálculo de
features (forma recente + rating Elo) e as predições vêm do mesmo motor
usado no treinamento (PreditorFutebol, em preditor_futebol.py), garantindo
que a predição de um confronto futuro use exatamente o mesmo tipo de dado
visto pelo modelo durante o treino.
"""

import warnings
warnings.filterwarnings('ignore')

from preditor_futebol import PreditorFutebol


class PreditorInterativo:
    """Preditor interativo com seleção de times"""

    def __init__(self):
        self.preditor = PreditorFutebol()
        self.times = []

    def carregar_dados(self):
        """Carrega os modelos treinados (e o estado atual dos times)"""
        print("\n📥 Carregando dados...")
        try:
            self.preditor.carregar_modelos('modelos_futebol.pkl')
        except FileNotFoundError:
            print("⚠️  Modelos não encontrados. Execute 'python preditor_futebol.py' primeiro!")
            return False

        self.times = self.preditor.times
        print(f"✅ {len(self.times)} times carregados")
        print("✅ Modelos carregados com sucesso!")
        return True

    def mostrar_times(self):
        """Mostra lista de times formatada"""
        print("\n" + "=" * 80)
        print("⚽ TIMES DISPONÍVEIS")
        print("=" * 80)
        for i, time in enumerate(self.times, 1):
            print(f"  {i:2d}. {time}")
        print("=" * 80)

    def selecionar_time(self, tipo="mandante"):
        """Permite selecionar um time"""
        while True:
            try:
                self.mostrar_times()
                numero = int(input(f"\n🎯 Escolha o número do time {tipo}: "))
                if 1 <= numero <= len(self.times):
                    return self.times[numero - 1]
                else:
                    print(f"❌ Número inválido! Digite entre 1 e {len(self.times)}")
            except ValueError:
                print("❌ Digite um número válido!")

    def obter_stats_time(self, time):
        """Retorna o estado atual (forma recente + Elo) de um time"""
        return self.preditor.estado_atual.get(time)

    def calcular_features(self, mandante, visitante):
        """Delegado ao motor de predição (garante consistência com o treino)"""
        return self.preditor.calcular_features_confronto(mandante, visitante)

    def fazer_predicao(self, features):
        """Delegado ao motor de predição"""
        return self.preditor.prever(features)

    def exibir_predicao(self, mandante, visitante, features, resultado):
        """Exibe a predição de forma formatada"""
        stats_m = self.obter_stats_time(mandante)
        stats_v = self.obter_stats_time(visitante)

        print("\n" + "=" * 80)
        print(f"🎯 PREDIÇÃO: {mandante.upper()} x {visitante.upper()}")
        print("=" * 80)

        print(f"\n📊 FORMA ATUAL DOS TIMES (últimos jogos):")
        print(f"\n  {mandante} (Rating Elo: {stats_m['elo']:.0f}):")
        print(f"    • Chutes: {stats_m['chutes_media']:.1f}")
        print(f"    • Chutes a Gol: {stats_m['chutes_gol_media']:.1f}")
        print(f"    • Posse: {stats_m['posse_media']:.1f}%")
        print(f"    • Escanteios: {stats_m['escanteios_media']:.1f}")
        print(f"    • Faltas: {stats_m['faltas_media']:.1f}")
        print(f"    • Gols marcados/sofridos: {stats_m['gols_marcados_media']:.1f} / {stats_m['gols_sofridos_media']:.1f}")
        print(f"    • Forma (pontos últimos 5 jogos): {stats_m['forma_pontos']:.0f}/15")

        print(f"\n  {visitante} (Rating Elo: {stats_v['elo']:.0f}):")
        print(f"    • Chutes: {stats_v['chutes_media']:.1f}")
        print(f"    • Chutes a Gol: {stats_v['chutes_gol_media']:.1f}")
        print(f"    • Posse: {stats_v['posse_media']:.1f}%")
        print(f"    • Escanteios: {stats_v['escanteios_media']:.1f}")
        print(f"    • Faltas: {stats_v['faltas_media']:.1f}")
        print(f"    • Gols marcados/sofridos: {stats_v['gols_marcados_media']:.1f} / {stats_v['gols_sofridos_media']:.1f}")
        print(f"    • Forma (pontos últimos 5 jogos): {stats_v['forma_pontos']:.0f}/15")

        print(f"\n" + "=" * 80)
        print(f"🏆 RESULTADO PREVISTO")
        print("=" * 80)

        # Emoji baseado no resultado
        if resultado['resultado'] == 'Mandante':
            emoji = "🥇"
        elif resultado['resultado'] == 'Visitante':
            emoji = "🔙"
        else:
            emoji = "🤝"

        print(f"\n  {emoji} Vencedor: {resultado['resultado']}")
        print(f"  🎯 Confiança: {resultado['confianca']:.1%}")
        print(f"  📋 Placar Previsto: {resultado['placar']}")
        print(f"  🎲 Escanteios: {resultado['escanteios']}")
        print(f"  📋 Faltas: {resultado['faltas']}")
        print(f"  🟨 Cartões Amarelos: {resultado['amarelos']}")
        print(f"  🟥 Cartões Vermelhos: {resultado['vermelhos']}")

        print(f"\n  📊 Probabilidades Completas:")
        for classe, prob in resultado['probabilidades'].items():
            barra = "█" * int(prob * 20)
            print(f"    {classe:12s}: {barra:20s} {prob:6.1%}")

        print("\n" + "=" * 80)

    def executar(self):
        """Executa o programa principal"""
        print("\n" + "=" * 80)
        print("🏆 PREDITOR INTERATIVO DE FUTEBOL")
        print("=" * 80)

        # Carregar dados
        if not self.carregar_dados():
            return

        while True:
            print("\n" + "=" * 80)
            print("O QUE DESEJA FAZER?")
            print("=" * 80)
            print("  1 - Fazer Nova Predição")
            print("  2 - Ver Estatísticas de um Time")
            print("  3 - Comparar Dois Times")
            print("  4 - Simular Múltiplos Jogos (Monte Carlo)")
            print("  0 - Sair")

            escolha = input("\nEscolha uma opção: ").strip()

            if escolha == "1":
                self.fazer_nova_predicao()
            elif escolha == "2":
                self.ver_stats_time()
            elif escolha == "3":
                self.comparar_times()
            elif escolha == "4":
                self.simular_multiplos_jogos()
            elif escolha == "0":
                print("\n👋 Até logo!")
                break
            else:
                print("❌ Opção inválida!")

    def fazer_nova_predicao(self):
        """Fluxo completo de nova predição"""
        print("\n🏟️  SELEÇÃO DOS TIMES")
        print("═" * 80)

        mandante = self.selecionar_time("MANDANTE (em casa)")
        print(f"✅ Mandante selecionado: {mandante}")

        visitante = self.selecionar_time("VISITANTE (fora de casa)")
        print(f"✅ Visitante selecionado: {visitante}")

        if mandante == visitante:
            print("\n❌ Os times devem ser diferentes!")
            return

        print("\n⏳ Calculando predição...")
        features = self.calcular_features(mandante, visitante)

        if features is None:
            print("\n❌ Não foi possível calcular as estatísticas dos times!")
            print("   Tente com times diferentes.")
            return

        resultado = self.fazer_predicao(features)
        self.exibir_predicao(mandante, visitante, features, resultado)

        input("\nPressione ENTER para continuar...")

    def ver_stats_time(self):
        """Mostra estatísticas (forma atual) de um time"""
        time = self.selecionar_time("para ver estatísticas")

        stats = self.obter_stats_time(time)

        if stats is None:
            print(f"\n❌ Estatísticas não encontradas para {time}")
            return

        print("\n" + "=" * 80)
        print(f"📊 ESTATÍSTICAS: {time.upper()}")
        print("=" * 80)

        print(f"\n📈 FORMA ATUAL (últimos jogos):")
        print(f"  • Rating Elo: {stats['elo']:.0f}")
        print(f"  • Chutes médios: {stats['chutes_media']:.1f}")
        print(f"  • Chutes a gol: {stats['chutes_gol_media']:.1f}")
        print(f"  • Posse de bola: {stats['posse_media']:.1f}%")
        print(f"  • Escanteios: {stats['escanteios_media']:.1f}")
        print(f"  • Faltas: {stats['faltas_media']:.1f}")
        print(f"  • Cartões amarelos: {stats['amarelos_media']:.1f}")
        print(f"  • Cartões vermelhos: {stats['vermelhos_media']:.1f}")
        print(f"  • Gols marcados: {stats['gols_marcados_media']:.1f}")
        print(f"  • Gols sofridos: {stats['gols_sofridos_media']:.1f}")
        print(f"  • Forma (pontos últimos 5 jogos): {stats['forma_pontos']:.0f}/15")

        print("\n" + "=" * 80)
        input("Pressione ENTER para continuar...")

    def comparar_times(self):
        """Compara dois times lado a lado"""
        print("\n🏆 COMPARAÇÃO DE TIMES")
        time1 = self.selecionar_time("PRIMEIRO")
        time2 = self.selecionar_time("SEGUNDO")

        stats1 = self.obter_stats_time(time1)
        stats2 = self.obter_stats_time(time2)

        if stats1 is None or stats2 is None:
            print("\n❌ Não foi possível comparar os times!")
            return

        print("\n" + "=" * 80)
        print(f"📊 COMPARAÇÃO: {time1.upper()} x {time2.upper()}")
        print("=" * 80)

        print(f"\n{'Métrica':<25} | {time1:<20} | {time2:<20}")
        print("-" * 70)

        metricas = [
            ('Rating Elo', 'elo'),
            ('Chutes', 'chutes_media'),
            ('Chutes a Gol', 'chutes_gol_media'),
            ('Posse %', 'posse_media'),
            ('Escanteios', 'escanteios_media'),
            ('Faltas', 'faltas_media'),
            ('Amarelos', 'amarelos_media'),
            ('Vermelhos', 'vermelhos_media'),
            ('Gols marcados', 'gols_marcados_media'),
            ('Gols sofridos', 'gols_sofridos_media'),
            ('Forma (pts/5 jogos)', 'forma_pontos'),
        ]

        for nome, chave in metricas:
            v1 = stats1.get(chave, 0)
            v2 = stats2.get(chave, 0)

            if v1 > v2:
                s1 = f"{v1:.1f} ✓"
                s2 = f"{v2:.1f}"
            elif v2 > v1:
                s1 = f"{v1:.1f}"
                s2 = f"{v2:.1f} ✓"
            else:
                s1 = f"{v1:.1f}"
                s2 = f"{v2:.1f}"

            print(f"{nome:<25} | {s1:<20} | {s2:<20}")

        print("\n" + "=" * 80)
        input("Pressione ENTER para continuar...")


    def simular_multiplos_jogos(self):
        """Simula o confronto centenas/milhares de vezes (Monte Carlo) e
        mostra a distribuição real de resultados, em vez de uma única
        predição determinística. Times parelhos mostram resultados mais
        variados; um favorito claro vence a maioria das simulações."""
        print("\n🏟️  SELEÇÃO DOS TIMES PARA SIMULAÇÃO")
        print("═" * 80)

        mandante = self.selecionar_time("MANDANTE (em casa)")
        print(f"✅ Mandante selecionado: {mandante}")

        visitante = self.selecionar_time("VISITANTE (fora de casa)")
        print(f"✅ Visitante selecionado: {visitante}")

        if mandante == visitante:
            print("\n❌ Os times devem ser diferentes!")
            return

        try:
            n_simulacoes = int(input("\n🔢 Quantas simulações deseja rodar? (padrão 1000): ").strip() or 1000)
        except ValueError:
            n_simulacoes = 1000

        print(f"\n⏳ Simulando {n_simulacoes} jogos...")
        sim = self.preditor.simular_confronto(mandante, visitante, n_simulacoes=n_simulacoes)

        if sim is None:
            print("\n❌ Não foi possível simular. Tente com times diferentes.")
            return

        print("\n" + "=" * 80)
        print(f"🎲 SIMULAÇÃO MONTE CARLO: {mandante.upper()} x {visitante.upper()} ({sim['n_simulacoes']} jogos)")
        print("=" * 80)

        print(f"\n📊 RESULTADO EM {sim['n_simulacoes']} SIMULAÇÕES:")
        for nome, pct in [
            (f"Vitória {mandante}", sim['pct_vitoria_mandante']),
            ("Empate", sim['pct_empate']),
            (f"Vitória {visitante}", sim['pct_vitoria_visitante']),
        ]:
            barra = "█" * int(pct / 5)
            print(f"  {nome:<25}: {barra:20s} {pct:5.1f}%")

        print(f"\n⚽ Média de gols simulada: {mandante} {sim['gols_mandante_medio']:.2f} x {sim['gols_visitante_medio']:.2f} {visitante}")

        print(f"\n🏆 PLACARES MAIS FREQUENTES:")
        for placar, cont, pct in sim['placares_mais_comuns']:
            print(f"  {placar:<10} — {cont:5d} vezes ({pct:4.1f}%)")

        print(f"\n🎲 ESCANTEIOS (média simulada: {sim['escanteios_medio']:.1f}):")
        for qtd, cont, pct in sim['escanteios_mais_comuns']:
            print(f"  {qtd:2d} escanteios — {cont:5d} vezes ({pct:4.1f}%)")

        print(f"\n📋 Faltas (média simulada): {sim['faltas_medio']:.1f}")

        print(f"\n🟨 CARTÕES AMARELOS (média simulada: {sim['amarelos_medio']:.1f}):")
        for qtd, cont, pct in sim['amarelos_mais_comuns']:
            print(f"  {qtd:2d} amarelos — {cont:5d} vezes ({pct:4.1f}%)")

        print(f"\n🟥 Cartões vermelhos (média simulada): {sim['vermelhos_medio']:.2f}"
              f" | chance de pelo menos 1 vermelho: {sim['pct_pelo_menos_1_vermelho']:.1f}%")

        print("\n" + "=" * 80)
        input("Pressione ENTER para continuar...")


def main():
    """Função principal"""
    preditor = PreditorInterativo()
    preditor.executar()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()

