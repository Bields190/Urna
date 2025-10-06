from ttkbootstrap import ttk
import ttkbootstrap as tb
from tkinter import messagebox
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))

import c_eleicao  # type: ignore
import m_chapa    # type: ignore

import telaEleicoes, telaChapas, telaCargos, telaLogin, telaCadastrarAdm

class TelaADM:
    # Variável de classe para armazenar dados do admin logado
    _admin_logado = None
    
    @classmethod
    def set_admin_logado(cls, admin_data):
        """Define os dados do administrador logado"""
        cls._admin_logado = admin_data
    
    @classmethod
    def get_admin_logado(cls):
        """Retorna os dados do administrador logado"""
        return cls._admin_logado
    def criarFramesDashboard(self, frmpai, titulo, valor, coluna):
        frameBoard = ttk.Frame(frmpai, padding=20, relief="ridge", borderwidth=3)
        frameBoard.grid(row=0, column=coluna, padx=40)
        ttk.Label(frameBoard, text=titulo, font=("Courier", 16, "bold")).pack(pady=10)
        ttk.Label(frameBoard, text=valor, font=("Courier", 24)).pack()
        return frameBoard

    def __init__(self, master, admin_data=None):
        self.janela = master
        
        # Se admin_data não foi passado, usa os dados armazenados
        if admin_data is None:
            admin_data = TelaADM.get_admin_logado()
        else:
            # Se admin_data foi passado, armazena para uso futuro
            TelaADM.set_admin_logado(admin_data)
            
        self.admin_data = admin_data  # Dados do administrador logado
        self.janela.title('Tela do Administrador')
        # Configura para tela cheia
        self.janela.attributes('-fullscreen', True)

        # limpa tudo que já estava na janela (ex: telaLogin)
        for widget in self.janela.winfo_children():
            widget.destroy()

        frmTopo = ttk.Frame(self.janela)
        frmTopo.pack(fill="x")

        frmTopo.columnconfigure(0, weight=1)
        frmTopo.columnconfigure(1, weight=1)
        frmTopo.columnconfigure(2, weight=1)

        self.btn_logout = ttk.Button(frmTopo,text="Logout",bootstyle="danger",width=15,command=self.logout)
        self.btn_logout.grid(row=0, column=0, sticky="w", padx=20, pady=(0, 70))

        ttk.Label(frmTopo,text="Dashboard",font=("Courier", 28, "bold")).grid(row=0, column=1, sticky="n", padx=(10, 200), pady=(60, 40))

        if self.admin_data and self.admin_data.get('usuario'):
            nome_usuario = self.admin_data.get('usuario')
            self.lbl_saudacao = ttk.Label(frmTopo, text=f"Olá, {nome_usuario}", font=("Courier", 16, "bold"), bootstyle="info")
            self.lbl_saudacao.grid(row=0, column=2, sticky="e", padx=20, pady=(20, 0))
        else:
            # Fallback caso não tenha dados do usuário
            self.lbl_saudacao = ttk.Label(frmTopo, text="Olá, Administrador", font=("Courier", 16, "bold"), bootstyle="info")
            self.lbl_saudacao.grid(row=0, column=2, sticky="e", padx=20, pady=(20, 0))

        # Configurar fonte padrão global
        self.janela.option_add("*Font", "Courier 14")

        # Configurar estilos do ttkbootstrap para usar Courier
        self.configurar_fontes()
        
        self.control = c_eleicao.Control()

        # ----------- Dashboard -----------
        self.frmDashboard = ttk.Frame(self.janela)
        self.frmDashboard.pack()

        
        self._dashboard_frames = []
        
        self.atualizar_dashboard()


        # --------- botões -------------
        botoes_frame = ttk.Frame(self.janela)
        botoes_frame.pack(expand=True, pady=40)

        self.btnEleicao = ttk.Button(botoes_frame,text="Gerenciar Eleições",width=40,bootstyle="primary",style="Fonte.TButton",command=lambda: self.trocarTela(telaEleicoes))
        self.btnEleicao.grid(row=0, column=0, pady=10)

        self.btnChapas = ttk.Button(botoes_frame,text="Gerenciar Chapas",width=40,bootstyle="primary",style="Fonte.TButton",command=lambda: self.trocarTela(telaChapas))
        self.btnChapas.grid(row=1, column=0, pady=10)

        self.btnCargos = ttk.Button(botoes_frame,text="Gerenciar Cargos",width=40,bootstyle="primary",style="Fonte.TButton",command=lambda: self.trocarTela(telaCargos))
        self.btnCargos.grid(row=2, column=0, pady=10)

        # Só mostra o botão de cadastrar administradores se o usuário for master
        if self.admin_data and self.admin_data.get('master') == 1:
            self.btnCadastrarADM = ttk.Button(botoes_frame,text="Cadastrar Administradores",width=40,bootstyle="primary",style="Fonte.TButton", command=lambda: self.trocarTela(telaCadastrarAdm))
            self.btnCadastrarADM.grid(row=3, column=0, pady=10)

    def configurar_fontes(self):
        """Configura todas as fontes para usar Courier"""
        style = tb.Style()
        style.configure("TLabel", font=("Courier", 14))
        style.configure("TButton", font=("Courier", 14))
        style.configure("TFrame", font=("Courier", 14))
        style.configure("Fonte.TButton", font=("Courier", 20, "bold"))

    def trocarTela(self, modulo):
        for widget in self.janela.winfo_children():
            widget.destroy()
        modulo.Tela(self.janela)

    def logout(self):
        resposta = messagebox.askyesno("Logout", "Tem certeza que deseja fazer logout?")
        if resposta:
            # Limpa os dados do administrador logado
            TelaADM.set_admin_logado(None)
            for widget in self.janela.winfo_children():
                widget.destroy()
            telaLogin.Tela(self.janela)
    def limpar_dashboard(self):
        # remove frames antigos do dashboard
        for f in self._dashboard_frames:
            try:
                f.destroy()
            except Exception:
                pass
        self._dashboard_frames = []
    def atualizar_dashboard(self):
        
        self.limpar_dashboard()

        total_eleicoes = 0
        eleicoes_ativas = 0
        total_chapas = 0
        votos_ultima = 0

        #-------dados eleições dahsboard-------
        try:
            if self.control:
                stats = self.control.obter_estatisticas_eleicoes()
                total_eleicoes = stats.get('total', 0)
                eleicoes_ativas = stats.get('ativas', 0)
        except Exception:
            
            pass

        #--------total de chapas----------
        try:
            chapas = m_chapa.Chapa.listar()  
            total_chapas = len(chapas)
        except Exception:
            try:
                todas_eleicoes = []
                if self.control:
                    todas_eleicoes = self.control.listar_eleicoes()
                count = 0
                for el in todas_eleicoes:
                    el_id = el[0]
                    try:
                        chapas_el = m_chapa.Chapa.listar_por_eleicao(el_id)
                        count += len(chapas_el)
                    except Exception:
                        pass
                if count > 0:
                    total_chapas = count
            except Exception:
                pass

        try:
            if self.control:
                eleicoes = self.control.listar_eleicoes()
                if eleicoes:
                    # cada eleicao parece ser (id, titulo, data_inicio, data_fim)
                    ultima = max(eleicoes, key=lambda e: e[3] if len(e) > 3 else "")
                    ultima_id = ultima[0]
                    resultado = self.control.resultado_eleicao(ultima_id)
                    votos_ultima = resultado.get('total_votos', 0)
        except Exception:
            pass

        #----------cria os frames---------- 
        f1 = self.criarFramesDashboard(self.frmDashboard, "ELEIÇÕES TOTAIS", str(total_eleicoes), 0)
        f2 = self.criarFramesDashboard(self.frmDashboard, "ELEIÇÕES ATIVAS", str(eleicoes_ativas), 1)
        f3 = self.criarFramesDashboard(self.frmDashboard, "TOTAL DE CHAPAS", str(total_chapas), 2)
        f4 = self.criarFramesDashboard(self.frmDashboard, "TOTAL DE VOTOS (última)", f"{votos_ultima}", 3)

        self._dashboard_frames.extend([f1, f2, f3, f4])

    def toggle_fullscreen(self, event=None):
        """Alterna entre tela cheia e janela normal"""
        current_state = self.janela.attributes('-fullscreen')
        self.janela.attributes('-fullscreen', not current_state)


def iniciarTela():
    app = tb.Window(themename="litera")
    TelaADM(app)
    app.mainloop()