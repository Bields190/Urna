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

#------IMPORTANTE: modificar depois para a imagem da chapa campeã------
        img = Image.new("RGB", (150, 150), color="gray")
        self.img_vencedor = ImageTk.PhotoImage(img)

        self.lbl_img = tk.Label(self.frm_vencedor, image=self.img_vencedor, bg="white", highlightthickness=1, highlightbackground="black")
        self.lbl_img.grid(row=0, column=0, rowspan=2, padx=20)

        self.lbl_nome_vencedor = tk.Label(self.frm_vencedor, text="[Nome da Chapa]", font=("Arial", 30, "bold"), bg="white")
        self.lbl_nome_vencedor.grid(row=0, column=1, sticky="w")

        self.lbl_percent_vencedor = tk.Label(self.frm_vencedor, text="[XX% dos votos]", font=("Arial", 22), bg="white")
        self.lbl_percent_vencedor.grid(row=1, column=1, sticky="w")

        self.frm_inferior = tk.Frame(self.frm_resultados, bg="white")
        self.frm_inferior.pack(pady=60)

        self.frm_chapas = tk.Frame(self.frm_inferior, bg="white", width=500, height=350, highlightbackground="black", highlightthickness=1)
        self.frm_chapas.pack(side="left", padx=60)
        self.frm_chapas.pack_propagate(False)

        self.lbl_dms_chapas = tk.Label(self.frm_chapas, text="Demais Chapas", font=("Arial", 24, "bold"), bg="white")
        self.lbl_dms_chapas.pack(pady=15)

        for i in range(4):
            self.lbl_chapas_pos = tk.Label(self.frm_chapas, text=f"[Chapa {i+1}]   [XX%]", font=("Arial", 20), bg="white")
            self.lbl_chapas_pos.pack(anchor="w", padx=30, pady=10)

        self.frm_votos = tk.Frame(self.frm_inferior, bg="white", width=500, height=350, highlightbackground="black", highlightthickness=1)
        self.frm_votos.pack(side="left", padx=60)
        self.frm_votos.pack_propagate(False)

        self.lbl_total_votos = tk.Label(self.frm_votos, text="Total de Votos", font=("Arial", 25, "bold"), bg="white")
        self.lbl_total_votos.pack(pady=15)

        self.lbl_total_votos_nmr = tk.Label(self.frm_votos, text="[000]", font=("Arial", 60, "bold"), bg="white")
        self.lbl_total_votos_nmr.pack(pady=50)


app = tk.Tk()
Tela(app)
app.mainloop()