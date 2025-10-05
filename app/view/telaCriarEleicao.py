import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import sys, os
import telaEleicoes

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
        self.chapas_selecionadas = []

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

        # ---- Treeview para mostrar chapas selecionadas ----
        tb.Label(self.janela, text="Chapas Selecionadas:", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        self.tree_chapas = tb.Treeview(self.janela, columns=("chapa",), show="headings", height=8)
        self.tree_chapas.heading("chapa", text="Chapa")
        self.tree_chapas.column("chapa", width=500)
        self.tree_chapas.pack(fill="both", padx=20, pady=10)

    def voltarEleicoes(self):
        telaEleicoes.iniciarTela(self.janela)

    def salvarEleicao(self):
        titulo = self.entry_titulo.get().strip()
        data_inicio = self.entry_inicio.entry.get()
        data_fim = self.entry_fim.entry.get()

        if not titulo:
            messagebox.showerror("Erro", "O título da eleição é obrigatório!")
            return
        if not self.chapas_selecionadas:
            messagebox.showerror("Erro", "Adicione pelo menos uma chapa!")
            return

        self.control.tela.entry1 = self.entry_titulo
        self.control.tela.entry2 = self.entry_inicio
        self.control.tela.entry3 = self.entry_fim
        self.control.tela.chapas = self.chapas_selecionadas  # passar chapas selecionadas

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
        popup = tb.Toplevel(self.janela)
        popup.transient(self.janela)
        popup.grab_set()
        popup.title("Adicionar Chapas à Eleição")
        popup.geometry("600x520")
        popup.resizable(False, False)

        frame = tb.Frame(popup, padding=12)
        frame.pack(fill="both", expand=True)

        tb.Label(frame, text="Selecione a Chapa", font=("Arial", 16, "bold")).pack(pady=(10, 12))

        # carregar chapas do BD
        try:
            import c_chapas  # type: ignore
            chapas_bd = c_chapas.Control().listar_chapas()
            lista_chapas = [f"{c[0]} - {c[1]}" for c in chapas_bd] if chapas_bd else ["Nenhuma chapa cadastrada"]
        except Exception as e:
            print(f"[telaCriarEleicao] Erro ao carregar chapas: {e}")
            lista_chapas = ["Erro ao carregar chapas"]

        sel_var = tb.StringVar()
        cbx = tb.Combobox(frame, values=lista_chapas, textvariable=sel_var, state="readonly", width=50)
        if lista_chapas and lista_chapas[0] not in ["Nenhuma chapa cadastrada", "Erro ao carregar chapas"]:
            cbx.current(0)
        cbx.pack(pady=(5, 10))

        tb.Label(frame, text="Chapas Selecionadas:", font=("Arial", 12, "bold")).pack(pady=(10, 4))

        tree_popup = tb.Treeview(frame, columns=("chapa",), show="headings", height=8)
        tree_popup.heading("chapa", text="Chapa")
        tree_popup.column("chapa", width=500)
        tree_popup.pack(fill="both", padx=6, pady=6)

        def adicionar_local():
            chapa = sel_var.get()
            if chapa in ["Nenhuma chapa cadastrada", "Erro ao carregar chapas"]:
                tb.messagebox.showerror("Erro", "Selecione uma chapa válida!")
                return
            if chapa in self.chapas_selecionadas:
                tb.messagebox.showwarning("Aviso", "Chapa já adicionada!")
                return
            # adicionar à lista principal e aos Treeviews
            self.chapas_selecionadas.append(chapa)
            tree_popup.insert("", "end", values=(chapa,))
            self.tree_chapas.insert("", "end", values=(chapa,))
            tb.messagebox.showinfo("Sucesso", "Chapa adicionada!")

        # botão dentro do popup para adicionar chapa
        tb.Button(frame, text="Adicionar Chapa", bootstyle="success", command=adicionar_local).pack(pady=5)
        tb.Button(frame, text="Fechar", bootstyle="secondary", command=popup.destroy).pack(pady=6)


def iniciarTela(master=None):
    if master is None:
        app = tb.Window(themename="superhero")
        Tela(app)
        app.mainloop()
    else:
        Tela(master)
