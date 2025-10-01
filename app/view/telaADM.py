import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont   
import ttkbootstrap as tb     


class Tela():
    def criarFramesDashboard(self,frmpai, titulo, valor, coluna):
        frameBoard = ttk.Frame(frmpai, padding=20, relief="ridge", borderwidth=3)
        frameBoard.grid(row=0, column=coluna, padx=40)
        ttk.Label(frameBoard, text=titulo, font=("Helvetica", 16, "bold")).pack(pady=10)
        ttk.Label(frameBoard, text=valor, font=("Helvetica", 24)).pack()

    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela do Administrador')
        self.janela.geometry("1920x1080")

        frmTopo = ttk.Frame(self.janela)
        frmTopo.pack(fill="x")

        frmTopo.columnconfigure(0, weight=1)
        frmTopo.columnconfigure(1, weight=1)
        frmTopo.columnconfigure(2, weight=1)

        ttk.Button(frmTopo, text="Logout", bootstyle="danger", width=15).grid(row=0, column=0, sticky="w", padx=20,pady=(0,70))

        ttk.Label(frmTopo, text="Dashboard", font=("Helvetica", 28, "bold")).grid(row=0, column=1, sticky="n", padx=(10,200),pady=(60,40))



#-----------Dashboard-----------
        frmDashboard = ttk.Frame(self.janela )
        frmDashboard.pack()

        self.criarFramesDashboard(frmDashboard, "ELEIÇÕES ATIVAS", "3", 0)
        self.criarFramesDashboard(frmDashboard, "TOTAL DE VOTOS ÚLTIMA ELEIÇÃO", "1.250", 1)
        self.criarFramesDashboard(frmDashboard, "TOTAL DE CHAPAS", "15", 2)

#---------botoes-------------
        fonteBotoes = tkFont.Font(family="Helvetica", size=20, weight="bold")
        style = tb.Style()  
        style.configure("Fonte.TButton", font=fonteBotoes)
        botoes_frame = ttk.Frame(self.janela)
        botoes_frame.pack(expand=True, pady=40)

        ttk.Button(botoes_frame, text="Gerenciar Eleições", width=40, bootstyle="primary",style="Fonte.TButton").grid(row=0, column=0, pady=10)

        ttk.Button(botoes_frame, text="Gerenciar Chapas", width=40, bootstyle="primary",style="Fonte.TButton").grid(row=1, column=0, pady=10)

        ttk.Button(botoes_frame, text="Gerenciar Cargos",   width=40, bootstyle="primary",style="Fonte.TButton").grid(row=2, column=0, pady=10)
        
        ttk.Button(botoes_frame, text="Cadastrar Administradores", width=40, bootstyle="primary",style="Fonte.TButton").grid(row=3, column=0, pady=10)
        

   

app = tb.Window(themename='superhero')
Tela(app)
app.mainloop()