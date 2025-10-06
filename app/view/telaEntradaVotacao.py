import ttkbootstrap as tb
from ttkbootstrap import ttk
import sys, os
import re

# importa o controlador
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_eleicao  # type: ignore

# importa outras telas
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'view'))
import telaVotacao  # type: ignore
import telaEleicoes  # type: ignore


class TelaEntradaVotacao:
    def __init__(self, master, eleicao_id=None, titulo="Eleição"):
        self.janela = master
        self.eleicao_id = eleicao_id
        self.titulo = titulo
        self.control = c_eleicao.Control(self)

        try:
            self.janela.title('Urna Eletrônica - Entrada para Votação')
            # Configura para tela cheia
            self.janela.attributes('-fullscreen', True)
        except Exception:
            pass

        # Bind especial para sair: Ctrl+Alt+X
        self.janela.bind("<Control-Alt-x>", lambda e: self.voltar_para_eleicoes())

        # Frame principal
        frmPrincipal = ttk.Frame(self.janela, padding=20)
        frmPrincipal.pack(fill="both", expand=True)

        # Topo
        frmTopo = ttk.Frame(frmPrincipal)
        frmTopo.pack(fill="both", pady=50)

        # Título da eleição
        self.labelEleicao = ttk.Label(
            frmTopo, text=f"{titulo}",
            font=("Courier", 32, "bold")
        )
        self.labelEleicao.pack()

        # Centro - Formulário de entrada
        frmCentro = ttk.Frame(frmPrincipal)
        frmCentro.pack(expand=True)

        # Frame para centralizar o conteúdo
        frmEntrada = ttk.LabelFrame(frmCentro, text="Entrada para Votação", padding=40)
        frmEntrada.pack(expand=True)

        # Instrução
        lblInstrucao = ttk.Label(
            frmEntrada, 
            text="Para votar, digite seu email institucional:",
            font=("Courier", 20)
        )
        lblInstrucao.pack(pady=20)

        # Campo de email
        self.entEmail = ttk.Entry(
            frmEntrada, 
            font=("Courier", 16), 
            width=40,
            justify="center"
        )
        self.entEmail.pack(pady=20, ipady=8)
        self.entEmail.bind("<Return>", self.validar_e_entrar)
        self.entEmail.focus()

        # Label para mensagens de erro
        self.lblMensagem = ttk.Label(
            frmEntrada, 
            text="",
            font=("Courier", 14),
            foreground="red"
        )
        self.lblMensagem.pack(pady=10)

        # Botões
        frmBotoes = ttk.Frame(frmEntrada)
        frmBotoes.pack(pady=30)

        self.btnEntrar = ttk.Button(
            frmBotoes, 
            text="Entrar para Votar",
            bootstyle="success", 
            width=20,
            command=self.validar_e_entrar
        )
        self.btnEntrar.pack(side="left", padx=20)

        self.btnVoltar = ttk.Button(
            frmBotoes, 
            text="Voltar",
            bootstyle="secondary", 
            width=15,
            command=self.voltar_para_eleicoes
        )
        self.btnVoltar.pack(side="left", padx=20)

    def validar_email(self, email):
        """Valida se o email tem formato institucional válido"""
        if not email:
            return False, "Email é obrigatório"
        
        # Padrão básico para email institucional (pode ser ajustado conforme necessário)
        padrao = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(padrao, email):
            return False, "Formato de email inválido"
        
        # Verifica se é um email institucional (contém domínio educacional)
        dominios_institucionais = ['ufac.br', 'edu.br', 'ac.gov.br']
        dominio = email.split('@')[1].lower() if '@' in email else ''
        
        if not any(dom in dominio for dom in dominios_institucionais):
            return False, "Use um email institucional (@ufac.br, @edu.br, etc.)"
        
        return True, ""

    def validar_e_entrar(self, event=None):
        """Valida o email e direciona para a tela de votação"""
        email = self.entEmail.get().strip().lower()
        
        valido, mensagem = self.validar_email(email)
        
        if not valido:
            self.lblMensagem.config(text=mensagem, foreground="red")
            self.entEmail.focus()
            return
        
        # Verifica se o email já votou nesta eleição
        if self.verificar_email_ja_votou(email):
            self.lblMensagem.config(
                text="Este email já votou nesta eleição!", 
                foreground="red"
            )
            self.entEmail.focus()
            return
        
        # Email válido, prosseguir para votação
        self.lblMensagem.config(text="")
        self.ir_para_votacao(email)

    def verificar_email_ja_votou(self, email):
        """Verifica se o email já votou nesta eleição"""
        try:
            # Consulta no banco para verificar se já existe uma cédula com este email
            from model import Model
            db = Model()
            
            sql = f"""
                SELECT COUNT(*) 
                FROM cedula 
                WHERE eleicao_id = {self.eleicao_id} 
                AND email_votante = '{email}'
            """
            
            resultado = db.get(sql)
            return resultado[0][0] > 0 if resultado else False
            
        except Exception as e:
            print(f"Erro ao verificar voto: {e}")
            return False

    def ir_para_votacao(self, email):
        """Limpa a tela e vai para a tela de votação"""
        # Limpa todos os widgets da janela
        for widget in self.janela.winfo_children():
            widget.destroy()
        
        # Inicia a tela de votação passando o email do votante
        telaVotacao.iniciarTela(self.janela, self.eleicao_id, self.titulo, email)

    def voltar_para_eleicoes(self, event=None):
        """Volta para a tela de eleições"""
        for widget in self.janela.winfo_children():
            widget.destroy()
        
        telaEleicoes.iniciarTela(self.janela)


def iniciarTela(master=None, eleicao_id=None, titulo="Eleição"):
    """Função para iniciar a tela de entrada para votação"""
    if master is None:
        app = tb.Window(themename="superhero")
        TelaEntradaVotacao(app, eleicao_id, titulo)
        app.mainloop()
    else:
        TelaEntradaVotacao(master, eleicao_id, titulo)