import ttkbootstrap as tb
from ttkbootstrap import ttk
import sys, os
from datetime import datetime
import threading

# Para envio de email
try:
    import yagmail
    EMAIL_DISPONIVEL = True
except ImportError:
    EMAIL_DISPONIVEL = False
    print("⚠️ yagmail não disponível - funcionalidade de email desabilitada")

# importa outras telas
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'view'))
import telaEntradaVotacao  # type: ignore


class TelaCedulaVirtual:
    def __init__(self, master, eleicao_id=None, titulo="Eleição", cedula_id=None, email_votante=None):
        self.janela = master
        self.eleicao_id = eleicao_id
        self.titulo = titulo
        self.cedula_id = cedula_id
        self.email_votante = email_votante
        self.espaco_contador = 0  # Contador para tecla espaço
        self.email_enviado = False  # Flag para controlar se já foi enviado

        try:
            self.janela.title('Urna Eletrônica - Cédula Virtual')
            # Configura para tela cheia
            self.janela.attributes('-fullscreen', True)
        except Exception:
            pass

        # Bind especial para sair: Ctrl+Alt+X
        self.janela.bind("<Control-Alt-x>", lambda e: self.voltar_para_entrada())
        self.janela.bind("<KeyPress-space>", self.contar_espaco)
        self.janela.focus_set()  # Permite que a janela receba eventos de teclado

        # Frame principal
        frmPrincipal = ttk.Frame(self.janela, padding=20)
        frmPrincipal.pack(fill="both", expand=True)

        # Centro - Cédula Virtual
        frmCentro = ttk.Frame(frmPrincipal)
        frmCentro.pack(expand=True)

        # Frame da cédula com aparência de documento
        frmCedula = ttk.LabelFrame(
            frmCentro, 
            text="CÉDULA ELEITORAL VIRTUAL", 
            padding=50,
            bootstyle="info"
        )
        frmCedula.pack(expand=True, padx=100, pady=50)

        # Cabeçalho da cédula
        lblCabecalho = ttk.Label(
            frmCedula,
            text="COMPROVANTE DE VOTAÇÃO",
            font=("Courier", 24, "bold"),
            anchor="center"
        )
        lblCabecalho.pack(pady=20)

        # Informações da eleição
        lblEleicao = ttk.Label(
            frmCedula,
            text=f"Eleição: {titulo}",
            font=("Courier", 16),
            anchor="center"
        )
        lblEleicao.pack(pady=5)

        # Data e hora da votação
        data_hora_atual = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        lblDataHora = ttk.Label(
            frmCedula,
            text=f"Data/Hora: {data_hora_atual}",
            font=("Courier", 14),
            anchor="center"
        )
        lblDataHora.pack(pady=5)

        # ID da cédula
        lblCedulaId = ttk.Label(
            frmCedula,
            text=f"Cédula ID: {cedula_id or 'N/A'}",
            font=("Courier", 14),
            anchor="center"
        )
        lblCedulaId.pack(pady=5)

        # Separador
        separador = ttk.Separator(frmCedula, orient='horizontal')
        separador.pack(fill='x', pady=20)

        # Confirmação de voto
        lblConfirmacao = ttk.Label(
            frmCedula,
            text="✅ SEU VOTO FOI REGISTRADO COM SUCESSO",
            font=("Courier", 18, "bold"),
            foreground="green",
            anchor="center"
        )
        lblConfirmacao.pack(pady=20)

        # Mensagem sobre sigilo
        lblSigilo = ttk.Label(
            frmCedula,
            text="O voto é secreto e foi registrado de forma anônima.\nEste comprovante confirma apenas que você votou.",
            font=("Courier", 14),
            anchor="center",
            justify="center"
        )
        lblSigilo.pack(pady=15)

        # Email mascarado (para privacidade)
        email_mascarado = self.mascarar_email(email_votante) if email_votante else "N/A"
        lblEmail = ttk.Label(
            frmCedula,
            text=f"Votante: {email_mascarado}",
            font=("Courier", 12),
            anchor="center"
        )
        lblEmail.pack(pady=10)

        # Botão para nova votação
        frmBotoes = ttk.Frame(frmCedula)
        frmBotoes.pack(pady=30)

        self.btnNovaVotacao = ttk.Button(
            frmBotoes,
            text="Nova Votação",
            bootstyle="primary",
            width=20,
            command=self.voltar_para_entrada
        )
        self.btnNovaVotacao.pack(pady=5)

        # Botão para enviar comprovante por email (se disponível)
        if EMAIL_DISPONIVEL and email_votante:
            self.btnEnviarEmail = ttk.Button(
                frmBotoes,
                text="📧 Enviar Comprovante por Email",
                bootstyle="info",
                width=30,
                command=self.enviar_comprovante_email
            )
            self.btnEnviarEmail.pack(pady=5)
            
            # Label para status do envio
            self.lblStatusEmail = ttk.Label(
                frmBotoes,
                text="",
                font=("Courier", 11),
                anchor="center"
            )
            self.lblStatusEmail.pack(pady=5)

        # Instrução para voltar manualmente
        self.lblInstrucao = ttk.Label(
            frmCedula,
            text="Aperte ESPAÇO 3 vezes para voltar",
            font=("Courier", 12, "bold"),
            anchor="center",
            foreground="blue"
        )
        self.lblInstrucao.pack(pady=20)

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

    def enviar_comprovante_email(self):
        """Envia o comprovante de votação por email"""
        if self.email_enviado:
            self.lblStatusEmail.config(
                text="✅ Comprovante já foi enviado!",
                foreground="green"
            )
            return
            
        if not EMAIL_DISPONIVEL:
            self.lblStatusEmail.config(
                text="❌ yagmail não instalado",
                foreground="red"
            )
            return
            
        if not self.email_votante:
            self.lblStatusEmail.config(
                text="❌ Email do votante não disponível",
                foreground="red"
            )
            return
        
        # Desabilitar botão durante envio
        self.btnEnviarEmail.config(state="disabled")
        self.lblStatusEmail.config(
            text="📤 Enviando comprovante...",
            foreground="blue"
        )
        
        # Enviar em thread separada para não travar a interface
        thread = threading.Thread(target=self._enviar_email_thread)
        thread.daemon = True
        thread.start()
    
    def _enviar_email_thread(self):
        """Thread para envio do email"""
        try:
            # Configurar dados do email
            data_hora_atual = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
            
            assunto = f"Comprovante de Votação - {self.titulo}"
            
            conteudo = f"""Prezado(a) eleitor(a),

Seu voto foi registrado com sucesso!

=== DETALHES DA VOTAÇÃO ===
Eleição: {self.titulo}
Data/Hora: {data_hora_atual}
Cédula ID: {self.cedula_id or 'N/A'}
Votante: {self.mascarar_email(self.email_votante)}

=== IMPORTANTE ===
• Este é um comprovante de PARTICIPAÇÃO na votação
• O voto é secreto e foi registrado de forma anônima
• Este comprovante NÃO revela em qual candidato/chapa você votou
• Guarde este comprovante para seus registros

=== SISTEMA DE URNA ELETRÔNICA ===
Data de geração: {data_hora_atual}

Obrigado por participar do processo democrático!
"""
            
            # Configuração do email
            try:
                # Importar configurações do sistema
                import sys, os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
                from config_email import EMAIL_SISTEMA, SENHA_EMAIL
                
                # Usar configuração específica
                yag = yagmail.SMTP(EMAIL_SISTEMA, SENHA_EMAIL)
            except Exception as config_error:
                print(f"Erro na configuração do email: {config_error}")
                # Atualizar interface no thread principal
                self.janela.after(0, lambda: self._email_erro("Configuração de email não encontrada"))
                return
            
            # Enviar email
            yag.send(
                to=self.email_votante,
                subject=assunto,
                contents=conteudo
            )
            
            # Atualizar interface no thread principal
            self.janela.after(0, self._email_enviado_sucesso)
            
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            # Atualizar interface no thread principal
            self.janela.after(0, lambda: self._email_erro(str(e)))
    
    def _email_enviado_sucesso(self):
        """Callback quando email é enviado com sucesso"""
        self.email_enviado = True
        self.btnEnviarEmail.config(state="normal")
        self.lblStatusEmail.config(
            text="✅ Comprovante enviado com sucesso!",
            foreground="green"
        )
    
    def _email_erro(self, erro):
        """Callback quando há erro no envio"""
        self.btnEnviarEmail.config(state="normal")
        
        # Mensagens de erro mais amigáveis
        if "authentication" in erro.lower() or "password" in erro.lower():
            mensagem = "❌ Erro de autenticação"
        elif "connection" in erro.lower() or "network" in erro.lower():
            mensagem = "❌ Erro de conexão"
        elif "recipient" in erro.lower() or "address" in erro.lower():
            mensagem = "❌ Email inválido"
        else:
            mensagem = "❌ Erro ao enviar comprovante"
            
        self.lblStatusEmail.config(
            text=mensagem,
            foreground="red"
        )
        print(f"Erro detalhado: {erro}")

    def contar_espaco(self, event=None):
        """Conta as vezes que a tecla espaço foi pressionada"""
        self.espaco_contador += 1
        
        if self.espaco_contador == 1:
            self.lblInstrucao.config(
                text="Aperte ESPAÇO mais 2 vezes para voltar",
                foreground="orange"
            )
        elif self.espaco_contador == 2:
            self.lblInstrucao.config(
                text="Aperte ESPAÇO mais 1 vez para voltar",
                foreground="red"
            )
        elif self.espaco_contador >= 3:
            self.voltar_para_entrada()

    def voltar_para_entrada(self, event=None):
        """Volta para a tela de entrada de votação"""
        # Limpa todos os widgets da janela
        for widget in self.janela.winfo_children():
            widget.destroy()
        
        # Volta para a tela de entrada
        telaEntradaVotacao.iniciarTela(self.janela, self.eleicao_id, self.titulo)


def iniciarTela(master=None, eleicao_id=None, titulo="Eleição", cedula_id=None, email_votante=None):
    """Função para iniciar a tela de cédula virtual"""
    if master is None:
        app = tb.Window(themename="superhero")
        TelaCedulaVirtual(app, eleicao_id, titulo, cedula_id, email_votante)
        app.mainloop()
    else:
        TelaCedulaVirtual(master, eleicao_id, titulo, cedula_id, email_votante)