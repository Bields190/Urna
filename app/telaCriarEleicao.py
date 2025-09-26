import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Criação de Eleições')
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")

        self.lbl_topo = tk.Label(self.janela, text="Criar Eleição", font=("Arial", 24, "bold"), bg="white")
        self.lbl_topo.pack()

        self.frm_entrada = tk.Frame(self.janela, bg="white")
        self.frm_entrada.pack(pady=5)
        self.frm = tk.Frame(self.frm_entrada, bg='white')
        self.frm.pack(expand=True)

        self.lbl1 = tk.Label(self.frm_entrada, text='Título:', bg='white',font=("Arial",18))
        self.lbl1.pack(pady=(40, 0))
        self.entry1 = tk.Entry(self.frm_entrada, width=40)
        self.entry1.pack()

        self.lbl2 = tk.Label(self.frm, text='Data de Início:',bg='white',font=("Arial",18))
        self.lbl2.pack()
        self.entry2 = ttk.DateEntry(self.janela,
                                dateformat = '%d-%m-%Y',
                                 bootstyle=DARK
                                )
        self.entry2.pack(pady=5)

app = tk.Tk()
Tela(app)
app.mainloop()