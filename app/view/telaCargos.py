import tkinter as tk
from tkinter import Menu
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
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
        self.adcCargo=tk.Toplevel(self.janela)
        self.adcCargo.grab_set()
        self.adcCargo.title('Adicionar Cargo')
        self.adcCargo.configure(bg="white")
        self.janelaCentro(self.adcCargo, 450, 250)

        self.lbl_tituloCargo=tk.Label(self.adcCargo, text="Adicionar Cargo", font=("Arial", 16, "bold"), bg="white")
        self.lbl_tituloCargo.pack(pady=15)

        self.frm_campos=tk.Frame(self.adcCargo, bg="white")
        self.frm_campos.pack(padx=20)

        self.lbl_cargo=tk.Label(self.frm_campos, text="Cargo:", font=("Arial", 10), bg="white")
        self.lbl_cargo.pack(anchor="w")
        self.ent_cargo=tk.Entry(self.frm_campos, width=50, highlightthickness=1, highlightbackground="black")
        self.ent_cargo.pack(pady=(0, 10), ipady=3)

        self.lbl_descricao=tk.Label(self.frm_campos, text="Descrição:", font=("Arial", 10), bg="white")
        self.lbl_descricao.pack(anchor="w")
        self.entry_descricao=tk.Entry(self.frm_campos, width=50, highlightthickness=1, highlightbackground="black")
        self.entry_descricao.pack(pady=(0, 10), ipady=3)

        self.btn_entrar=tk.Button(self.adcCargo, text='Adicionar', bg='black', fg='white', width=15, font=("Arial",14), command=self.salvarCargo)
        self.btn_entrar.pack(pady=10)

    def salvarCargo(self):
        self.adcCargo.destroy()

    def janelaCentro(self, window, largura, altura):
        x=(window.winfo_screenwidth()-largura)//2
        y=(window.winfo_screenheight()-altura)//2
        window.geometry(f"{largura}x{altura}+{x}+{y}")

app = tk.Tk()
Tela(app)
app.mainloop()