from ttkbootstrap import ttk
import ttkbootstrap as tb
from tkinter import messagebox

import telaEleicoes, telaChapas, telaCargos, telaLogin # e a de cadastrar adm

class TelaADM:
    def criarFramesDashboard(self, frmpai, titulo, valor, coluna):
        frameBoard = ttk.Frame(frmpai, padding=20, relief="ridge", borderwidth=3)
        frameBoard.grid(row=0, column=coluna, padx=40)
        ttk.Label(frameBoard, text=titulo, font=("Courier", 16, "bold")).pack(pady=10)
        ttk.Label(frameBoard, text=valor, font=("Courier", 24)).pack()

    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela do Administrador')
        self.janela.geometry("1920x1080")

        # limpa tudo que já estava na janela (ex: telaLogin)
        for widget in self.janela.winfo_children():
            widget.destroy()

        frmTopo = ttk.Frame(self.janela)
        frmTopo.pack(fill="x")

        frmTopo.columnconfigure(0, weight=1)
        frmTopo.columnconfigure(1, weight=1)
        frmTopo.columnconfigure(2, weight=1)

        self.btn_logout = ttk.Button(frmTopo,text="Logout",bootstyle="danger",width=15,command=self.logout)
        self.btn_logout.grid(row=0, column=0, sticky="w", padx=20, pady=(0, 70))

        ttk.Label(frmTopo,text="Dashboard",font=("Courier", 28, "bold")).grid(row=0, column=1, sticky="n", padx=(10, 200), pady=(60, 40))

        # Configurar fonte padrão global
        self.janela.option_add("*Font", "Courier 14")

        # Configurar estilos do ttkbootstrap para usar Courier
        self.configurar_fontes()

        # ----------- Dashboard -----------
        frmDashboard = ttk.Frame(self.janela)
        frmDashboard.pack()

        self.criarFramesDashboard(frmDashboard, "ELEIÇÕES ATIVAS", "3", 0)
        self.criarFramesDashboard(frmDashboard, "TOTAL DE VOTOS ÚLTIMA ELEIÇÃO", "1.250", 1)
        self.criarFramesDashboard(frmDashboard, "TOTAL DE CHAPAS", "15", 2)

        # --------- botões -------------
        botoes_frame = ttk.Frame(self.janela)
        botoes_frame.pack(expand=True, pady=40)

        self.btnEleicao = ttk.Button(botoes_frame,text="Gerenciar Eleições",width=40,bootstyle="primary",style="Fonte.TButton",command=lambda: self.trocarTela(telaEleicoes))
        self.btnEleicao.grid(row=0, column=0, pady=10)

        self.btnChapas = ttk.Button(botoes_frame,text="Gerenciar Chapas",width=40,bootstyle="primary",style="Fonte.TButton",command=lambda: self.trocarTela(telaChapas))
        self.btnChapas.grid(row=1, column=0, pady=10)

        self.btnCargos = ttk.Button(botoes_frame,text="Gerenciar Cargos",width=40,bootstyle="primary",style="Fonte.TButton",command=lambda: self.trocarTela(telaCargos))
        self.btnCargos.grid(row=2, column=0, pady=10)

        self.btnCadastrarADM = ttk.Button(botoes_frame,text="Cadastrar Administradores",width=40,bootstyle="primary",style="Fonte.TButton",command=None )# depois chama telaCadastrarADM
        self.btnCadastrarADM.grid(row=3, column=0, pady=10)

    def configurar_fontes(self):
        """Configura todas as fontes para usar Courier"""
        style = tb.Style()
        style.configure("TLabel", font=("Courier", 14))
        style.configure("TButton", font=("Courier", 14))
        style.configure("TFrame", font=("Courier", 14))
        style.configure("Fonte.TButton", font=("Courier", 20, "bold"))

    def trocarTela(self, modulo):
        for widget in self.janela.winfo_children():
            widget.destroy()
        modulo.Tela(self.janela)

    def logout(self):
        resposta = messagebox.askyesno("Logout", "Tem certeza que deseja fazer logout?")
        if resposta:
            for widget in self.janela.winfo_children():
                widget.destroy()
            telaLogin.Tela(self.janela)


def iniciarTela():
    app = tb.Window()
    TelaADM(app)
    app.mainloop()