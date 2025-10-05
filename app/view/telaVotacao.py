import ttkbootstrap as tb
from ttkbootstrap import ttk
import ttkbootstrap as tb
from ttkbootstrap import ttk


class TelaVotacao:
    def __init__(self, master, eleicao_id=None, titulo="Eleição"):
        self.janela = master
        self.janela.title("Tela de Votação")
        self.janela.title("Tela de Votação")
        self.janela.geometry("1920x1080")

        # Frame principal
        frmPrincipal = ttk.Frame(self.janela, padding=20)
        # Frame principal
        frmPrincipal = ttk.Frame(self.janela, padding=20)
        frmPrincipal.pack(fill="both", expand=True)

        # Topo
        frmTopo = ttk.Frame(frmPrincipal)
        # Topo
        frmTopo = ttk.Frame(frmPrincipal)
        frmTopo.pack(fill="both", pady=20)

        self.labelEleicao = ttk.Label(
            frmTopo, text=f"{titulo} (ID: {eleicao_id})",
            font=("Courier", 26, "bold")
        )
        self.labelEleicao = ttk.Label(
            frmTopo, text=f"{titulo} (ID: {eleicao_id})",
            font=("Courier", 26, "bold")
        )
        self.labelEleicao.pack(side="left", padx=45)

        # Número da chapa
        frmNumero = ttk.Frame(frmPrincipal)
        frmNumero.pack(pady=(30, 20))
        # Número da chapa
        frmNumero = ttk.Frame(frmPrincipal)
        frmNumero.pack(pady=(30, 20))

        self.lblInserirNumero = ttk.Label(
            frmNumero, text="Escreva o número da chapa:",
            font=("Courier", 18)
        )
        self.lblInserirNumero = ttk.Label(
            frmNumero, text="Escreva o número da chapa:",
            font=("Courier", 18)
        )
        self.lblInserirNumero.pack()

        self.entInserirNumero = ttk.Entry(frmNumero, font=("Courier", 14), width=10)
        self.entInserirNumero = ttk.Entry(frmNumero, font=("Courier", 14), width=10)
        self.entInserirNumero.pack(pady=10, ipady=3)

        # Informações do voto
        frmChapa = ttk.Frame(frmPrincipal)
        # Informações do voto
        frmChapa = ttk.Frame(frmPrincipal)
        frmChapa.pack(pady=5, expand=True)

        # Foto chapa
        self.frmFoto = ttk.Frame(frmChapa, width=400, height=400)
        # Foto chapa
        self.frmFoto = ttk.Frame(frmChapa, width=400, height=400)
        self.frmFoto.pack(side="left", padx=50)
        self.frmFoto.pack_propagate(False)

        # Info + slogan
        frmInformacoes = ttk.Frame(frmChapa)
        # Info + slogan
        frmInformacoes = ttk.Frame(frmChapa)
        frmInformacoes.pack(side="left", padx=20)

        self.frmSlogan = ttk.Frame(frmInformacoes, width=600, height=80, relief="ridge")
        self.frmSlogan = ttk.Frame(frmInformacoes, width=600, height=80, relief="ridge")
        self.frmSlogan.pack(pady=10)
        self.frmSlogan.pack_propagate(False)

        self.frmInfoChapa = ttk.Frame(frmInformacoes, width=600, height=200, relief="ridge")
        self.frmInfoChapa = ttk.Frame(frmInformacoes, width=600, height=200, relief="ridge")
        self.frmInfoChapa.pack(pady=10)
        self.frmInfoChapa.pack_propagate(False)

        # Botões de confirmação
        frmConfirmacao = ttk.Frame(frmPrincipal)
        frmConfirmacao.pack(pady=(30, 150))
        # Botões de confirmação
        frmConfirmacao = ttk.Frame(frmPrincipal)
        frmConfirmacao.pack(pady=(30, 150))

        self.btnConfirmar = ttk.Button(
            frmConfirmacao, text="Confirmar",
            bootstyle="success", width=20
        )
        self.btnConfirmar = ttk.Button(
            frmConfirmacao, text="Confirmar",
            bootstyle="success", width=20
        )
        self.btnConfirmar.pack(side="left", padx=40)

        self.btnCancelar = ttk.Button(
            frmConfirmacao, text="Cancelar",
            bootstyle="danger", width=20,
            command=self.janela.destroy
        )
        self.btnCancelar = ttk.Button(
            frmConfirmacao, text="Cancelar",
            bootstyle="danger", width=20,
            command=self.janela.destroy
        )
        self.btnCancelar.pack(side="left", padx=40)


def iniciarTela(eleicao_id=None, titulo="Eleição"):
    app = tb.Window(themename="litera")
    TelaVotacao(app, eleicao_id, titulo)
    app.mainloop()