import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox

import telaEleicoes


class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Criação de Eleições')

        # --- limpar widgets antigos ---
        for widget in self.janela.winfo_children():
            widget.destroy()

        # --- bind ESC para voltar ---
        self.janela.bind('<Escape>', lambda e: self.voltarEleicoes())

        # -------- título topo --------
        lbl_topo = tb.Label(
            self.janela,
            text="Criar Eleição",
            font=("Arial", 35, "bold")
        )
        lbl_topo.pack(pady=15)

        # -------- formulário --------
        frm = tb.Frame(self.janela, padding=20)
        frm.pack(pady=10)

        tb.Label(frm, text="Título:", font=("Arial", 20)).pack(pady=(20, 5))
        self.entry_titulo = tb.Entry(frm, width=40)
        self.entry_titulo.pack(pady=10)

        tb.Label(frm, text="Data de Início:", font=("Arial", 20)).pack()
        self.entry_inicio = tb.DateEntry(frm, dateformat="%d-%m-%Y", bootstyle=INFO, width=36)
        self.entry_inicio.pack(pady=10)

        tb.Label(frm, text="Data de Encerramento:", font=("Arial", 20)).pack()
        self.entry_fim = tb.DateEntry(frm, dateformat="%d-%m-%Y", bootstyle=INFO, width=36)
        self.entry_fim.pack(pady=10)

        # -------- botão salvar --------
        self.btn_salvar = tb.Button(self.janela,text="Salvar",bootstyle="success-outline",width=20,command=self.salvarEleicao)
        self.btn_salvar.pack(pady=20)

        # -------- seção chapas --------
        self.frm_chapas = tb.Frame(self.janela, padding=10)
        self.frm_chapas.pack(pady=20)

        self.chapas = []
        self.add_chapa_btn = self.criar_card_adicionar()
        self.add_chapa_btn.grid(row=0, column=0, padx=10)

    # -------- funções --------
    def voltarEleicoes(self):
        
        telaEleicoes.iniciarTela(self.janela)

    def salvarEleicao(self):
        titulo = self.entry_titulo.get().strip()
        data_ini = self.entry_inicio.entry.get()
        data_fim = self.entry_fim.entry.get()

        if not titulo:
            messagebox.showerror("Erro", "O título da eleição é obrigatório!")
            return

        messagebox.showinfo("Sucesso", f"Eleição '{titulo}' salva!\n{data_ini} - {data_fim}")
        self.voltarEleicoes()

    def criar_card_adicionar(self):
        
        frm_card = tb.Frame(self.frm_chapas, bootstyle="light", width=300, height=300)
        frm_card.pack_propagate(False)

        lbl = tb.Label(frm_card, text="Adicionar Chapa", font=("Arial", 18, "bold"))
        lbl.pack(pady=(50, 20))

        btn = tb.Button(frm_card,text="+",bootstyle="dark",width=10)
        btn.pack()

        return frm_card

    def criar_card_chapa(self, nome):
        frm_card = tb.Frame(self.frm_chapas, bootstyle="light", width=300, height=300)
        frm_card.pack_propagate(False)

        lbl = tb.Label(frm_card, text=nome, font=("Arial", 18, "bold"))
        lbl.pack(expand=True)

        return frm_card


    def salvar_chapa(self, nome):
        
        nova = self.criar_card_chapa(nome)
        col = len(self.chapas)
        nova.grid(row=0, column=col, padx=10)

        self.chapas.append(nova)
        self.add_chapa_btn.grid(row=0, column=len(self.chapas), padx=10)


# -------- iniciarTela --------
def iniciarTela(master=None):
    if master is None:
        app = tb.Window()
        Tela(app)
        app.mainloop()
    else:
        Tela(master)
