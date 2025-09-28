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
        self.lbl_topo.pack(pady=15)

        self.frm_entrada = tk.Frame(self.janela, bg="white")
        self.frm_entrada.pack(pady=5)

        self.lbl1 = tk.Label(self.frm_entrada, text='Título:', bg='white',font=("Arial",18))
        self.lbl1.pack(pady=(40, 0))
        self.entry1 = tk.Entry(self.frm_entrada, width=40)
        self.entry1.pack(pady=15)

        self.lbl2 = tk.Label(self.frm_entrada, text='Data de Início:', bg='white', font=("Arial",18))
        self.lbl2.pack()
        self.entry2 = ttk.DateEntry(self.frm_entrada, dateformat='%d-%m-%Y', bootstyle=DARK, width=36)
        self.entry2.pack(pady=15)

        self.lbl3 = tk.Label(self.frm_entrada, text='Data de Encerramento:', bg='white', font=("Arial",18))
        self.lbl3.pack()
        self.entry3 = ttk.DateEntry(self.frm_entrada, dateformat='%d-%m-%Y', bootstyle=DARK, width=36)
        self.entry3.pack(pady=15)

app = tk.Tk()
Tela(app)
app.mainloop()