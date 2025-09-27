import tkinter as tk
from PIL import Image, ImageTk

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))

import c_administrador, c_eleitor

class Tela:

    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Login')
        self.janela.geometry("1920x1080")

        self.frm_principal = tk.Frame(self.janela,bg='white')
        self.frm_principal.pack(fill='both',expand=True)
        self.frm = tk.Frame(self.frm_principal,bg='white')
        self.frm.pack(expand=True)
        
        self.imagem = tk.PhotoImage(file="app/src/Logo.png")
        self.imagem = self.imagem.subsample(3,3)
        self.lbl = tk.Label(self.frm, image=self.imagem, bg='white')
        self.lbl.image = self.imagem
        self.lbl.pack()
        
#------entry e label de user---------
        self.lbl1 = tk.Label(self.frm, text='Usuário:', bg='white',font=("Arial",18))
        self.lbl1.pack(pady=(40, 0))
        self.entry1 = tk.Entry(self.frm, width=40)
        self.entry1.pack()
        self.entry1.bind('<Return>', lambda event: event.widget.event_generate("<Tab>"))
        
#------entry e label de senha---------
        self.lbl2 = tk.Label(self.frm, text='Senha:',bg='white',font=("Arial",18))
        self.lbl2.pack()
        self.entry2 = tk.Entry(self.frm, show='*', width=40)    
        self.entry2.pack(pady=5)
        self.entry2.bind('<Return>', self.login)

        self.btn_entrar = tk.Button(self.frm, text='Entrar',bg='black',fg='white', width=10,font=("Arial",14), command=self.login)
        self.btn_entrar.pack(pady=10)

# PARA ELEITOR, O USUARIO EH A MATRICULA E A SENHA EH O PRIMEIRO NOME
# ex: 20170300016, Fernanda
    def login(self, event=None):
        if c_administrador.Control(self).login():
                tk.messagebox.showinfo("Login - ADM", "Login bem-sucedido! Bem vindo, Administrador.")
                self.janela.destroy()
                import telaEleicoes
        elif c_eleitor.Control(self).login():
                tk.messagebox.showinfo("Login - Usuário", "Login bem-sucedido! Bem vindo, Usuário.")
                self.janela.destroy()
                #import telaUsuario

        else:
                tk.messagebox.showerror("Login - ADM", "Usuário ou senha incorretos.")

app = tk.Tk()
Tela(app)
app.mainloop()