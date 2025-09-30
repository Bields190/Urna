import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk

import telaCriarEleicao

class Tela:
    def mostrarMenu(self):
        self.menu.post(self.janela.winfo_x() + 50, self.janela.winfo_y() + 50)
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Eleicoes')
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")
        
#-------menu hamburguer---------aaaaaaaaaaaaaaaaaaaaaaaaaaa
        img = Image.open('app/src/hamburger.png')
        img = img.resize((30,30))
        self.iconeHamburguer = ImageTk.PhotoImage(img)
        
        
        self.btn = tk.Button(self.janela, image=self.iconeHamburguer, command=self.mostrarMenu, bg="white")
        self.btn.image = self.iconeHamburguer  
        self.btn.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        
        self.menu = Menu(self.janela, tearoff=0)

        self.menu.add_command(label="Logout")

    
#-----sessão das eleições----------
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=3)
        self.janela.rowconfigure(3, weight=1)
        
        self.lbl_ola = tk.Label(text="Olá! Administrador",font=("Arial",20,"bold"), bg="white")
        self.lbl_ola.grid(row=1,column=0, pady=(40, 10), padx=(20,0))
        
        self.btn_criar_eleicao = tk.Button(text="+ Criar Nova Eleição", font=("Arial",16,"bold"), command= lambda:(self.janela.destroy(), telaCriarEleicao.iniciarTela()))
        self.btn_criar_eleicao.grid(row=2,column=0,pady=(30,60))
#-----sessão 2 das eleições----------      
        self.frmEleicoes = tk.Frame(self.janela, bd=2, padx=5, pady=5,bg="white",relief="solid")
        self.frmEleicoes.grid(row=3, column=0, columnspan=3, padx=80, pady=(20,100), sticky="nsew")
        self.frmEleicoes.columnconfigure(0, weight=1)
        self.frmEleicoes.columnconfigure(1, weight=1)
        self.frmEleicoes.columnconfigure(2, weight=1)

#essas eleicoes sao apenas exemplos para dimensionar a tela
#-----eleição 1------
        eleicao1 = tk.Frame(self.frmEleicoes, bd=2, relief="solid", width=100, height=400,bg="white")
        eleicao1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        eleicao1.grid_propagate(False)  
        eleicao1.pack_propagate(False)  

        tk.Label(eleicao1, text="Eleição 15", font=("Arial", 15, "bold"), fg="black",padx=15,pady=15,bg="white").pack(anchor="nw", side="top")
        tk.Label(eleicao1, text="Ativa", bg="green", fg="white", font=("Arial", 13, "bold"),height=3).pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Button(eleicao1, text="Encerrar",font=("Arial", 13, "bold"),height=3, bg="white",relief="solid").pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Button(eleicao1, text="Abrir Urna",font=("Arial", 13, "bold"),height=3, bg="white",relief="solid").pack(fill="x", pady=5, side="bottom",padx=10)
        
'''

#-----eleição 2------
        eleicao2 = tk.Frame(self.frmEleicoes, bd=2, relief="solid", width=100, height=400,bg="white")
        eleicao2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        eleicao2.grid_propagate(False)
        eleicao2.pack_propagate(False)

        tk.Label(eleicao2, text="Eleição 14", font=("Arial", 15, "bold"), fg="black",padx=15,pady=15,bg="white").pack(anchor="nw", side="top")
        tk.Label(eleicao2, text="Encerrada", bg="red", fg="white", font=("Arial", 13, "bold"),height=3).pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Button(eleicao2, text="Arquivar",font=("Arial", 13, "bold"),height=3, bg="white",relief="solid").pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Button(eleicao2, text="Resultados",font=("Arial", 13, "bold"),height=3, bg="white",relief="solid").pack(fill="x", pady=5, side="bottom",padx=10)

#-----eleição 3------
        eleicao3 = tk.Frame(self.frmEleicoes, bd=2, relief="solid", width=100, height=400,bg="white")
        eleicao3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        eleicao3.grid_propagate(False)
        eleicao3.pack_propagate(False)

        tk.Label(eleicao3, text="Eleição 13", font=("Arial", 15, "bold"), fg="black",padx=15,pady=15,bg="white").pack(anchor="nw", side="top")
        tk.Label(eleicao3, text="Encerrada", bg="red", fg="white", font=("Arial", 13, "bold"),height=3).pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Button(eleicao3, text="Arquivar",font=("Arial", 13, "bold"),height=3,bg="white",relief="solid").pack(fill="x", pady=5, side="bottom",padx=10)
        tk.Button(eleicao3, text="Resultados",font=("Arial", 13, "bold"),height=3,bg="white",relief="solid").pack(fill="x", pady=5, side="bottom",padx=10)'''
     
def iniciarTela():
        gui = tk.Tk()
        Tela(gui)
        gui.mainloop()