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
        # Ajuste de resolução — opcional, você pode alterar
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

    def _resolve_path(self, p):
        """Resolve caminhos relativos/absolutos para a logo."""
        if not p:
            return None
        # Se já for absoluto
        if os.path.isabs(p):
            return p if os.path.exists(p) else None
        # Tenta candidatos comuns
        candidates = [
            os.path.abspath(p),
            os.path.join(os.path.dirname(__file__), p),
            os.path.join(os.getcwd(), p)
        ]
        for c in candidates:
            if os.path.exists(c):
                return c
        return None

    def mostrar_resultados(self):
        chapas = self.dados.get('chapas', []) if isinstance(self.dados, dict) else []
        total_votos = self.dados.get('total_votos', 0) if isinstance(self.dados, dict) else 0

        # vencedor (primeiro da lista ordenada)
        vencedor = chapas[0] if chapas else None

        self.lbl_vencedor = ttk.Label(self.frm_resultados, text="🏆 Chapa Vencedora", font=("Courier", 25, "bold"), bootstyle=DARK)
        self.lbl_vencedor.pack(pady=15)

        self.frm_vencedor = ttk.Frame(self.frm_resultados, bootstyle="#ffffff")
        self.frm_vencedor.pack(pady=10)

        # Limpar possíveis widgets anteriores
        for w in self.frm_vencedor.winfo_children():
            w.destroy()

        if vencedor:
            logo_path = self._resolve_path(vencedor.get('logo'))
            try:
                if logo_path:
                    img = Image.open(logo_path).resize((150,150))
                else:
                    img = Image.new("RGB", (150, 150), color="gray")
            except Exception:
                img = Image.new("RGB", (150, 150), color="gray")

            self.img_vencedor = ImageTk.PhotoImage(img)

            self.lbl_img = ttk.Label(self.frm_vencedor, image=self.img_vencedor, bootstyle="#ffffff")
            self.lbl_img.grid(row=0, column=0, rowspan=2, padx=20)

            self.lbl_nome_vencedor = ttk.Label(self.frm_vencedor, text=vencedor.get('nome', '—'), font=("Arial", 30, "bold"), bootstyle=DARK)
            self.lbl_nome_vencedor.grid(row=0, column=1, sticky="w")

            votos_vencedor = vencedor.get('votos', 0)
            perc_vencedor = vencedor.get('percentual', 0)
            resultado_text = f"{votos_vencedor} votos ({perc_vencedor:.2f}%)"
            self.lbl_percent_vencedor = ttk.Label(self.frm_vencedor, text=resultado_text, font=("Arial", 22), bootstyle=DARK)
            self.lbl_percent_vencedor.grid(row=1, column=1, sticky="w")
        else:
            lbl = ttk.Label(self.frm_vencedor, text="Nenhuma chapa encontrada para esta eleição.", font=("Arial", 18), bootstyle=DARK)
            lbl.pack()

        # área inferior (demais chapas + total de votos)
        # limpar antes
        for w in getattr(self, 'frm_inferior', []):
            try:
                w.destroy()
            except Exception:
                pass

        self.frm_inferior = ttk.Frame(self.frm_resultados, bootstyle="#ffffff")
        self.frm_inferior.pack(pady=60)

        # Demais chapas
        self.frm_chapas = ttk.Labelframe(self.frm_inferior, text="Demais Chapas", bootstyle=DARK, width=500, height=350)
        self.frm_chapas.pack(side="left", padx=60)
        self.frm_chapas.pack_propagate(False)

        # Exibir outras chapas (exceto o vencedor)
        outras = chapas[1:] if len(chapas) > 1 else []
        if not outras:
            lbl = ttk.Label(self.frm_chapas, text="Nenhuma outra chapa cadastrada.", font=("Arial", 16), bootstyle=DARK)
            lbl.pack(anchor="w", padx=30, pady=10)
        else:
            for chapa in outras:
                nome = chapa.get('nome', '—')
                votos = chapa.get('votos', 0)
                perc = chapa.get('percentual', 0)
                lbl = ttk.Label(self.frm_chapas, text=f"{nome} - {votos} votos ({perc:.2f}%)", font=("Arial", 20), bootstyle=DARK)
                lbl.pack(anchor="w", padx=30, pady=10)

        # Total de votos
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