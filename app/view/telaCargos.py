import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk

import telaCriarEleicao

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Controle de Chapas')
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")     
    
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=3)
        self.janela.rowconfigure(3, weight=1)

        self.lbl_ola = tk.Label(text="Controle de Cargos",font=("Arial",20,"bold"), bg="white")
        self.lbl_ola.grid(row=1,column=0, pady=(40, 10), padx=(20,0))
        
        self.btn_criar_eleicao = tk.Button(text="+ Criar Novo Cargo", font=("Arial",16,"bold"), command=self.criarCargo)
        self.btn_criar_eleicao.grid(row=2,column=0,pady=(30,60))
   
        self.frmChapas = tk.Frame(self.janela, bd=2, padx=5, pady=5,bg="white")
        self.frmChapas.grid(row=3, column=0, columnspan=3, padx=10, pady=(20,20), sticky="nsew")
        self.frmChapas.columnconfigure(0, weight=1)
        self.frmChapas.columnconfigure(1, weight=1)
        self.frmChapas.columnconfigure(2, weight=1)
        self.frmChapas.columnconfigure(3, weight=1)

        cargo1 = tk.Frame(self.frmChapas, bd=2, relief="solid", width=30, height=100, bg="white")
        cargo1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        cargo1.grid_propagate(False)  
        cargo1.pack_propagate(False)  

        tk.Label(cargo1, text="Presidente", font=("Arial", 15, "bold"), fg="black", padx=10, pady=10, bg="white").pack(anchor="nw", side="top")
        
        frm_botoes1 = tk.Frame(cargo1, bg="white")
        frm_botoes1.pack(side="bottom", fill="x", padx=10, pady=5)
        tk.Button(frm_botoes1, text="Editar", font=("Arial", 13, "bold"), height=3, bg="white", relief="solid").pack(side="left", fill="x", expand=True, padx=(0,5))
        tk.Button(frm_botoes1, text="Excluir", bg="red", fg="white", font=("Arial", 13, "bold"), height=3).pack(side="left", fill="x", expand=True, padx=(5,0))

        cargo2 = tk.Frame(self.frmChapas, bd=2, relief="solid", width=30, height=50, bg="white")
        cargo2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        cargo2.grid_propagate(False)  
        cargo2.pack_propagate(False)  

        tk.Label(cargo2, text="Vice-Presidente", font=("Arial", 15, "bold"), fg="black", padx=10, pady=10, bg="white").pack(anchor="nw", side="top")
        
        frm_botoes2 = tk.Frame(cargo2, bg="white")
        frm_botoes2.pack(side="bottom", fill="x", padx=10, pady=5)
        tk.Button(frm_botoes2, text="Editar", font=("Arial", 13, "bold"), height=3, bg="white", relief="solid").pack(side="left", fill="x", expand=True, padx=(0,5))
        tk.Button(frm_botoes2, text="Excluir", bg="red", fg="white", font=("Arial", 13, "bold"), height=3).pack(side="left", fill="x", expand=True, padx=(5,0))

        cargo3 = tk.Frame(self.frmChapas, bd=2, relief="solid", width=30, height=50, bg="white")
        cargo3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        cargo3.grid_propagate(False)  
        cargo3.pack_propagate(False)  

        tk.Label(cargo3, text="Diretor-Geral", font=("Arial", 15, "bold"), fg="black", padx=10, pady=10, bg="white").pack(anchor="nw", side="top")
        
        frm_botoes3 = tk.Frame(cargo3, bg="white")
        frm_botoes3.pack(side="bottom", fill="x", padx=10, pady=5)
        tk.Button(frm_botoes3, text="Editar", font=("Arial", 13, "bold"), height=3, bg="white", relief="solid").pack(side="left", fill="x", expand=True, padx=(0,5))
        tk.Button(frm_botoes3, text="Excluir", bg="red", fg="white", font=("Arial", 13, "bold"), height=3).pack(side="left", fill="x", expand=True, padx=(5,0))

    def criarCargo(self):
        pass

app = tk.Tk()
Tela(app)
app.mainloop()