import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Tela de Resultados")
        self.janela.geometry("1920x1080")

        #título
        self.lbl_ini = ttk.Label(
            self.janela,
            text="Resultados - {Eleição #}",
            font=("Arial", 35, "bold"),
            bootstyle=DARK
        )
        self.lbl_ini.pack(pady=15)

        #quadro principal
        self.frm_resultados = ttk.Frame(
            self.janela,
            bootstyle="#ffffff",
            width=1500,
            height=850
        )
        self.frm_resultados.pack(pady=(25,20))
        self.frm_resultados.pack_propagate(False)

        #vencedor
        self.lbl_vencedor = ttk.Label(
            self.frm_resultados,
            text="🏆 Chapa Vencedora",
            font=("Arial", 25, "bold"),
            bootstyle=DARK
        )
        self.lbl_vencedor.pack(pady=15)

        self.frm_vencedor = ttk.Frame(self.frm_resultados, bootstyle="#ffffff")
        self.frm_vencedor.pack(pady=10)

        #IMPORTANTE: mudar depois para a imagem da chapa vencedora
        img = Image.new("RGB", (150, 150), color="gray")
        self.img_vencedor = ImageTk.PhotoImage(img)

        self.lbl_img = ttk.Label(
            self.frm_vencedor,
            image=self.img_vencedor,
            bootstyle="#ffffff"
        )
        self.lbl_img.grid(row=0, column=0, rowspan=2, padx=20)

        self.lbl_nome_vencedor = ttk.Label(
            self.frm_vencedor,
            text="[Nome da Chapa]",
            font=("Arial", 30, "bold"),
            bootstyle=DARK
        )
        self.lbl_nome_vencedor.grid(row=0, column=1, sticky="w")

        self.lbl_percent_vencedor = ttk.Label(
            self.frm_vencedor,
            text="[XX% dos votos]",
            font=("Arial", 22),
            bootstyle=DARK
        )
        self.lbl_percent_vencedor.grid(row=1, column=1, sticky="w")

        #container inferior
        self.frm_inferior = ttk.Frame(self.frm_resultados, bootstyle="#ffffff")
        self.frm_inferior.pack(pady=60)

        #quadro das demais chapas
        self.frm_chapas = ttk.Labelframe(
            self.frm_inferior,
            text="Demais Chapas",
            bootstyle=DARK,
            width=500,
            height=350
        )
        self.frm_chapas.pack(side="left", padx=60)
        self.frm_chapas.pack_propagate(False)

        for i in range(4):
            self.lbl_chapas_pos = ttk.Label(
                self.frm_chapas,
                text=f"[Chapa {i+1}]   [XX%]",
                font=("Arial", 20),
                bootstyle=DARK
            )
            self.lbl_chapas_pos.pack(anchor="w", padx=30, pady=10)

        #quadro total de votos
        self.frm_votos = ttk.Labelframe(
            self.frm_inferior,
            text="Total de Votos",
            bootstyle=DARK,
            width=500,
            height=350
        )
        self.frm_votos.pack(side="left", padx=60)
        self.frm_votos.pack_propagate(False)

        self.lbl_total_votos_nmr = ttk.Label(
            self.frm_votos,
            text="[000]",
            font=("Arial", 60, "bold"),
            bootstyle=DARK
        )
        self.lbl_total_votos_nmr.pack(pady=50)


app = ttk.Window(themename="litera")
Tela(app)
app.mainloop()