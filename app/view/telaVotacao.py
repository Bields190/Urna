import ttkbootstrap as tb
from ttkbootstrap import ttk
import sys, os

# importa o controlador
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_eleicao  # type: ignore

# importa a tela de eleições
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'view'))
import telaEleicoes  # type: ignore


class TelaVotacao:
    def __init__(self, master, eleicao_id=None, titulo="Eleição"):
        self.janela = master
        self.eleicao_id = eleicao_id
        self.control = c_eleicao.Control(self)
        self.chapa_atual = None 

        try:
            self.janela.title(f"Tela de Votação - {titulo}")
        except Exception:
            pass


        self.janela.bind("<Escape>", self.voltar_para_eleicoes)

        # Frame principal
        frmPrincipal = ttk.Frame(self.janela, padding=20)
        frmPrincipal.pack(fill="both", expand=True)

        # Topo
        frmTopo = ttk.Frame(frmPrincipal)
        frmTopo.pack(fill="both", pady=20)

        self.labelEleicao = ttk.Label(
            frmTopo, text=f"{titulo} (ID: {eleicao_id})",
            font=("Courier", 26, "bold")
        )
        self.labelEleicao.pack(side="left", padx=45)

        # Número da chapa
        frmNumero = ttk.Frame(frmPrincipal)
        frmNumero.pack(pady=(30, 20))

        self.lblInserirNumero = ttk.Label(
            frmNumero, text="Escreva o número da chapa:",
            font=("Courier", 18)
        )
        self.lblInserirNumero.pack()

        vcmd = self.janela.register(self.validar_inteiro)
        self.entInserirNumero = ttk.Entry(
            frmNumero, font=("Courier", 14), width=10,
            validate="key", validatecommand=(vcmd, "%P")
        )
        self.entInserirNumero.pack(pady=10, ipady=3)
        self.entInserirNumero.bind("<Return>", self.buscar_chapa)
        self.entInserirNumero.bind("<Escape>", self.voltar_para_eleicoes)

        # Informações do voto
        frmChapa = ttk.Frame(frmPrincipal)
        frmChapa.pack(pady=5, expand=True)

        self.frmFoto = ttk.Labelframe(frmChapa, text="", bootstyle="secondary", width=400, height=400)
        self.frmFoto.pack(side="left", padx=50, pady=10)
        self.frmFoto.pack_propagate(False)

        frmInformacoes = ttk.Frame(frmChapa)
        frmInformacoes.pack(side="left", padx=20)

        self.frmSlogan = ttk.Frame(frmInformacoes, width=600, height=80, relief="ridge")
        self.frmSlogan.pack(pady=10)
        self.frmSlogan.pack_propagate(False)

        self.frmInfoChapa = ttk.Frame(frmInformacoes, width=600, height=200, relief="ridge")
        self.frmInfoChapa.pack(pady=10)
        self.frmInfoChapa.pack_propagate(False)

        self.lblSlogan = ttk.Label(self.frmSlogan, text="", font=("Courier", 14, "italic"))
        self.lblSlogan.pack(expand=True)

        self.lblInfo = ttk.Label(self.frmInfoChapa, text="", font=("Courier", 14), wraplength=580, justify="left")
        self.lblInfo.pack(expand=True)

        # Botões
        frmConfirmacao = ttk.Frame(frmPrincipal)
        frmConfirmacao.pack(pady=(30, 150))

        self.btnConfirmar = ttk.Button(
            frmConfirmacao, text="Confirmar",
            bootstyle="success", width=20,
            command=self.confirmar_voto, state="disabled"
        )
        self.btnConfirmar.pack(side="left", padx=40)

        self.btnCancelar = ttk.Button(
            frmConfirmacao, text="Cancelar",
            bootstyle="danger", width=20,
            command=self.cancelar_voto, state="disabled"
        )
        self.btnCancelar.pack(side="left", padx=40)

    def validar_inteiro(self, valor):
        if valor == "":
            return True
        return valor.isdigit()

    def buscar_chapa(self, event=None):
        numero_digitado = self.entInserirNumero.get().strip()
        if not numero_digitado:
            return

        chapas = self.control.listar_chapas_por_eleicao(self.eleicao_id) or []
        self.chapa_atual = None

        for chapa in chapas:
            if len(chapa) >= 5 and str(chapa[4]) == numero_digitado:
                self.chapa_atual = chapa
                break

        if self.chapa_atual:
            _, nome, slogan, logo, numero = self.chapa_atual
            self.lblSlogan.config(text=slogan or "Sem slogan")
            self.lblInfo.config(text=f"Nome: {nome}\nNúmero: {numero}\nLogo: {logo or 'Sem logo'}")

            
            self.btnConfirmar.config(state="normal")
            self.btnCancelar.config(state="normal")
        else:
            self.lblSlogan.config(text="Chapa não encontrada")
            self.lblInfo.config(text="")
            self.btnConfirmar.config(state="disabled")
            self.btnCancelar.config(state="disabled")

    def confirmar_voto(self):
        if self.chapa_atual:
            _, nome, slogan, logo, numero = self.chapa_atual
            print(f"✅ Voto confirmado para a chapa {nome} (número {numero})")
            
            self.btnConfirmar.config(state="disabled")
            self.btnCancelar.config(state="disabled")
            self.lblSlogan.config(text="Voto registrado com sucesso!")
            self.lblInfo.config(text="")

    def cancelar_voto(self):

        self.chapa_atual = None
        self.entInserirNumero.delete(0, "end")
        self.lblSlogan.config(text="")
        self.lblInfo.config(text="")
        self.btnConfirmar.config(state="disabled")
        self.btnCancelar.config(state="disabled")

    def voltar_para_eleicoes(self, event=None):
        for widget in self.janela.winfo_children():
            widget.destroy()

        telaEleicoes.iniciarTela(self.janela)


def iniciarTela(master=None, eleicao_id=None):
    if master is None:
        app = tb.Window(themename="superhero")
        TelaVotacao(app, eleicao_id)
        app.mainloop()
    else:
        TelaVotacao(master, eleicao_id)
