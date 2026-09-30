"""Regras do jogo da velha e IA, sem dependência de interface gráfica."""
import random

VAZIO = " "
LINHAS_VENCEDORAS = (
    [[(i, j) for j in range(3)] for i in range(3)]
    + [[(i, j) for i in range(3)] for j in range(3)]
    + [[(i, i) for i in range(3)], [(i, 2 - i) for i in range(3)]]
)


def novo_tabuleiro():
    return [[VAZIO] * 3 for _ in range(3)]


def celulas_vencedoras(tab, jogador):
    """Retorna as células da linha vencedora de `jogador`, ou None."""
    for linha in LINHAS_VENCEDORAS:
        if all(tab[i][j] == jogador for i, j in linha):
            return linha
    return None


def tabuleiro_cheio(tab):
    return all(c != VAZIO for linha in tab for c in linha)


def casas_livres(tab):
    return [(i, j) for i in range(3) for j in range(3) if tab[i][j] == VAZIO]


def jogada_aleatoria(tab):
    return random.choice(casas_livres(tab))


def _minimax(tab, jogador, ia, humano, profundidade, alfa, beta):
    if celulas_vencedoras(tab, ia):
        return 10 - profundidade
    if celulas_vencedoras(tab, humano):
        return profundidade - 10
    if tabuleiro_cheio(tab):
        return 0

    if jogador == ia:
        melhor = -100
        for i, j in casas_livres(tab):
            tab[i][j] = jogador
            melhor = max(melhor, _minimax(tab, humano, ia, humano, profundidade + 1, alfa, beta))
            tab[i][j] = VAZIO
            alfa = max(alfa, melhor)
            if alfa >= beta:
                break
        return melhor
    melhor = 100
    for i, j in casas_livres(tab):
        tab[i][j] = jogador
        melhor = min(melhor, _minimax(tab, ia, ia, humano, profundidade + 1, alfa, beta))
        tab[i][j] = VAZIO
        beta = min(beta, melhor)
        if alfa >= beta:
            break
    return melhor


def melhor_jogada(tab, ia, humano):
    """Melhor jogada da IA via minimax com poda alfa-beta (prefere vitórias rápidas)."""
    tab = [linha[:] for linha in tab]
    melhor_pontos, melhor = -100, None
    for i, j in casas_livres(tab):
        tab[i][j] = ia
        pontos = _minimax(tab, humano, ia, humano, 1, -100, 100)
        tab[i][j] = VAZIO
        if pontos > melhor_pontos:
            melhor_pontos, melhor = pontos, (i, j)
    return melhor
