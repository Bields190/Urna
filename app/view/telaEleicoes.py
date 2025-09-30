import tkinter as tk
from tkinter import Menu
from PIL import Image, ImageTk

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
        
        
        self.btn = tk.Button(self.janela, image=self.iconeHamburguer, command=self.mostrarMenu)
        self.btn.image = self.iconeHamburguer  
        self.btn.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        
        self.menu = Menu(self.janela, tearoff=0)

        self.menu.add_command(label="Opção 20")

    
#-----sessão das eleições----------
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=3)
        self.janela.rowconfigure(3, weight=1)
        
        self.lbl_ola = tk.Label(text="Olá! Administrador",font=("Arial",20,"bold"))
        self.lbl_ola.grid(row=1,column=0, pady=(40, 10), padx=(20,0))
        
        self.btn_criar_eleicao = tk.Button(text="+ Criar Nova Eleição", font=("Arial",16,"bold"))
        self.btn_criar_eleicao.grid(row=2,column=0,pady=(30,60))
#-----sessão 2 das eleições----------      
        self.frmEleicoes = tk.Frame(self.janela, bd=2, relief="solid", padx=5, pady=5)
        self.frmEleicoes.grid(row=3, column=0, columnspan=3, padx=80, pady=(20,100), sticky="nsew")
        self.frmEleicoes.columnconfigure(0, weight=1)
        self.frmEleicoes.columnconfigure(1, weight=1)
        self.frmEleicoes.columnconfigure(2, weight=1)

#essas eleicoes sao apenas exemplos para dimensionar a tela
#-----eleição 1------
        eleicao1 = tk.Frame(self.frmEleicoes, bd=2, relief="solid", width=100, height=400)
        eleicao1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        eleicao1.grid_propagate(False)  
        eleicao1.pack_propagate(False)  


        tk.Label(eleicao1, text="Eleição 15", font=("Arial", 12, "bold"), fg="black").pack(anchor="nw", side="top")
        tk.Label(eleicao1, text="Ativa", bg="green", fg="white", font=("Arial", 10, "bold")).pack(fill="x", pady=2, side="bottom")
        tk.Button(eleicao1, text="Encerrar").pack(fill="x", pady=2, side="bottom")
        tk.Button(eleicao1, text="Abrir Urna").pack(fill="x", pady=2, side="bottom")
        tk.Label(eleicao1, text="●", fg="green", font=("Arial", 10, "bold")).pack(anchor="ne", side="bottom")
        


#-----eleição 2------
        eleicao2 = tk.Frame(self.frmEleicoes, bd=2, relief="solid", width=100, height=400)
        eleicao2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        eleicao2.grid_propagate(False)
        eleicao2.pack_propagate(False)

        tk.Label(eleicao2, text="Eleição 14", font=("Arial", 12, "bold"), fg="black").pack(anchor="nw")
        tk.Label(eleicao2, text="●", fg="red", font=("Arial", 10, "bold")).pack(anchor="ne")
        tk.Button(eleicao2, text="Resultados").pack(fill="x", pady=2)
        tk.Button(eleicao2, text="Arquivar").pack(fill="x", pady=2)
        tk.Label(eleicao2, text="Encerrada", bg="red", fg="white", font=("Arial", 10, "bold")).pack(fill="x", pady=2)

#-----eleição 3------
        eleicao3 = tk.Frame(self.frmEleicoes, bd=2, relief="solid", width=100, height=400)
        eleicao3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
        eleicao3.grid_propagate(False)
        eleicao3.pack_propagate(False)

        tk.Label(eleicao3, text="Eleição 13", font=("Arial", 12, "bold"), fg="black").pack(anchor="nw")
        tk.Label(eleicao3, text="●", fg="red", font=("Arial", 10, "bold")).pack(anchor="ne")
        tk.Button(eleicao3, text="Resultados").pack(fill="x", pady=2)
        tk.Button(eleicao3, text="Arquivar").pack(fill="x", pady=2)
        tk.Label(eleicao3, text="Encerrada", bg="red", fg="white", font=("Arial", 10, "bold")).pack(fill="x", pady=2)
     
gui = tk.Tk()
Tela(gui)
gui.mainloop()