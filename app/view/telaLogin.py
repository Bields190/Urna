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

def resource_path(relative_path):
    """Obtém o caminho absoluto para recursos, funciona tanto em desenvolvimento quanto em executável"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
        # No PyInstaller, os arquivos estão em src/ não app/src/
        if relative_path.startswith("app/src/"):
            relative_path = relative_path[4:]  # Remove "app/"
    except Exception:
        # Em desenvolvimento, busca a partir da raiz do projeto
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    return os.path.join(base_path, relative_path)

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Urna Eletrônica')
        # Configura para tela cheia
        self.janela.attributes('-fullscreen', True)
        self.janela.option_add("*Font", "Courier 14")
        
        self.janela.bind('<F11>', self.toggle_fullscreen)

        # Frame principal
        self.frm_principal = ttk.Frame(self.janela)
        self.frm_principal.pack(fill='both', expand=True)

        self.frm = ttk.Frame(self.frm_principal)
        self.frm.pack(expand=True)

        # Logo
        logo_path = resource_path("app/src/Logo.png")
        self.imagem = tk.PhotoImage(file=logo_path)
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
    
    def toggle_fullscreen(self, event=None):
        """Alterna entre tela cheia e janela normal"""
        current_state = self.janela.attributes('-fullscreen')
        self.janela.attributes('-fullscreen', not current_state)


def iniciarTela():
    app = tb.Window(themename="litera")
    Tela(app)
    app.mainloop()