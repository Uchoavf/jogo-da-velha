import tkinter as tk
from tkinter import messagebox
import time
import random

class JogoDaVelha:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo da Velha")
        self.master.configure(bg="#2c3e50")
        self.vitorias_jogador = 0
        self.vitorias_ia = 0
        self.empates = 0
        self.jogador_humano = "X"
        self.jogador_ia = "O"
        self.jogador_atual = "X"
        self.modo = None
        self.nivel = None
        self.inicio = None
        self.botao_grid = []
        self.tabuleiro = [[" "]*3 for _ in range(3)]
        self.frame_config = tk.Frame(self.master, bg="#2c3e50")
        self.frame_config.pack()
        self.tela_config()

    def tela_config(self):
        for widget in self.frame_config.winfo_children():
            widget.destroy()

        tk.Label(self.frame_config, text="JOGO DA VELHA", font=("Arial", 20, "bold"),
                 bg="#2c3e50", fg="#ecf0f1").pack(pady=10)

        tk.Label(self.frame_config, text="Modo de jogo:", font=("Arial", 12),
                 bg="#2c3e50", fg="#ecf0f1").pack()
        self.modo_var = tk.StringVar(value="ia")
        tk.Radiobutton(self.frame_config, text="Vs IA", variable=self.modo_var, value="ia",
                       bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e",
                       font=("Arial", 11)).pack()
        tk.Radiobutton(self.frame_config, text="2 Jogadores", variable=self.modo_var, value="2p",
                       bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e",
                       font=("Arial", 11)).pack()

        tk.Label(self.frame_config, text="Nível da IA:", font=("Arial", 12),
                 bg="#2c3e50", fg="#ecf0f1").pack()
        self.nivel_var = tk.StringVar(value="1")
        tk.Radiobutton(self.frame_config, text="Normal", variable=self.nivel_var, value="1",
                       bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e",
                       font=("Arial", 11)).pack()
        tk.Radiobutton(self.frame_config, text="Difícil", variable=self.nivel_var, value="2",
                       bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e",
                       font=("Arial", 11)).pack()

        tk.Label(self.frame_config, text="Seu símbolo:", font=("Arial", 12),
                 bg="#2c3e50", fg="#ecf0f1").pack()
        self.simbolo_var = tk.StringVar(value="X")
        tk.Radiobutton(self.frame_config, text="X (Começa)", variable=self.simbolo_var, value="X",
                       bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e",
                       font=("Arial", 11)).pack()
        tk.Radiobutton(self.frame_config, text="O", variable=self.simbolo_var, value="O",
                       bg="#2c3e50", fg="#ecf0f1", selectcolor="#34495e",
                       font=("Arial", 11)).pack()

        btn = tk.Button(self.frame_config, text="INICIAR", font=("Arial", 14, "bold"),
                        bg="#27ae60", fg="white", padx=20, pady=5,
                        command=self.iniciar_jogo)
        btn.pack(pady=15)

    def iniciar_jogo(self):
        self.modo = self.modo_var.get()
        if self.modo == "ia":
            self.nivel = int(self.nivel_var.get())
            self.jogador_humano = self.simbolo_var.get()
            self.jogador_ia = "O" if self.jogador_humano == "X" else "X"
        self.frame_config.pack_forget()
        self.criar_tabuleiro()

    def criar_tabuleiro(self):
        self.jogador_atual = "X"
        self.inicio = time.time()
        self.tabuleiro = [[" "]*3 for _ in range(3)]

        self.frame_jogo = tk.Frame(self.master, bg="#2c3e50")
        self.frame_jogo.pack()

        self.frame_placar = tk.Frame(self.frame_jogo, bg="#2c3e50")
        self.frame_placar.pack(pady=5)

        self.label_placar = tk.Label(
            self.frame_placar,
            text=self.texto_placar(),
            font=("Arial", 12, "bold"), bg="#2c3e50", fg="#ecf0f1"
        )
        self.label_placar.pack()

        self.label_vez = tk.Label(
            self.frame_jogo, text=self.texto_vez(),
            font=("Arial", 12), bg="#2c3e50", fg="#f1c40f"
        )
        self.label_vez.pack(pady=5)

        self.frame_tab = tk.Frame(self.frame_jogo, bg="#2c3e50")
        self.frame_tab.pack()

        self.botao_grid = []
        for i in range(3):
            linha = []
            for j in range(3):
                btn = tk.Button(
                    self.frame_tab, text=" ", font=("Arial", 28, "bold"),
                    width=3, height=1, bg="#ecf0f1", fg="#2c3e50",
                    activebackground="#bdc3c7",
                    command=lambda x=i, y=j: self.jogada_humana(x, y)
                )
                btn.grid(row=i, column=j, padx=3, pady=3)
                linha.append(btn)
            self.botao_grid.append(linha)

        frame_botoes = tk.Frame(self.frame_jogo, bg="#2c3e50")
        frame_botoes.pack(pady=10)

        btn_desistir = tk.Button(
            frame_botoes, text="Desistir", font=("Arial", 12),
            bg="#e74c3c", fg="white", padx=15,
            command=self.desistir
        )
        btn_desistir.pack(side=tk.LEFT, padx=5)

        btn_menu = tk.Button(
            frame_botoes, text="Menu", font=("Arial", 12),
            bg="#3498db", fg="white", padx=15,
            command=self.voltar_menu
        )
        btn_menu.pack(side=tk.LEFT, padx=5)

        if self.modo == "ia" and self.jogador_ia == "X":
            self.master.after(500, self.jogada_ia)

    def texto_placar(self):
        if self.modo == "ia":
            return f"Você: {self.vitorias_jogador}  |  IA: {self.vitorias_ia}  |  Empates: {self.empates}"
        return f"Jogador X: {self.vitorias_jogador}  |  Jogador O: {self.vitorias_ia}  |  Empates: {self.empates}"

    def texto_vez(self):
        if self.modo == "ia":
            if self.jogador_atual == self.jogador_humano:
                return "Sua vez"
            return "Vez da IA..."
        return f"Vez do Jogador {self.jogador_atual}"

    def atualizar_placar(self):
        self.label_placar.config(text=self.texto_placar())

    def jogada_humana(self, i, j):
        if self.tabuleiro[i][j] != " ":
            return

        if self.modo == "ia" and self.jogador_atual != self.jogador_humano:
            return

        self.tabuleiro[i][j] = self.jogador_atual
        self.botao_grid[i][j].config(text=self.jogador_atual, state="disabled")

        resultado = self.verifica_vencedor(self.jogador_atual)
        if resultado:
            self.destacar_vencedor(resultado)
            if self.modo == "ia":
                if self.jogador_atual == self.jogador_humano:
                    self.vitorias_jogador += 1
                    msg = f"Parabéns! Você ({self.jogador_atual}) venceu!"
                else:
                    self.vitorias_ia += 1
                    msg = f"A IA ({self.jogador_atual}) venceu!"
            else:
                if self.jogador_atual == "X":
                    self.vitorias_jogador += 1
                else:
                    self.vitorias_ia += 1
                msg = f"Jogador {self.jogador_atual} venceu!"
            self.fim_de_jogo(msg)
            return

        if self.tabuleiro_cheio():
            self.empates += 1
            self.fim_de_jogo("Empate!")
            return

        if self.modo == "ia":
            self.jogador_atual = self.jogador_ia
            self.label_vez.config(text=self.texto_vez())
            self.master.after(500, self.jogada_ia)
        else:
            self.jogador_atual = "O" if self.jogador_atual == "X" else "X"
            self.label_vez.config(text=self.texto_vez())

    def desistir(self):
        if self.modo == "ia":
            self.vitorias_ia += 1
            msg = "Você desistiu! A IA venceu."
        else:
            vencedor = "O" if self.jogador_atual == "X" else "X"
            if vencedor == "X":
                self.vitorias_jogador += 1
            else:
                self.vitorias_ia += 1
            msg = f"Jogador {self.jogador_atual} desistiu! Jogador {vencedor} venceu."
        self.fim_de_jogo(msg)

    def voltar_menu(self):
        for widget in self.frame_jogo.winfo_children():
            widget.destroy()
        self.frame_jogo.pack_forget()
        self.frame_config.pack()
        self.tela_config()

    def jogada_ia(self):
        if self.jogador_atual != self.jogador_ia:
            return

        if self.nivel == 1:
            i, j = self.jogada_ia_normal()
        else:
            i, j = self.jogada_ia_dificil()

        self.tabuleiro[i][j] = self.jogador_ia
        self.botao_grid[i][j].config(text=self.jogador_ia, state="disabled")

        resultado = self.verifica_vencedor(self.jogador_ia)
        if resultado:
            self.destacar_vencedor(resultado)
            self.vitorias_ia += 1
            self.fim_de_jogo(f"A IA ({self.jogador_ia}) venceu!")
            return

        if self.tabuleiro_cheio():
            self.empates += 1
            self.fim_de_jogo("Empate!")
            return

        self.jogador_atual = self.jogador_humano
        self.label_vez.config(text=self.texto_vez())

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
            return max(movimentos, key=lambda x: x['pontuacao'])
        else:
            return min(movimentos, key=lambda x: x['pontuacao'])

    def jogada_ia_dificil(self):
        mov = self.minimax([linha[:] for linha in self.tabuleiro], self.jogador_ia)
        return mov['i'], mov['j']

    def verifica_vencedor(self, jogador):
        tab = self.tabuleiro
        for i, linha in enumerate(tab):
            if all(s == jogador for s in linha):
                return [(i, j) for j in range(3)]
        for j in range(3):
            if all(tab[i][j] == jogador for i in range(3)):
                return [(i, j) for i in range(3)]
        if all(tab[i][i] == jogador for i in range(3)):
            return [(i, i) for i in range(3)]
        if all(tab[i][2 - i] == jogador for i in range(3)):
            return [(i, 2 - i) for i in range(3)]
        return None

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

    def destacar_vencedor(self, celulas):
        cor = "#27ae60"
        for i, j in celulas:
            self.botao_grid[i][j].config(bg=cor, fg="white")

    def tabuleiro_cheio(self):
        return all(all(celula != " " for celula in linha) for linha in self.tabuleiro)

    def fim_de_jogo(self, mensagem):
        fim = time.time()
        tempo_jogo = fim - self.inicio
        self.atualizar_placar()
        jogar_novamente = messagebox.askyesno(
            "Fim de jogo",
            f"{mensagem}\nTempo: {tempo_jogo:.2f}s\n\nDeseja jogar novamente?"
        )
        if jogar_novamente:
            self.reiniciar_jogo()
        else:
            self.master.destroy()

    def reiniciar_jogo(self):
        for widget in self.frame_jogo.winfo_children():
            widget.destroy()
        self.frame_jogo.pack_forget()
        self.criar_tabuleiro()

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoDaVelha(root)
    root.mainloop()
