import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_eleicao #type: ignore

import telaEleicoes

class Tela:
    def __init__(self, master, eleicao_id):
        self.janela = master
        self.janela.title("Tela de Resultados")
        self.janela.geometry("1920x1080")
        self.eleicao_id = eleicao_id

        # bind ESC
        self.janela.bind("<Escape>", lambda e: self.voltarEleicoes())

        # controlador
        self.control = c_eleicao.Control(self)

        # título
        self.lbl_ini = ttk.Label(
            self.janela,
            text=f"Resultados - Eleição #{eleicao_id}",
            font=("Courier", 35, "bold"),
            bootstyle=DARK
        )
        self.lbl_ini.pack(pady=15)

        # quadro principal
        self.frm_resultados = ttk.Frame(self.janela, bootstyle="#ffffff", width=1500, height=850)
        self.frm_resultados.pack(pady=(25,20))
        self.frm_resultados.pack_propagate(False)

        # pegar resultados
        self.dados = self.control.resultado_eleicao(eleicao_id)
        self.mostrar_resultados()

    def mostrar_resultados(self):
        chapas = self.dados['chapas']
        total_votos = self.dados['total_votos']

        # vencedor
        vencedor = chapas[0] if chapas else None

        self.lbl_vencedor = ttk.Label(self.frm_resultados, text="🏆 Chapa Vencedora", font=("Courier", 25, "bold"), bootstyle=DARK)
        self.lbl_vencedor.pack(pady=15)

        self.frm_vencedor = ttk.Frame(self.frm_resultados, bootstyle="#ffffff")
        self.frm_vencedor.pack(pady=10)

        if vencedor:
            # imagem
            if vencedor['logo'] and os.path.exists(vencedor['logo']):
                img = Image.open(vencedor['logo']).resize((150,150))
            else:
                img = Image.new("RGB", (150, 150), color="gray")
            self.img_vencedor = ImageTk.PhotoImage(img)

            self.lbl_img = ttk.Label(self.frm_vencedor, image=self.img_vencedor, bootstyle="#ffffff")
            self.lbl_img.grid(row=0, column=0, rowspan=2, padx=20)

            self.lbl_nome_vencedor = ttk.Label(self.frm_vencedor, text=vencedor['nome'], font=("Courier", 30, "bold"), bootstyle=DARK)
            self.lbl_nome_vencedor.grid(row=0, column=1, sticky="w")

            self.lbl_percent_vencedor = ttk.Label(self.frm_vencedor, text=f"{vencedor['percentual']:.2f}% dos votos", font=("Courier", 22), bootstyle=DARK)
            self.lbl_percent_vencedor.grid(row=1, column=1, sticky="w")

        # demais chapas
        self.frm_inferior = ttk.Frame(self.frm_resultados, bootstyle="#ffffff")
        self.frm_inferior.pack(pady=60)

        self.frm_chapas = ttk.Labelframe(self.frm_inferior, text="Demais Chapas", bootstyle=DARK, width=500, height=350)
        self.frm_chapas.pack(side="left", padx=60)
        self.frm_chapas.pack_propagate(False)

        for chapa in chapas[1:]:
            lbl = ttk.Label(self.frm_chapas, text=f"{chapa['nome']} - {chapa['percentual']:.2f}%", font=("Courier", 20), bootstyle=DARK)
            lbl.pack(anchor="w", padx=30, pady=10)

        # total de votos
        self.frm_votos = ttk.Labelframe(self.frm_inferior, text="Total de Votos", bootstyle=DARK, width=500, height=350)
        self.frm_votos.pack(side="left", padx=60)
        self.frm_votos.pack_propagate(False)

        self.lbl_total_votos_nmr = ttk.Label(self.frm_votos, text=str(total_votos), font=("Courier", 60, "bold"), bootstyle=DARK)
        self.lbl_total_votos_nmr.pack(pady=50)

    def voltarEleicoes(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaEleicoes.iniciarTela(self.janela)

def iniciarTela(master=None, eleicao_id=None):
    if master is None:
        app = ttk.Window(themename="superhero")
        Tela(app, eleicao_id)
        app.mainloop()
    else:
        Tela(master, eleicao_id)
