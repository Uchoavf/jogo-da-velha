import time
import tkinter as tk
from tkinter import messagebox

import logica

BG = "#2c3e50"
FG = "#ecf0f1"
SELECT = "#34495e"


class JogoDaVelha:
    def __init__(self, master):
        self.master = master
        self.master.title("Jogo da Velha")
        self.master.configure(bg=BG)
        self.vitorias_x = 0
        self.vitorias_o = 0
        self.empates = 0
        self.placar_chave = None
        self.jogador_humano = "X"
        self.jogador_ia = "O"
        self.jogador_atual = "X"
        self.modo = None
        self.nivel = None
        self.inicio = None
        self.fim = True
        self.id_ia = None
        self.botao_grid = []
        self.tabuleiro = logica.novo_tabuleiro()
        self.frame_config = tk.Frame(self.master, bg=BG)
        self.frame_config.pack()
        self.frame_jogo = None
        self.tela_config()

    # ---------- menu ----------
    def _radio(self, texto, var, valor, widgets):
        rb = tk.Radiobutton(self.frame_config, text=texto, variable=var, value=valor,
                            bg=BG, fg=FG, selectcolor=SELECT, font=("Arial", 11))
        rb.pack()
        widgets.append(rb)

    def tela_config(self):
        for widget in self.frame_config.winfo_children():
            widget.destroy()

        tk.Label(self.frame_config, text="JOGO DA VELHA", font=("Arial", 20, "bold"),
                 bg=BG, fg=FG).pack(pady=10)

        self.opcoes_ia = []
        tk.Label(self.frame_config, text="Modo de jogo:", font=("Arial", 12),
                 bg=BG, fg=FG).pack()
        self.modo_var = tk.StringVar(value="ia")
        modo_widgets = []
        self._radio("Vs IA", self.modo_var, "ia", modo_widgets)
        self._radio("2 Jogadores", self.modo_var, "2p", modo_widgets)

        lbl = tk.Label(self.frame_config, text="Nível da IA:", font=("Arial", 12), bg=BG, fg=FG)
        lbl.pack()
        self.opcoes_ia.append(lbl)
        self.nivel_var = tk.StringVar(value="1")
        self._radio("Normal", self.nivel_var, "1", self.opcoes_ia)
        self._radio("Difícil", self.nivel_var, "2", self.opcoes_ia)

        lbl = tk.Label(self.frame_config, text="Seu símbolo:", font=("Arial", 12), bg=BG, fg=FG)
        lbl.pack()
        self.opcoes_ia.append(lbl)
        self.simbolo_var = tk.StringVar(value="X")
        self._radio("X (Começa)", self.simbolo_var, "X", self.opcoes_ia)
        self._radio("O", self.simbolo_var, "O", self.opcoes_ia)

        for rb in modo_widgets:
            rb.config(command=self.atualizar_opcoes_ia)
        self.atualizar_opcoes_ia()

        tk.Button(self.frame_config, text="INICIAR", font=("Arial", 14, "bold"),
                  bg="#27ae60", fg="white", padx=20, pady=5,
                  command=self.iniciar_jogo).pack(pady=15)

    def atualizar_opcoes_ia(self):
        estado = "normal" if self.modo_var.get() == "ia" else "disabled"
        for w in self.opcoes_ia:
            w.config(state=estado)

    def iniciar_jogo(self):
        self.modo = self.modo_var.get()
        if self.modo == "ia":
            self.nivel = int(self.nivel_var.get())
            self.jogador_humano = self.simbolo_var.get()
            self.jogador_ia = "O" if self.jogador_humano == "X" else "X"
        chave = (self.modo, self.jogador_humano if self.modo == "ia" else None)
        if chave != self.placar_chave:
            self.vitorias_x = self.vitorias_o = self.empates = 0
            self.placar_chave = chave
        self.frame_config.pack_forget()
        self.criar_tabuleiro()

    # ---------- tabuleiro ----------
    def criar_tabuleiro(self):
        self.jogador_atual = "X"
        self.inicio = time.monotonic()
        self.fim = False
        self.tabuleiro = logica.novo_tabuleiro()

        self.frame_jogo = tk.Frame(self.master, bg=BG)
        self.frame_jogo.pack()

        self.frame_placar = tk.Frame(self.frame_jogo, bg=BG)
        self.frame_placar.pack(pady=5)
        self.label_placar = tk.Label(self.frame_placar, text=self.texto_placar(),
                                     font=("Arial", 12, "bold"), bg=BG, fg=FG)
        self.label_placar.pack()

        self.label_vez = tk.Label(self.frame_jogo, text=self.texto_vez(),
                                  font=("Arial", 12), bg=BG, fg="#f1c40f")
        self.label_vez.pack(pady=5)

        self.frame_tab = tk.Frame(self.frame_jogo, bg=BG)
        self.frame_tab.pack()

        self.botao_grid = []
        for i in range(3):
            linha = []
            for j in range(3):
                btn = tk.Button(self.frame_tab, text=" ", font=("Arial", 28, "bold"),
                                width=3, height=1, bg=FG, fg=BG,
                                activebackground="#bdc3c7",
                                command=lambda x=i, y=j: self.jogada_humana(x, y))
                btn.grid(row=i, column=j, padx=3, pady=3)
                linha.append(btn)
            self.botao_grid.append(linha)

        frame_botoes = tk.Frame(self.frame_jogo, bg=BG)
        frame_botoes.pack(pady=10)
        tk.Button(frame_botoes, text="Desistir", font=("Arial", 12), bg="#e74c3c",
                  fg="white", padx=15, command=self.desistir).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Menu", font=("Arial", 12), bg="#3498db",
                  fg="white", padx=15, command=self.voltar_menu).pack(side=tk.LEFT, padx=5)

        if self.modo == "ia" and self.jogador_ia == "X":
            self.agendar_ia()

    def texto_placar(self):
        if self.modo == "ia":
            x_humano = self.jogador_humano == "X"
            voce = self.vitorias_x if x_humano else self.vitorias_o
            ia = self.vitorias_o if x_humano else self.vitorias_x
            return f"Você: {voce}  |  IA: {ia}  |  Empates: {self.empates}"
        return (f"Jogador X: {self.vitorias_x}  |  Jogador O: {self.vitorias_o}  |  "
                f"Empates: {self.empates}")

    def texto_vez(self):
        if self.modo == "ia":
            return "Sua vez" if self.jogador_atual == self.jogador_humano else "Vez da IA..."
        return f"Vez do Jogador {self.jogador_atual}"

    def atualizar_placar(self):
        self.label_placar.config(text=self.texto_placar())

    def registrar_vitoria(self, simbolo):
        if simbolo == "X":
            self.vitorias_x += 1
        else:
            self.vitorias_o += 1

    def nome_vencedor(self, simbolo):
        if self.modo == "ia":
            if simbolo == self.jogador_humano:
                return f"Parabéns! Você ({simbolo}) venceu!"
            return f"A IA ({simbolo}) venceu!"
        return f"Jogador {simbolo} venceu!"

    def jogar(self, i, j):
        """Aplica a jogada do jogador atual; retorna True se a partida terminou."""
        simbolo = self.jogador_atual
        self.tabuleiro[i][j] = simbolo
        self.botao_grid[i][j].config(text=simbolo, state="disabled")

        celulas = logica.celulas_vencedoras(self.tabuleiro, simbolo)
        if celulas:
            self.destacar_vencedor(celulas)
            self.registrar_vitoria(simbolo)
            self.fim_de_jogo(self.nome_vencedor(simbolo))
            return True
        if logica.tabuleiro_cheio(self.tabuleiro):
            self.empates += 1
            self.fim_de_jogo("Empate!")
            return True

        self.jogador_atual = "O" if simbolo == "X" else "X"
        self.label_vez.config(text=self.texto_vez())
        return False

    def jogada_humana(self, i, j):
        if self.fim or self.tabuleiro[i][j] != logica.VAZIO:
            return
        if self.modo == "ia" and self.jogador_atual != self.jogador_humano:
            return
        if not self.jogar(i, j) and self.modo == "ia":
            self.agendar_ia()

    def agendar_ia(self):
        self.cancelar_ia()
        self.id_ia = self.master.after(500, self.jogada_ia)

    def cancelar_ia(self):
        if self.id_ia is not None:
            self.master.after_cancel(self.id_ia)
            self.id_ia = None

    def jogada_ia(self):
        self.id_ia = None
        if self.fim or self.jogador_atual != self.jogador_ia:
            return
        if self.nivel == 1:
            i, j = logica.jogada_aleatoria(self.tabuleiro)
        else:
            i, j = logica.melhor_jogada(self.tabuleiro, self.jogador_ia, self.jogador_humano)
        self.jogar(i, j)

    def destacar_vencedor(self, celulas):
        for i, j in celulas:
            self.botao_grid[i][j].config(bg="#27ae60", fg="white")

    # ---------- fluxo ----------
    def desistir(self):
        if self.fim:
            return
        if self.modo == "ia":
            vencedor = self.jogador_ia
            msg = "Você desistiu! A IA venceu."
        else:
            vencedor = "O" if self.jogador_atual == "X" else "X"
            msg = f"Jogador {self.jogador_atual} desistiu! Jogador {vencedor} venceu."
        self.registrar_vitoria(vencedor)
        self.fim_de_jogo(msg)

    def voltar_menu(self):
        self.cancelar_ia()
        self.fim = True
        self.frame_jogo.destroy()
        self.frame_config.pack()
        self.tela_config()

    def fim_de_jogo(self, mensagem):
        self.fim = True
        self.cancelar_ia()
        for linha in self.botao_grid:
            for btn in linha:
                btn.config(state="disabled")
        tempo_jogo = time.monotonic() - self.inicio
        self.atualizar_placar()
        jogar_novamente = messagebox.askyesno(
            "Fim de jogo",
            f"{mensagem}\nTempo: {tempo_jogo:.2f}s\n\nDeseja jogar novamente?"
        )
        if jogar_novamente:
            self.reiniciar_jogo()
        else:
            self.voltar_menu()

    def reiniciar_jogo(self):
        self.frame_jogo.destroy()
        self.criar_tabuleiro()


if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoDaVelha(root)
    root.mainloop()
