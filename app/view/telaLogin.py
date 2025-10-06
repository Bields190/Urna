import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import ttkbootstrap as tb
from ttkbootstrap import ttk
import sys
import os

import telaADM
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_administrador # type: ignore

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Login')
        self.janela.geometry("1920x1080")
        self.janela.option_add("*Font", "Courier 14")

        # Frame principal
        self.frm_principal = ttk.Frame(self.janela)
        self.frm_principal.pack(fill='both', expand=True)

        self.frm = ttk.Frame(self.frm_principal)
        self.frm.pack(expand=True)

        # Logo
        self.imagem = tk.PhotoImage(file="app/src/Logo.png")
        self.imagem = self.imagem.subsample(3, 3)
        self.lbl = ttk.Label(self.frm, image=self.imagem)
        self.lbl.image = self.imagem
        self.lbl.pack()

        # Usuário
        self.lbl1 = ttk.Label(self.frm, text='Usuário(Matrícula):', font=("Arial", 18))
        self.lbl1.pack(pady=(40, 0))

        self.entry1 = ttk.Entry(self.frm, width=40, bootstyle="info")
        self.entry1.pack()
        self.entry1.bind('<Return>', lambda event: event.widget.event_generate("<Tab>"))

        # Senha
        self.lbl2 = ttk.Label(self.frm, text='Senha:', font=("Arial", 18))
        self.lbl2.pack()

        self.entry2 = ttk.Entry(self.frm, show='*', width=40, bootstyle="info")
        self.entry2.pack(pady=5)
        self.entry2.bind('<Return>', self.login)

        # Botão Entrar
        self.btn_entrar = ttk.Button(
            self.frm, text='Entrar', width=10,
            bootstyle="dark", command=self.login
        )
        self.btn_entrar.pack(pady=10)

    def login(self, event=None):
        login_result = c_administrador.Control(self).login()
        if login_result and login_result != False:
            messagebox.showinfo("Login - ADM", "Login bem-sucedido! Bem vindo, Administrador.")
            for widget in self.janela.winfo_children():
                widget.destroy()
            telaADM.TelaADM(self.janela, admin_data=login_result)
        else:
            messagebox.showerror("Login - ADM", "Usuário ou senha incorretos.")


def iniciarTela():
    app = tb.Window(themename="litera")
    Tela(app)
    app.mainloop()