#!/usr/bin/env python3
"""
🎯 GUIA RÁPIDO - PREDITOR POR TIME
Como usar o novo programa interativo!
"""

print("""

╔════════════════════════════════════════════════════════════════════════════╗
║                                                                            ║
║           🏆 COMO USAR O PREDITOR INTERATIVO DE TIMES 🏆                 ║
║                                                                            ║
╚════════════════════════════════════════════════════════════════════════════╝


🚀 COMO EXECUTAR

    $ python preditor_por_time.py


📋 FUNCIONAMENTO

O programa oferece um menu com 3 opções:

    1 - Fazer Nova Predição
    2 - Ver Estatísticas de um Time
    3 - Comparar Dois Times


═══════════════════════════════════════════════════════════════════════════════
OPÇÃO 1: FAZER NOVA PREDIÇÃO
═══════════════════════════════════════════════════════════════════════════════

Passo 1: Digite "1" no menu principal

Passo 2: Escolha o time MANDANTE (em casa)
         • Será mostrada uma lista numerada de 1 a 46
         • Digite o número do time desejado
         • Exemplo: 21 (Flamengo)

Passo 3: Escolha o time VISITANTE (fora de casa)
         • Mesma lista de times
         • Digite um número diferente do mandante
         • Exemplo: 9 (Botafogo-RJ)

Resultado: O programa mostrará:
    ✓ Estatísticas médias de ambos os times
    ✓ Vencedor provável
    ✓ Confiança da predição
    ✓ Placar estimado
    ✓ Escanteios estimados
    ✓ Faltas estimadas
    ✓ Probabilidades completas


═══════════════════════════════════════════════════════════════════════════════
OPÇÃO 2: VER ESTATÍSTICAS DE UM TIME
═══════════════════════════════════════════════════════════════════════════════

Passo 1: Digite "2" no menu principal

Passo 2: Escolha o time
         • Digite o número do time (1-46)
         • Exemplo: 21 (Flamengo)

Resultado: Mostrará estatísticas do time:
    ✓ Como mandante (em casa)
    ✓ Como visitante (fora de casa)
    ✓ Média de chutes, posse, faltas, escanteios, etc.


═══════════════════════════════════════════════════════════════════════════════
OPÇÃO 3: COMPARAR DOIS TIMES
═══════════════════════════════════════════════════════════════════════════════

Passo 1: Digite "3" no menu principal

Passo 2: Escolha o primeiro time
         • Digite o número (1-46)

Passo 3: Escolha o segundo time
         • Digite outro número (1-46)

Resultado: Tabela comparativa com:
    ✓ Chutes
    ✓ Chutes a gol
    ✓ Posse de bola
    ✓ Escanteios
    ✓ Faltas
    ✓ Cartões
    
    O melhor em cada métrica terá um ✓


═══════════════════════════════════════════════════════════════════════════════
EXEMPLOS DE USO
═══════════════════════════════════════════════════════════════════════════════

EXEMPLO 1: Predição Clássico Paulista
─────────────────────────────────────────

Menu: 1 (Fazer Nova Predição)
Mandante: 44 (São Paulo)
Visitante: 15 (Corinthians)

Resultado: Predição completa com probabilidades


EXEMPLO 2: Ver Estatísticas do Flamengo
─────────────────────────────────────────

Menu: 2 (Ver Estatísticas)
Time: 21 (Flamengo)

Resultado: 
    🏠 Como Mandante: média de 7 chutes, 60% posse...
    🔙 Como Visitante: média de 5 chutes, 48% posse...


EXEMPLO 3: Comparar Palmeiras e São Paulo
──────────────────────────────────────────

Menu: 3 (Comparar)
Primeiro: 34 (Palmeiras)
Segundo: 44 (São Paulo)

Resultado: Tabela com estatísticas lado a lado


═══════════════════════════════════════════════════════════════════════════════
LISTA COMPLETA DE TIMES (46 times)
═══════════════════════════════════════════════════════════════════════════════

 1. America-MG              24. Goias
 2. America-RN              25. Gremio
 3. Athletico-PR            26. Gremio Prudente
 4. Atletico-GO             27. Guarani
 5. Atletico-MG             28. Internacional
 6. Avai                    29. Ipatinga
 7. Bahia                   30. Joinville
 8. Barueri                 31. Juventude
 9. Botafogo-RJ             32. Mirassol
10. Bragantino              33. Nautico
11. Brasiliense             34. Palmeiras
12. CSA                     35. Parana
13. Ceara                   36. Paysandu
14. Chapecoense             37. Ponte Preta
15. Corinthians             38. Portuguesa
16. Coritiba                39. Santa Cruz
17. Criciuma                40. Santo Andre
18. Cruzeiro                41. Santos
19. Cuiaba                  42. Sao Caetano
20. Figueirense             43. Sao Paulo
21. Flamengo                44. Sport
22. Fluminense              45. Vasco
23. Fortaleza               46. Vitoria


═══════════════════════════════════════════════════════════════════════════════
INTERPRETANDO OS RESULTADOS
═══════════════════════════════════════════════════════════════════════════════

VENCEDOR:
    🥇 Mandante = Time que joga em casa
    🔙 Visitante = Time que joga fora
    🤝 Empate = Ambos têm chances iguais

CONFIANÇA:
    80-100% = Muito provável
    60-80%  = Provável
    50-60%  = Incerto
    <50%    = Muito incerto

PLACAR:
    Estimativa baseada em desempenho histórico
    Exemplo: "2 x 1" = Mandante 2 gols, Visitante 1 gol

PROBABILIDADES:
    Gráfico com % para cada resultado possível
    Total sempre = 100%


═══════════════════════════════════════════════════════════════════════════════
DICAS
═══════════════════════════════════════════════════════════════════════════════

✓ Os dados usados são baseados em histórico completo do time
✓ Quanto mais partidas na história, mais preciso o resultado
✓ Times novos podem ter menos dados históricos
✓ Use a comparação para entender melhor os times
✓ Compare as predições com odds de casas de apostas

❌ NÃO é uma garantia, apenas uma estimativa
❌ Futebol é imprevisível, pode sempre haver surpresas


═══════════════════════════════════════════════════════════════════════════════

🎯 COMECE AGORA!

    $ python preditor_por_time.py

E escolha um dos times para começar!

Boa sorte! ⚽

═══════════════════════════════════════════════════════════════════════════════
""")
