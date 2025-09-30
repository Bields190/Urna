import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk

import telaCriarEleicao

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Criação de Chapas')
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")

        self.lbl_titulo=tk.Label(self.janela, text="Adicionar Chapa", font=("Arial", 24, "bold"), bg="white")
        self.lbl_titulo.pack(pady=45)

        self.frm_geral=tk.Frame(self.janela, bg="white")
        self.frm_geral.pack(pady=(10, 30))

        self.frm_entradas=tk.Frame(self.frm_geral, bg="white")
        self.frm_entradas.grid(row=0, column=1, padx=20)

        #Frame para a foto da chapa
        self.frm_foto=tk.Frame(self.frm_geral, bg="white", width=225, height=225, highlightthickness=1, highlightbackground="black")
        self.frm_foto.grid(row=0, column=0, padx=20)
        self.frm_foto.grid_propagate(False)

        self.lbl_adcFoto=tk.Label(self.frm_foto, text="Adicionar Foto", font=("Arial", 16), bg="white")
        self.lbl_adcFoto.place(relx=0.5, rely=0.5, anchor="center")
        self.lbl_adcFoto.bind('<Button-1>', lambda event: self.adcFoto())

        #Entrys e Labels de nome, número e slogan da chapa
        self.lbl_nome=tk.Label(self.frm_entradas, text="Nome da Chapa:", font=("Arial", 16), bg="white")
        self.lbl_nome.pack(anchor="w")
        self.entry_nome=tk.Entry(self.frm_entradas, width=50, highlightthickness=1, highlightbackground="black")
        self.entry_nome.pack(pady=(0), ipady=3)

        self.lbl_num=tk.Label(self.frm_entradas, text="Número da Chapa:", font=("Arial", 16), bg="white")
        self.lbl_num.pack(anchor="w")
        self.entry_num=tk.Entry(self.frm_entradas, width=50, highlightthickness=1, highlightbackground="black")
        self.entry_num.pack(pady=(0), ipady=3)

        self.lbl_slogan=tk.Label(self.frm_entradas, text="Slogan:", font=("Arial", 16), bg="white")
        self.lbl_slogan.pack(anchor="w")
        self.entry_slogan=tk.Entry(self.frm_entradas, width=50, highlightthickness=1, highlightbackground="black")
        self.entry_slogan.pack(pady=(0), ipady=20)  

        self.btn_entrar=tk.Button(self.janela, text='Salvar',bg='black',fg='white', width=10,font=("Arial",14), command= self.salvar_chapa)
        self.btn_entrar.pack(pady=0)

        #Frame para adicionar cargos
        self.frm_cargos=tk.Frame(self.janela, bg="white", width=1500, height=350, highlightthickness=1, highlightbackground="black")
        self.frm_cargos.pack(pady=(25,20))  
        self.frm_cargos.pack_propagate(False)

        self.btn_entrar=tk.Button(self.frm_cargos, text='Designar Cargo',bg='black',fg='white', width=15,font=("Arial",14), command=self.abrir)
        self.btn_entrar.pack(pady=10, anchor="w", padx=10)

    #PopUp de adicionar cargo
    def abrir(self):
        self.adcCargo=tk.Toplevel(self.janela)
        self.adcCargo.grab_set()
        self.adcCargo.title('Designar Cargo')
        self.adcCargo.configure(bg="white")
        self.janelaCentro(self.adcCargo, 450, 250)

        self.lbl_tituloCargo=tk.Label(self.adcCargo, text="Designar Cargo", font=("Arial", 16, "bold"), bg="white")
        self.lbl_tituloCargo.pack(pady=15)

        self.frm_campos=tk.Frame(self.adcCargo, bg="white")
        self.frm_campos.pack(padx=20)

        self.lbl_cargo=tk.Label(self.frm_campos, text="Cargo:", font=("Arial", 10), bg="white")
        self.lbl_cargo.pack(anchor="w")
        cargos=['Presidente', 'Vice-Presidente', 'Diretor Geral']
        estiloCargo=ttk.Style()
        estiloCargo.configure('Custom.TCombobox', padding=3)
        self.cargos=tk.StringVar()
        self.cbx_cargos=ttk.Combobox(self.frm_campos, values=cargos, textvariable=self.cargos, state='readonly', width=47, style='Custom.TCombobox')
        self.cbx_cargos.current(0)
        self.cbx_cargos.pack(pady=(0, 10))

        self.lbl_descricao=tk.Label(self.frm_campos, text="Nome do Candidato:", font=("Arial", 10), bg="white")
        self.lbl_descricao.pack(anchor="w")
        self.entry_descricao=tk.Entry(self.frm_campos, width=50, highlightthickness=1, highlightbackground="black")
        self.entry_descricao.pack(pady=(0, 10), ipady=3)

        self.btn_entrar=tk.Button(self.adcCargo, text='Adicionar', bg='black', fg='white', width=15, font=("Arial",14))
        self.btn_entrar.pack(pady=10)

    def janelaCentro(self, window, largura, altura):
        x=(window.winfo_screenwidth()-largura)//2
        y=(window.winfo_screenheight()-altura)//2
        window.geometry(f"{largura}x{altura}+{x}+{y}")

    #Comando para adicionar foto da chapa
    def adcFoto(self):
        tipos=(('Imagens', '*.jpeg *.jpg'), ('Todos', '*.*'))
        caminho_imagem = fd.askopenfilename(filetypes=tipos)
        if caminho_imagem:
            imagem=Image.open(caminho_imagem)
            imagem=imagem.resize((225, 225))
            imagem_tk=ImageTk.PhotoImage(imagem)

            self.lbl_imagem = tk.Label(self.frm_foto, bg="white")
            self.lbl_imagem.place(relx=0.5, rely=0.5, anchor="center")
            self.lbl_imagem.config(image=imagem_tk)
            self.lbl_imagem.image = imagem_tk
            self.lbl_adcFoto.place_forget()

    def salvar_chapa(self):
        tk.messagebox.showinfo("Criação de chapas", "Os dados foram Salvos!")
        #aq ele salva tudo no bd
        self.janela.destroy()
        telaCriarEleicao.iniciarTela()



def iniciarTela():
    app = tk.Tk()
    Tela(app)
    app.mainloop()