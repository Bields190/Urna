import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Criação de Chapas')
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")

        self.lbl_topo=tk.Label(self.janela, text="Adicionar Chapa", font=("Arial", 24, "bold"), bg="white")
        self.lbl_topo.pack(pady=45)

        self.frm_geral=tk.Frame(self.janela, bg="white")
        self.frm_geral.pack(pady=(10, 30))

        self.frm_entradas=tk.Frame(self.frm_geral, bg="white")
        self.frm_entradas.grid(row=0, column=1, padx=20)

        # Frame para a foto da chapa.
        self.frm_foto=tk.Frame(self.frm_geral, bg="white", width=225, height=225, highlightthickness=1, highlightbackground="black")
        self.frm_foto.grid(row=0, column=0, padx=20)
        self.frm_foto.grid_propagate(False)

        # self.btn_addFoto = tk.Button(self.frm_foto, text='Adicionar Imagem',bg='white',fg='black', width=15,font=("Arial",14))
        # self.btn_addFoto.pack(pady=10, anchor="w", padx=10)
        
        self.lbl_nome = tk.Label(self.frm_entradas, text="Nome da Chapa:", font=("Arial", 16), bg="white")
        self.lbl_nome.pack(anchor="w")
        self.entry_nome = tk.Entry(self.frm_entradas, width=50, highlightthickness=1, highlightbackground="black")
        self.entry_nome.pack(pady=(0), ipady=3)

        self.lbl_num = tk.Label(self.frm_entradas, text="Número da Chapa:", font=("Arial", 16), bg="white")
        self.lbl_num.pack(anchor="w")
        self.entry_num = tk.Entry(self.frm_entradas, width=50, highlightthickness=1, highlightbackground="black")
        self.entry_num.pack(pady=(0), ipady=3)

        self.lbl_slogan = tk.Label(self.frm_entradas, text="Slogan:", font=("Arial", 16), bg="white")
        self.lbl_slogan.pack(anchor="w")
        self.entry_slogan = tk.Entry(self.frm_entradas, width=50, highlightthickness=1, highlightbackground="black")
        self.entry_slogan.pack(pady=(0), ipady=20)  

        self.btn_entrar = tk.Button(self.janela, text='Salvar',bg='black',fg='white', width=10,font=("Arial",14))
        self.btn_entrar.pack(pady=0)

        self.frm_cargos=tk.Frame(self.janela, bg="white", width=1500, height=350, highlightthickness=1, highlightbackground="black")
        self.frm_cargos.pack(pady=(25,20))  
        self.frm_cargos.pack_propagate(False)

        self.btn_entrar = tk.Button(self.frm_cargos, text='Adicionar Cargo',bg='black',fg='white', width=15,font=("Arial",14))
        self.btn_entrar.pack(pady=10, anchor="w", padx=10)



app = tk.Tk()
app.state('zoomed')
Tela(app)
app.mainloop()