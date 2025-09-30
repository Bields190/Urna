import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Tela de Resultados")
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")

        self.lbl_ini = tk.Label(self.janela, text="Resultados - {Eleição #}", font=("Arial", 35, "bold"), bg="white")
        self.lbl_ini.pack(pady=15)

        self.frm_resultados=tk.Frame(self.janela, bg="white", width=1500, height=850, highlightthickness=1, highlightbackground="black")
        self.frm_resultados.pack(pady=(25,20))  
        self.frm_resultados.pack_propagate(False)

        self.lbl_vencedor = tk.Label(self.frm_resultados, text="🏆 Chapa Vencedora", font=("Arial", 25, "bold"), bg="white")
        self.lbl_vencedor.pack(pady=15)

        self.frm_vencedor = tk.Frame(self.frm_resultados, bg="white")
        self.frm_vencedor.pack(pady=10)

        img = Image.new("RGB", (150, 150), color="gray")
        self.img_vencedor = ImageTk.PhotoImage(img)

        self.lbl_img = tk.Label(self.frm_vencedor, image=self.img_vencedor, bg="white", highlightthickness=1, highlightbackground="black")
        self.lbl_img.grid(row=0, column=0, rowspan=2, padx=20)

app = tk.Tk()
Tela(app)
app.mainloop()