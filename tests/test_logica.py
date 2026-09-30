import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logica as lg  # noqa: E402


def tab_de(texto):
    return [list(linha) for linha in texto.split("/")]


def test_vencedor_linha_coluna_diagonais():
    assert lg.celulas_vencedoras(tab_de("XXX/   /   "), "X") == [(0, 0), (0, 1), (0, 2)]
    assert lg.celulas_vencedoras(tab_de("O  /O  /O  "), "O") == [(0, 0), (1, 0), (2, 0)]
    assert lg.celulas_vencedoras(tab_de("X  / X /  X"), "X") == [(0, 0), (1, 1), (2, 2)]
    assert lg.celulas_vencedoras(tab_de("  X/ X /X  "), "X") == [(0, 2), (1, 1), (2, 0)]
    assert lg.celulas_vencedoras(tab_de("XO /   /   "), "X") is None


def test_tabuleiro_cheio():
    assert not lg.tabuleiro_cheio(lg.novo_tabuleiro())
    assert lg.tabuleiro_cheio(tab_de("XOX/XOO/OXX"))


def test_ia_vence_quando_pode():
    assert lg.melhor_jogada(tab_de("XX /OO /   "), "X", "O") == (0, 2)


def test_ia_bloqueia():
    assert lg.melhor_jogada(tab_de("OO /X  /X  "), "X", "O") == (0, 2)


def test_ia_prefere_vitoria_imediata_a_adiar():
    # X vence agora em (2,2); não deve escolher outra jogada que só vença depois
    assert lg.melhor_jogada(tab_de("XO /OX /   "), "X", "O") == (2, 2)


def _humano_joga_tudo(tab, vez, ia, humano):
    """Explora todas as jogadas do humano; retorna True se a IA nunca perde."""
    if lg.celulas_vencedoras(tab, humano):
        return False
    if lg.celulas_vencedoras(tab, ia) or lg.tabuleiro_cheio(tab):
        return True
    if vez == ia:
        i, j = lg.melhor_jogada(tab, ia, humano)
        tab[i][j] = ia
        ok = _humano_joga_tudo(tab, humano, ia, humano)
        tab[i][j] = lg.VAZIO
        return ok
    for i, j in lg.casas_livres(tab):
        tab[i][j] = humano
        ok = _humano_joga_tudo(tab, ia, ia, humano)
        tab[i][j] = lg.VAZIO
        if not ok:
            return False
    return True


def test_ia_dificil_nunca_perde_comecando_ou_nao():
    assert _humano_joga_tudo(lg.novo_tabuleiro(), "X", "O", "X")
    assert _humano_joga_tudo(lg.novo_tabuleiro(), "X", "X", "O")
