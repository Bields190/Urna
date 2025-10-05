import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import telaEleicoes, telaChapas
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_eleicao  # type: ignore


class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Criar Eleição")

        # limpar tela
        for widget in self.janela.winfo_children():
            widget.destroy()

        self.control = c_eleicao.Control(self)

        # bind ESC para voltar
        self.janela.bind("<Escape>", lambda e: self.voltarEleicoes())

        tb.Label(self.janela, text="Criar Eleição", font=("Arial", 35, "bold")).pack(
            pady=15
        )

        frm = tb.Frame(self.janela, padding=20)
        frm.pack(pady=10)

        # ---- Campos da Eleição ----
        tb.Label(frm, text="Título:", font=("Arial", 20)).pack(pady=(20, 5))
        self.entry_titulo = tb.Entry(frm, width=40)
        self.entry_titulo.pack(pady=10)

        tb.Label(frm, text="Data de Início:", font=("Arial", 20)).pack()
        self.entry_inicio = tb.DateEntry(
            frm, dateformat="%d-%m-%Y", bootstyle=INFO, width=36
        )
        self.entry_inicio.pack(pady=10)

        tb.Label(frm, text="Data de Encerramento:", font=("Arial", 20)).pack()
        self.entry_fim = tb.DateEntry(
            frm, dateformat="%d-%m-%Y", bootstyle=INFO, width=36
        )
        self.entry_fim.pack(pady=10)

        # ---- Botões ----
        frm_botoes = tb.Frame(self.janela)
        frm_botoes.pack(pady=20)

        # Botão Salvar
        tb.Button(
            frm_botoes,
            text="Salvar Eleição",
            bootstyle="success-outline",
            width=20,
            command=self.salvarEleicao,
        ).pack(side="left", padx=10)

        # Botão Adicionar Chapa
        tb.Button(
            frm_botoes,
            text="Adicionar Chapa",
            bootstyle="info-outline",
            width=20,
            command=self.adicionarChapa,
        ).pack(side="left", padx=10)

    def voltarEleicoes(self):
        telaEleicoes.iniciarTela(self.janela)

    def salvarEleicao(self):
        titulo = self.entry_titulo.get().strip()
        data_inicio = self.entry_inicio.entry.get()
        data_fim = self.entry_fim.entry.get()

        if not titulo:
            messagebox.showerror("Erro", "O título da eleição é obrigatório!")
            return

        self.control.tela.entry1 = self.entry_titulo
        self.control.tela.entry2 = self.entry_inicio
        self.control.tela.entry3 = self.entry_fim

        try:
            sucesso = self.control.adicionar_eleicao()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar eleição: {e}")
            return

        if sucesso:
            messagebox.showinfo("Sucesso", "Eleição criada com sucesso!")
            self.voltarEleicoes()
        else:
            messagebox.showerror("Erro", "Erro ao salvar eleição!")



    def adicionarChapa(self):
        """Abre a tela de gerenciamento de chapas"""
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaChapas.iniciarTela(self.janela)


def iniciarTela(master=None):
    if master is None:
        app = tb.Window(themename="superhero")
        Tela(app)
        app.mainloop()
    else:
        Tela(master)
