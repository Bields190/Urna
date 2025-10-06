import ttkbootstrap as tb
from ttkbootstrap import ttk
from PIL import Image, ImageTk
import sys, os
from PIL import Image, ImageTk
import tkinter as tk

# importa os modelos
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))
import m_cedula  # type: ignore
import m_voto  # type: ignore

# importa o controlador
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_eleicao  # type: ignore

# importa outras telas
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'view'))
import telaEleicoes  # type: ignore
import telaCedulaVirtual  # type: ignore


class TelaVotacao:
    def __init__(self, master, eleicao_id=None, titulo="Eleição", email_votante=None):
        self.janela = master
        self.eleicao_id = eleicao_id
        self.titulo = titulo
        self.email_votante = email_votante
        self.control = c_eleicao.Control(self)
        self.chapa_atual = None
        self.cedula = None 

        # título
        try:
            self.janela.title(f"Tela de Votação - {titulo}")
        except Exception:
            pass

        # bind ESC
        self.janela.bind("<Escape>", self.voltar_para_eleicoes)

        # Frame principal
        frmPrincipal = ttk.Frame(self.janela, padding=20)
        frmPrincipal.pack(fill="both", expand=True)

        #Topo
        frmTopo = ttk.Frame(frmPrincipal)
        frmTopo.pack(fill="both", pady=20)

        self.labelEleicao = ttk.Label(
            frmTopo, text=f"{titulo}",
            font=("Courier", 26, "bold")
        )
        self.labelEleicao.pack(side="left", padx=45)

        # Info do votante (mascarado)
        email_mascarado = self.mascarar_email(email_votante) if email_votante else "N/A"
        self.labelVotante = ttk.Label(
            frmTopo, text=f"Votante: {email_mascarado}",
            font=("Courier", 14)
        )
        self.labelVotante.pack(side="right", padx=45)

        # Número da chapa
        frmNumero = ttk.Frame(frmPrincipal)
        frmNumero.pack(pady=(30, 20))

        self.lblInserirNumero = ttk.Label(
            frmNumero, text="Escreva o número da chapa:",
            font=("Courier", 18)
        )
        self.lblInserirNumero.pack()

        vcmd = self.janela.register(self.validar_dois_digitos)
        self.entInserirNumero = ttk.Entry(
            frmNumero, font=("Courier", 14), width=10,
            validate="key", validatecommand=(vcmd, "%P")
        )
        self.entInserirNumero.pack(pady=10, ipady=3)
        self.entInserirNumero.bind("<Return>", self.buscar_chapa)
        self.entInserirNumero.bind("<KeyRelease>", self.buscar_automatico)
        self.entInserirNumero.bind("<Escape>", self.voltar_para_eleicoes)

        #Frame de informações da chapa
        frmChapa = ttk.Frame(frmPrincipal)
        frmChapa.pack(pady=5, expand=True)

        self.frmFoto = ttk.Labelframe(frmChapa, text="Logo da Chapa", bootstyle="secondary", width=400, height=400)
        self.frmFoto.pack(side="left", padx=50, pady=10)
        self.frmFoto.pack_propagate(False)

        # Label para exibir a imagem
        self.lblFoto = ttk.Label(self.frmFoto)
        self.lblFoto.pack(expand=True, fill="both", padx=10, pady=10)

        frmInformacoes = ttk.Frame(frmChapa)
        frmInformacoes.pack(side="left", padx=20)

        self.frmSlogan = ttk.Frame(frmInformacoes, width=600, height=80, relief="ridge")
        self.frmSlogan.pack(pady=10)
        self.frmSlogan.pack_propagate(False)

        self.frmInfoChapa = ttk.Frame(frmInformacoes, width=600, height=200, relief="ridge")
        self.frmInfoChapa.pack(pady=10)
        self.frmInfoChapa.pack_propagate(False)

        self.lblSlogan = ttk.Label(self.frmSlogan, text="", font=("Courier", 18, "bold"))
        self.lblSlogan.pack(expand=True)

        self.lblInfo = ttk.Label(self.frmInfoChapa, text="", font=("Courier", 18,"bold"), wraplength=580, justify="left")
        self.lblInfo.pack(expand=True)

        #Botões
        frmConfirmacao = ttk.Frame(frmPrincipal)
        frmConfirmacao.pack(pady=(30, 150))

        self.btnConfirmar = ttk.Button(frmConfirmacao, text="Confirmar",bootstyle="success", width=20,command=self.confirmar_voto, state="disabled")
        self.btnConfirmar.pack(side="left", padx=40)

        self.btnCancelar = ttk.Button(frmConfirmacao, text="Cancelar",bootstyle="danger", width=20,command=self.cancelar_voto, state="disabled")
        self.btnCancelar.pack(side="left", padx=40)

    def limpar_campo(self):
        """Limpa o campo de entrada"""
        self.entInserirNumero.delete(0, tk.END)
        self.limpar_exibicao_chapa()

    def mascarar_email(self, email):
        """Mascara o email para preservar privacidade"""
        if not email or '@' not in email:
            return email
        
        partes = email.split('@')
        usuario = partes[0]
        dominio = partes[1]
        
        if len(usuario) <= 3:
            usuario_mascarado = usuario[0] + '*' * (len(usuario) - 1)
        else:
            usuario_mascarado = usuario[:2] + '*' * (len(usuario) - 4) + usuario[-2:]
        
        return f"{usuario_mascarado}@{dominio}"

    def carregar_imagem(self, caminho_imagem):
        """Carrega e redimensiona uma imagem para exibição"""
        try:
            # Primeiro tenta carregar a imagem da chapa
            if caminho_imagem and os.path.exists(caminho_imagem):
                # Carregar a imagem da chapa
                image = Image.open(caminho_imagem)
            else:
                # Se não tem imagem da chapa, usar logo da urna como fallback
                logo_urna_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'Logo.png')
                if os.path.exists(logo_urna_path):
                    image = Image.open(logo_urna_path)
                else:
                    # Se nem a logo da urna existir, mostrar mensagem
                    self.lblFoto.config(
                        text="SEM LOGO\nDISPONÍVEL", 
                        image="", 
                        compound="center",
                        font=("Courier", 16, "bold"),
                        foreground="gray"
                    )
                    if hasattr(self.lblFoto, 'image'):
                        self.lblFoto.image = None
                    return
            
            # Redimensionar mantendo proporção (máximo 350x350)
            image.thumbnail((350, 350), Image.Resampling.LANCZOS)
            
            # Converter para formato que o tkinter aceita
            photo = ImageTk.PhotoImage(image)
            
            # Exibir a imagem
            self.lblFoto.config(image=photo, text="", foreground="black")
            self.lblFoto.image = photo  # Manter referência para evitar garbage collection
            
        except Exception as e:
            print(f"Erro ao carregar imagem {caminho_imagem}: {e}")
            # Em caso de erro, tentar logo da urna como último recurso
            try:
                logo_urna_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'Logo.png')
                if os.path.exists(logo_urna_path):
                    image = Image.open(logo_urna_path)
                    image.thumbnail((350, 350), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(image)
                    self.lblFoto.config(image=photo, text="", foreground="black")
                    self.lblFoto.image = photo
                else:
                    # Se nada funcionar, mostrar mensagem de erro
                    self.lblFoto.config(
                        text="ERRO AO\nCARREGAR\nLOGO", 
                        image="", 
                        compound="center",
                        font=("Courier", 14, "bold"),
                        foreground="red"
                    )
                    if hasattr(self.lblFoto, 'image'):
                        self.lblFoto.image = None
            except Exception:
                self.lblFoto.config(
                    text="ERRO AO\nCARREGAR\nLOGO", 
                    image="", 
                    compound="center",
                    font=("Courier", 14, "bold"),
                    foreground="red"
                )
                if hasattr(self.lblFoto, 'image'):
                    self.lblFoto.image = None

    def validar_dois_digitos(self, valor):
        """Valida que apenas números com no máximo 2 dígitos sejam digitados"""
        if valor == "":
            return True
        # Só aceita números e no máximo 2 dígitos
        return valor.isdigit() and len(valor) <= 2

    def buscar_automatico(self, event=None):
        """Busca automaticamente quando 2 dígitos são digitados"""
        numero_digitado = self.entInserirNumero.get().strip()
        
        if len(numero_digitado) == 2:
            # Quando chegar a 2 dígitos, busca automaticamente
            self.buscar_chapa()
        elif len(numero_digitado) < 2:
            # Se tem menos de 2 dígitos, limpa a exibição
            self.limpar_exibicao_chapa()

    def limpar_exibicao_chapa(self):
        """Limpa a exibição da chapa"""
        self.chapa_atual = None
        self.lblSlogan.config(text="")
        self.lblInfo.config(text="")
        self.carregar_imagem(None)  # Limpar imagem
        self.btnConfirmar.config(state="disabled")
        self.btnCancelar.config(state="disabled")

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
            self.lblInfo.config(text=f"Nome: {nome}\nNúmero: {numero}")

            # Carregar a logo da chapa
            if logo:
                # Verificar se é caminho absoluto ou relativo
                if not os.path.isabs(logo):
                    # Se for relativo, procurar em app/src/
                    logo_path = os.path.join(os.path.dirname(__file__), '..', 'src', logo)
                    if not os.path.exists(logo_path):
                        # Tentar na raiz do projeto
                        logo_path = os.path.join(os.path.dirname(__file__), '..', '..', logo)
                else:
                    logo_path = logo
                    
                self.carregar_imagem(logo_path)
            else:
                self.carregar_imagem(None)
            
            self.btnConfirmar.config(state="normal")
            self.btnCancelar.config(state="normal")
        else:
            self.lblSlogan.config(text="Chapa não encontrada")
            self.lblInfo.config(text="")
            self.carregar_imagem(None)  # Limpar imagem
            self.btnConfirmar.config(state="disabled")
            self.btnCancelar.config(state="disabled")

    def confirmar_voto(self):
        if self.chapa_atual and self.email_votante:
            _, nome, slogan, logo, numero = self.chapa_atual
            
            try:
                # Criar uma nova cédula com o email do votante
                cedula = m_cedula.Cedula(self.eleicao_id, self.email_votante)
                if cedula.salvar():
                    # Criar o voto associado à cédula
                    voto = m_voto.Voto(
                        self.eleicao_id,
                        self.chapa_atual[0],  # ID da chapa
                        cedula.id
                    )
                    
                    if voto.salvar():
                        # Limpar a tela e ir para a cédula virtual
                        for widget in self.janela.winfo_children():
                            widget.destroy()
                        
                        # Redirecionar para a cédula virtual
                        telaCedulaVirtual.iniciarTela(
                            self.janela, 
                            self.eleicao_id,
                            self.titulo,
                            cedula.id,
                            self.email_votante
                        )
                    else:
                        self.lblSlogan.config(text="Erro ao salvar o voto!")
                        self.lblInfo.config(text="Tente novamente.")
                else:
                    self.lblSlogan.config(text="Erro ao criar cédula!")
                    self.lblInfo.config(text="Tente novamente.")
                    
            except Exception as e:
                print(f"Erro ao confirmar voto: {e}")
                self.lblSlogan.config(text="Erro ao processar voto!")
                self.lblInfo.config(text="Tente novamente.")
        else:
            self.lblSlogan.config(text="Dados insuficientes para o voto!")
            self.lblInfo.config(text="Selecione uma chapa e verifique o email.")

    def cancelar_voto(self):
        self.chapa_atual = None
        self.entInserirNumero.delete(0, "end")
        self.lblSlogan.config(text="")
        self.lblInfo.config(text="")
        self.lblFoto.config(text="", image="")
        self.btnConfirmar.config(state="disabled")
        self.btnCancelar.config(state="disabled")

    def voltar_para_eleicoes(self, event=None):

        for widget in self.janela.winfo_children():
            widget.destroy()
        telaEleicoes.iniciarTela(self.janela)


def iniciarTela(master=None, eleicao_id=None, titulo="Eleição", email_votante=None):
    if master is None:
        app = tb.Window(themename="superhero")
        TelaVotacao(app, eleicao_id, titulo, email_votante)
        app.mainloop()
    else:
        TelaVotacao(master, eleicao_id, titulo, email_votante)
