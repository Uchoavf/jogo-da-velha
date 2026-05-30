import tkinter as tk
from tkinter import messagebox
import time
import random

class JogoDaVelha:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo da Velha")
        self.jogador_humano = "X"
        self.jogador_ia = "O"
        self.jogador_atual = "X"
        self.nivel = None
        self.inicio = None
        self.botao_grid = []
        self.tabuleiro = [[" "]*3 for _ in range(3)]

        self.frame_config = tk.Frame(self.master)
        self.frame_config.pack()

        tk.Label(self.frame_config, text="Escolha o nível da IA:").pack()
        self.nivel_var = tk.StringVar(value="1")
        tk.Radiobutton(self.frame_config, text="Normal", variable=self.nivel_var, value="1").pack()
        tk.Radiobutton(self.frame_config, text="Difícil", variable=self.nivel_var, value="2").pack()

        tk.Label(self.frame_config, text="Escolha seu símbolo:").pack()
        self.simbolo_var = tk.StringVar(value="X")
        tk.Radiobutton(self.frame_config, text="X (Começa)", variable=self.simbolo_var, value="X").pack()
        tk.Radiobutton(self.frame_config, text="O", variable=self.simbolo_var, value="O").pack()

        tk.Button(self.frame_config, text="Iniciar Jogo", command=self.iniciar_jogo).pack()

    def iniciar_jogo(self):
        self.nivel = int(self.nivel_var.get())
        self.jogador_humano = self.simbolo_var.get()
        self.jogador_ia = "O" if self.jogador_humano == "X" else "X"
        self.jogador_atual = "X"
        self.inicio = time.time()
        self.tabuleiro = [[" "]*3 for _ in range(3)]

        self.frame_config.pack_forget()

        self.frame_jogo = tk.Frame(self.master)
        self.frame_jogo.pack()

        self.botao_grid = []
        for i in range(3):
            linha = []
            for j in range(3):
                btn = tk.Button(self.frame_jogo, text=" ", font=("Arial", 30), width=3, height=1,
                                command=lambda x=i, y=j: self.jogada_humana(x, y))
                btn.grid(row=i, column=j)
                linha.append(btn)
            self.botao_grid.append(linha)

        if self.jogador_ia == "X":
            self.jogada_ia()

    def jogada_humana(self, i, j):
        if self.jogador_atual != self.jogador_humano:
            return

        if self.tabuleiro[i][j] == " ":
            self.tabuleiro[i][j] = self.jogador_humano
            self.botao_grid[i][j].config(text=self.jogador_humano, state="disabled")
            if self.verifica_vencedor(self.jogador_humano):
                self.fim_de_jogo(f"Parabéns! Você ({self.jogador_humano}) venceu!")
                return
            elif self.tabuleiro_cheio():
                self.fim_de_jogo("Empate!")
                return
            self.jogador_atual = self.jogador_ia
            self.master.after(500, self.jogada_ia)  # Delay para a IA jogar

    def jogada_ia(self):
        if self.jogador_atual != self.jogador_ia:
            return

        if self.nivel == 1:
            i, j = self.jogada_ia_normal()
        else:
            i, j = self.jogada_ia_dificil()

        self.tabuleiro[i][j] = self.jogador_ia
        self.botao_grid[i][j].config(text=self.jogador_ia, state="disabled")

        if self.verifica_vencedor(self.jogador_ia):
            self.fim_de_jogo(f"A IA ({self.jogador_ia}) venceu! Tente novamente.")
            return
        elif self.tabuleiro_cheio():
            self.fim_de_jogo("Empate!")
            return

        self.jogador_atual = self.jogador_humano

    def jogada_ia_normal(self):
        possiveis = [(i, j) for i in range(3) for j in range(3) if self.tabuleiro[i][j] == " "]
        return random.choice(possiveis)

    def minimax(self, tabuleiro, jogador):
        if self.verifica_vencedor_no_tab(tabuleiro, self.jogador_ia):
            return {'pontuacao': 1}
        elif self.verifica_vencedor_no_tab(tabuleiro, self.jogador_humano):
            return {'pontuacao': -1}
        elif all(all(c != " " for c in linha) for linha in tabuleiro):
            return {'pontuacao': 0}

        movimentos = []

        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == " ":
                    tabuleiro[i][j] = jogador
                    if jogador == self.jogador_ia:
                        resultado = self.minimax(tabuleiro, self.jogador_humano)
                        movimentos.append({'i': i, 'j': j, 'pontuacao': resultado['pontuacao']})
                    else:
                        resultado = self.minimax(tabuleiro, self.jogador_ia)
                        movimentos.append({'i': i, 'j': j, 'pontuacao': resultado['pontuacao']})
                    tabuleiro[i][j] = " "

        if jogador == self.jogador_ia:
            max_mov = max(movimentos, key=lambda x: x['pontuacao'])
            return max_mov
        else:
            min_mov = min(movimentos, key=lambda x: x['pontuacao'])
            return min_mov

    def jogada_ia_dificil(self):
        mov = self.minimax([linha[:] for linha in self.tabuleiro], self.jogador_ia)
        return mov['i'], mov['j']

    def verifica_vencedor(self, jogador):
        return self.verifica_vencedor_no_tab(self.tabuleiro, jogador)

    def verifica_vencedor_no_tab(self, tab, jogador):
        for linha in tab:
            if all(s == jogador for s in linha):
                return True
        for col in range(3):
            if all(tab[linha][col] == jogador for linha in range(3)):
                return True
        if all(tab[i][i] == jogador for i in range(3)):
            return True
        if all(tab[i][2 - i] == jogador for i in range(3)):
            return True
        return False

    def tabuleiro_cheio(self):
        return all(all(celula != " " for celula in linha) for linha in self.tabuleiro)

    def fim_de_jogo(self, mensagem):
        fim = time.time()
        tempo_jogo = fim - self.inicio
        jogar_novamente = messagebox.askyesno(
            "Fim de jogo",
            f"{mensagem}\nTempo total de jogo: {tempo_jogo:.2f} segundos.\n\nDeseja jogar novamente?"
        )
        if jogar_novamente:
            self.reiniciar_jogo()
        else:
            self.master.destroy()

    def reiniciar_jogo(self):
        self.frame_jogo.pack_forget()
        self.jogador_atual = "X"
        self.tabuleiro = [[" "]*3 for _ in range(3)]
        self.frame_config.pack()

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoDaVelha(root)
    root.mainloop()