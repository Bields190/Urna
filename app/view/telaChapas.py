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

        self.lbl_ola = tk.Label(text="Olá! Administrador",font=("Arial",20,"bold"), bg="white")
        self.lbl_ola.grid(row=1,column=0, pady=(40, 10), padx=(20,0))
        
        self.btn_criar_eleicao = tk.Button(text="+ Criar Nova Chapa", font=("Arial",16,"bold"), command= lambda:(self.janela.destroy(), telaCriarEleicao.iniciarTela()))
        self.btn_criar_eleicao.grid(row=2,column=0,pady=(30,60))
   
        self.frmChapas = tk.Frame(self.janela, bd=2, padx=5, pady=5,bg="white")
        self.frmChapas.grid(row=3, column=0, columnspan=3, padx=10, pady=(20,20), sticky="nsew")
        self.frmChapas.columnconfigure(0, weight=1)
        self.frmChapas.columnconfigure(1, weight=1)
        self.frmChapas.columnconfigure(2, weight=1)
        self.frmChapas.columnconfigure(3, weight=1)

        chapa1 = tk.Frame(self.frmChapas, bd=2, relief="solid", width=30, height=275,bg="white")
        chapa1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        chapa1.grid_propagate(False)  
        chapa1.pack_propagate(False)  

        tk.Label(chapa1, text="Chapa 1", font=("Arial", 15, "bold"), fg="black", padx=10, pady=10, bg="white").pack(anchor="nw", side="top")
        tk.Button(chapa1, text="Excluir", bg="red", fg="white", font=("Arial", 13, "bold"),height=3).pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Button(chapa1, text="Editar",font=("Arial", 13, "bold"),height=3, bg="white",relief="solid").pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Label(chapa1, text="Epitassayssa",font=("Arial", 18, "bold"), fg="black", padx=10, pady=10, bg="white").pack(anchor="nw", side="bottom")

        chapa2 = tk.Frame(self.frmChapas, bd=2, relief="solid", width=30, height=50,bg="white")
        chapa2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        chapa2.grid_propagate(False)  
        chapa2.pack_propagate(False)  

        tk.Label(chapa2, text="Chapa 2", font=("Arial", 15, "bold"), fg="black", padx=10, pady=10, bg="white").pack(anchor="nw", side="top")
        tk.Button(chapa2, text="Excluir", bg="red", fg="white", font=("Arial", 13, "bold"),height=3).pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Button(chapa2, text="Editar",font=("Arial", 13, "bold"),height=3, bg="white",relief="solid").pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Label(chapa2, text="Porongabi",font=("Arial", 18, "bold"), fg="black", padx=10, pady=10, bg="white").pack(anchor="nw", side="bottom")

        chapa3 = tk.Frame(self.frmChapas, bd=2, relief="solid", width=30, height=50,bg="white")
        chapa3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        chapa3.grid_propagate(False)  
        chapa3.pack_propagate(False)  

        tk.Label(chapa3, text="Chapa 3", font=("Arial", 15, "bold"), fg="black", padx=10, pady=10, bg="white").pack(anchor="nw", side="top")
        tk.Button(chapa3, text="Excluir", bg="red", fg="white", font=("Arial", 13, "bold"),height=3).pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Button(chapa3, text="Editar",font=("Arial", 13, "bold"),height=3, bg="white",relief="solid").pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Label(chapa3, text="Crulil do Sul",font=("Arial", 18, "bold"), fg="black", padx=10, pady=10, bg="white").pack(anchor="nw", side="bottom")

        chapa4 = tk.Frame(self.frmChapas, bd=2, relief="solid", width=30, height=50,bg="white")
        chapa4.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")
        chapa4.grid_propagate(False)  
        chapa4.pack_propagate(False)  

        tk.Label(chapa4, text="Chapa 4", font=("Arial", 15, "bold"), fg="black", padx=10, pady=10, bg="white").pack(anchor="nw", side="top")
        tk.Button(chapa4, text="Excluir", bg="red", fg="white", font=("Arial", 13, "bold"),height=3).pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Button(chapa4, text="Editar",font=("Arial", 13, "bold"),height=3, bg="white",relief="solid").pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Label(chapa4, text="Ouricurey Mqs",font=("Arial", 18, "bold"), fg="black", padx=10, pady=10, bg="white").pack(anchor="nw", side="bottom")

app = tk.Tk()
Tela(app)
app.mainloop()