from ttkbootstrap import ttk
import ttkbootstrap as tb
from tkinter import messagebox
import sys, os
from ttkbootstrap import ttk
import ttkbootstrap as tb
from tkinter import messagebox
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_eleicao  # type: ignore
import c_eleicao  # type: ignore

import telaADM, telaCriarEleicao



class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Controle de Eleições")
        self.janela.title("Controle de Eleições")
        self.janela.geometry("1920x1080")

        # --- limpar widgets ---
        for widget in self.janela.winfo_children():
            widget.destroy()

        # bind ESC para voltar
        self.janela.bind("<Escape>", lambda e: self.voltar_tela_adm())

        # controlador

        # --- limpar widgets ---
        for widget in self.janela.winfo_children():
            widget.destroy()

        # bind ESC para voltar
        self.janela.bind("<Escape>", lambda e: self.voltar_tela_adm())

        # controlador
        self.control = c_eleicao.Control(self)

        # layout

        # layout
        self.setup_interface()
        self.renderizar_eleicoes()
        self.renderizar_eleicoes()

    def voltar_tela_adm(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaADM.TelaADM(self.janela)
    def voltar_tela_adm(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaADM.TelaADM(self.janela)

    def setup_interface(self):
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=1)

        ttk.Label(
            self.janela, text="Controle de Eleições", font=("Courier", 20, "bold")
        ).grid(row=1, column=0, pady=(40, 10), padx=(20, 0))

        # Botão criar eleição
        self.btn_criar = ttk.Button(
            self.janela,
            text="+ Criar Nova Eleição",
            bootstyle="primary",
            width=20,
            command=self.criarEleicao,
        )
        self.btn_criar.grid(row=2, column=0, pady=(30, 60))

        # Frame container
        self.frmEleicoes = ttk.Frame(self.janela, padding=10)
        self.frmEleicoes.grid(
            row=3, column=0, columnspan=3, padx=10, pady=20, sticky="nsew"
        )

    def criarEleicao(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaCriarEleicao.iniciarTela(self.janela)

    def excluirEleicao(self, id):
        if messagebox.askyesno("Confirmação", "Deseja excluir esta eleição?"):
            if self.control.deletar_eleicao(id):
                messagebox.showinfo("Sucesso", "Eleição excluída com sucesso!")
                self.renderizar_eleicoes()
            else:
                messagebox.showerror("Erro", "Erro ao excluir eleição!")

    def renderizar_eleicoes(self):

        ttk.Label(
            self.janela, text="Controle de Eleições", font=("Courier", 20, "bold")
        ).grid(row=1, column=0, pady=(40, 10), padx=(20, 0))

        # Botão criar eleição
        self.btn_criar = ttk.Button(
            self.janela,
            text="+ Criar Nova Eleição",
            bootstyle="primary",
            width=20,
            command=self.criarEleicao,
        )
        self.btn_criar.grid(row=2, column=0, pady=(30, 60))

        # Frame container
        self.frmEleicoes = ttk.Frame(self.janela, padding=10)
        self.frmEleicoes.grid(
            row=3, column=0, columnspan=3, padx=10, pady=20, sticky="nsew"
        )

    def criarEleicao(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaCriarEleicao.iniciarTela(self.janela)

    def excluirEleicao(self, id):
        if messagebox.askyesno("Confirmação", "Deseja excluir esta eleição?"):
            if self.control.deletar_eleicao(id):
                messagebox.showinfo("Sucesso", "Eleição excluída com sucesso!")
                self.renderizar_eleicoes()
            else:
                messagebox.showerror("Erro", "Erro ao excluir eleição!")

    def renderizar_eleicoes(self):
        for widget in self.frmEleicoes.winfo_children():
            widget.destroy()

        # configurar até 4 colunas
        for col in range(4):
            self.frmEleicoes.grid_columnconfigure(col, weight=1)


        # configurar até 4 colunas
        for col in range(4):
            self.frmEleicoes.grid_columnconfigure(col, weight=1)

        eleicoes = self.control.listar_eleicoes()


        if not eleicoes:
            ttk.Label(
                self.frmEleicoes,
                text="Nenhuma eleição cadastrada",
                font=("Courier", 16),
                bootstyle="secondary",
            ).grid(row=0, column=0, columnspan=4, pady=50)
            ttk.Label(
                self.frmEleicoes,
                text="Nenhuma eleição cadastrada",
                font=("Courier", 16),
                bootstyle="secondary",
            ).grid(row=0, column=0, columnspan=4, pady=50)
            return

        for i, eleicao in enumerate(eleicoes):
            id_eleicao, titulo, data_inicio, data_fim = eleicao
            status = self.control.obter_status_eleicao(data_inicio, data_fim)

            # card
            frame_eleicao = ttk.Frame(
                self.frmEleicoes, padding=10, relief="ridge", borderwidth=2
            )
            frame_eleicao.grid(
                row=i // 4, column=i % 4, padx=10, pady=10, sticky="nsew"
            )

            ttk.Label(
                frame_eleicao, text=titulo, font=("Courier", 15, "bold")
            ).pack(anchor="n", pady=5)

            ttk.Label(
                frame_eleicao,
                text=f"Início: {self.control.formatar_data_exibicao(data_inicio)}",
                font=("Courier", 11),
                bootstyle="secondary",
            ).pack()

            ttk.Label(
                frame_eleicao,
                text=f"Fim: {self.control.formatar_data_exibicao(data_fim)}",
                font=("Courier", 11),
                bootstyle="secondary",
            ).pack()

            ttk.Label(
                frame_eleicao,
                text=f"Status: {status}",
                font=("Courier", 12, "bold"),
            ).pack(pady=5)

            frm_btn = ttk.Frame(frame_eleicao)
            frm_btn.pack(fill="x", pady=10)

            ttk.Button(
                frm_btn,
                text="Excluir",
                bootstyle="danger",
                command=lambda id=id_eleicao: self.excluirEleicao(id),
            ).pack(side="left", expand=True, fill="x", padx=2)


def iniciarTela(master=None):
    if master is None:
        app = tb.Window(themename="superhero")
        Tela(app)
        app.mainloop()
    else:
        Tela(master)