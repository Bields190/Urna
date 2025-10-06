from ttkbootstrap import ttk
import ttkbootstrap as tb
from tkinter import messagebox
import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_eleicao  # type: ignore

import telaADM, telaCriarEleicao, telaResultados, telaVotacao


class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Controle de Eleições")
        self.janela.geometry("1920x1080")

        # --- limpar widgets ---
        for widget in self.janela.winfo_children():
            widget.destroy()

        # bind ESC para voltar
        self.janela.bind("<Escape>", lambda e: self.voltar_tela_adm())

        # controlador
        self.control = c_eleicao.Control(self)
        
        # Obter dados do administrador logado
        self.admin_data = telaADM.TelaADM.get_admin_logado()

        # layout
        self.setup_interface()
        self.renderizar_eleicoes()

    def abrirVotacao(self, id_eleicao):
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaVotacao.iniciarTela(self.janela, id_eleicao)

    def abrirResultados(self, id_eleicao):
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaResultados.iniciarTela(self.janela, id_eleicao)

    def voltar_tela_adm(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaADM.TelaADM(self.janela)

    def setup_interface(self):
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=1)

        ttk.Label(
            self.janela, text="Controle de Eleições", font=("Courier", 20, "bold")
        ).grid(row=1, column=0, pady=(40, 10), padx=(20, 0))

        # Botão criar eleição
        self.btn_criar = ttk.Button(
            self.janela,
            text="+ Criar Nova Eleição",
            bootstyle="primary",
            width=20,
            command=self.criarEleicao,
        )
        self.btn_criar.grid(row=2, column=0, pady=(30, 60))

        # Frame container
        self.frmEleicoes = ttk.Frame(self.janela, padding=10)
        self.frmEleicoes.grid(
            row=3, column=0, columnspan=3, padx=10, pady=20, sticky="nsew"
        )

    def criarEleicao(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaCriarEleicao.iniciarTela(self.janela)

    def editarEleicao(self, id_eleicao, titulo, data_inicio, data_fim):
        for widget in self.janela.winfo_children():
            widget.destroy()
        dados_eleicao = {
            'id': id_eleicao, 
            'titulo': titulo, 
            'data_inicio': data_inicio, 
            'data_fim': data_fim
        }
        telaCriarEleicao.iniciarTela(self.janela, modo_edicao=True, dados_eleicao=dados_eleicao)

    def verDadosEleicao(self, id_eleicao, titulo, data_inicio, data_fim):
        """Abre uma janela popup para visualizar os dados da eleição"""
        self.mostrarDadosEleicao(id_eleicao, titulo, data_inicio, data_fim)

    def fecharEleicao(self, id_eleicao):
        """Fecha uma eleição ativa"""
        
        if messagebox.askyesno(
            "Confirmação", 
            "Tem certeza que deseja fechar esta eleição?\n\nEsta ação encerrará definitivamente a votação e não poderá ser desfeita."
        ):
            try:
                # Encerrar a eleição no controlador
                if self.control.encerrar_eleicao(id_eleicao):
                    messagebox.showinfo("Sucesso", "Eleição encerrada com sucesso!\n\nAgora você pode visualizar os resultados.")
                    # Atualizar a interface para mostrar os novos botões
                    self.renderizar_eleicoes()
                else:
                    messagebox.showerror("Erro", "Erro ao encerrar a eleição!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")

    def mostrarDadosEleicao(self, id_eleicao, titulo, data_inicio, data_fim):
        """Cria uma janela popup com os dados detalhados da eleição"""
        import tkinter as tk
        from tkinter import ttk as tk_ttk
        
        # Buscar dados completos da eleição para obter o status
        eleicao_data = self.control.buscar_eleicao(id_eleicao)
        status_db = None
        if eleicao_data and len(eleicao_data[0]) >= 5:
            status_db = eleicao_data[0][4]  # Status do banco de dados
        
        # Criar janela popup
        popup = tk.Toplevel(self.janela)
        popup.title(f"Dados da Eleição - {titulo}")
        popup.geometry("600x500")
        popup.resizable(True, True)
        popup.grab_set()  # Modal
        
        # Frame principal
        main_frame = tk_ttk.Frame(popup, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = tk_ttk.Label(
            main_frame, 
            text=f"Dados da Eleição: {titulo}", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Informações básicas
        info_frame = tk_ttk.LabelFrame(main_frame, text="Informações Básicas", padding=10)
        info_frame.pack(fill="x", pady=(0, 15))
        
        tk_ttk.Label(info_frame, text=f"ID: {id_eleicao}", font=("Arial", 12)).pack(anchor="w")
        tk_ttk.Label(info_frame, text=f"Título: {titulo}", font=("Arial", 12)).pack(anchor="w")
        tk_ttk.Label(
            info_frame, 
            text=f"Data de Início: {self.control.formatar_data_exibicao(data_inicio)}", 
            font=("Arial", 12)
        ).pack(anchor="w")
        tk_ttk.Label(
            info_frame, 
            text=f"Data de Fim: {self.control.formatar_data_exibicao(data_fim)}", 
            font=("Arial", 12)
        ).pack(anchor="w")
        
        status = self.control.obter_status_eleicao(data_inicio, data_fim, status_db)
        tk_ttk.Label(info_frame, text=f"Status: {status}", font=("Arial", 12, "bold")).pack(anchor="w")
        
        # Mostrar total de votos se a eleição estiver encerrada
        if status.lower() == "encerrada":
            try:
                import sys, os
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))
                import m_voto  # type: ignore
                total_votos = m_voto.Voto.contar_total_eleicao(id_eleicao)
                tk_ttk.Label(
                    info_frame, 
                    text=f"Total de Votos: {total_votos}", 
                    font=("Arial", 12, "bold")
                ).pack(anchor="w")
            except Exception as e:
                tk_ttk.Label(
                    info_frame, 
                    text="Total de Votos: Não disponível", 
                    font=("Arial", 12)
                ).pack(anchor="w")
        
        # Chapas associadas
        chapas_frame = tk_ttk.LabelFrame(main_frame, text="Chapas Participantes", padding=10)
        chapas_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        # Treeview para chapas
        chapas_tree = tk_ttk.Treeview(
            chapas_frame, 
            columns=("nome", "slogan", "numero"), 
            show="headings",
            height=8
        )
        chapas_tree.heading("nome", text="Nome da Chapa")
        chapas_tree.heading("slogan", text="Slogan")
        chapas_tree.heading("numero", text="Número")
        chapas_tree.column("nome", width=180)
        chapas_tree.column("slogan", width=250)
        chapas_tree.column("numero", width=80)
        
        # Scrollbar para o treeview
        scrollbar = tk_ttk.Scrollbar(chapas_frame, orient="vertical", command=chapas_tree.yview)
        chapas_tree.configure(yscrollcommand=scrollbar.set)
        
        chapas_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Carregar chapas
        chapas_associadas = self.control.listar_chapas_por_eleicao(id_eleicao)
        if chapas_associadas:
            for chapa in chapas_associadas:
                chapa_id, nome, slogan, logo, numero = chapa
                chapas_tree.insert("", "end", values=(
                    nome, 
                    slogan or "Sem slogan",
                    numero or "S/N"
                ))
        else:
            chapas_tree.insert("", "end", values=("Nenhuma chapa", "Não há chapas associadas", ""))
        
        # Botão fechar
        btn_frame = tk_ttk.Frame(main_frame)
        btn_frame.pack(fill="x")
        
        tk_ttk.Button(
            btn_frame, 
            text="Fechar", 
            command=popup.destroy
        ).pack(side="right")

    def excluirEleicao(self, id):
        if messagebox.askyesno("Confirmação", "Deseja excluir esta eleição?"):
            if self.control.deletar_eleicao(id):
                messagebox.showinfo("Sucesso", "Eleição excluída com sucesso!")
                self.renderizar_eleicoes()
            else:
                messagebox.showerror("Erro", "Erro ao excluir eleição!")

    def renderizar_eleicoes(self):
        for widget in self.frmEleicoes.winfo_children():
            widget.destroy()

        # configurar até 4 colunas
        for col in range(4):
            self.frmEleicoes.grid_columnconfigure(col, weight=1)

        eleicoes = self.control.listar_eleicoes()

        if not eleicoes:
            ttk.Label(
                self.frmEleicoes,
                text="Nenhuma eleição cadastrada",
                font=("Courier", 16),
                bootstyle="secondary",
            ).grid(row=0, column=0, columnspan=4, pady=50)
            return

        for i, eleicao in enumerate(eleicoes):
            # Verificar se a eleição tem 4 ou 5 campos (com ou sem status)
            if len(eleicao) == 5:
                id_eleicao, titulo, data_inicio, data_fim, status_db = eleicao
                status = self.control.obter_status_eleicao(data_inicio, data_fim, status_db)
            else:
                id_eleicao, titulo, data_inicio, data_fim = eleicao
                status = self.control.obter_status_eleicao(data_inicio, data_fim)
            
            
            # card
            frame_eleicao = ttk.Frame(
                self.frmEleicoes, padding=10, relief="ridge", borderwidth=2
            )
            frame_eleicao.grid(
                row=i // 4, column=i % 4, padx=10, pady=10, sticky="nsew"
            )

            ttk.Label(
                frame_eleicao, text=titulo, font=("Courier", 15, "bold")
            ).pack(anchor="n", pady=5)

            ttk.Label(
                frame_eleicao,
                text=f"Início: {self.control.formatar_data_exibicao(data_inicio)}",
                font=("Courier", 11),
                bootstyle="secondary",
            ).pack()

            ttk.Label(
                frame_eleicao,
                text=f"Fim: {self.control.formatar_data_exibicao(data_fim)}",
                font=("Courier", 11),
                bootstyle="secondary",
            ).pack()

            ttk.Label(
                frame_eleicao,
                text=f"Status: {status}",
                font=("Courier", 12, "bold"),
            ).pack(pady=5)

            # Mostrar quantas chapas estão associadas
            chapas_associadas = self.control.listar_chapas_por_eleicao(id_eleicao)
            num_chapas = len(chapas_associadas) if chapas_associadas else 0
            ttk.Label(
                frame_eleicao,
                text=f"Chapas: {num_chapas}",
                font=("Courier", 10),
                bootstyle="info",
            ).pack()

            frm_btn = ttk.Frame(frame_eleicao)
            frm_btn.pack(fill="x", pady=10)

            if status.lower() == "encerrada":
                ttk.Button(
                    frm_btn,
                    text="Resultados",
                    bootstyle="success",
                    command=lambda id=id_eleicao: self.abrirResultados(id),
                ).pack(side="left", expand=True, fill="x", padx=2)

            if status.lower() == "ativa":
                ttk.Button(
                    frm_btn,
                    text="Abrir Urna",
                    bootstyle="sucess",
                    command=lambda id=id_eleicao: self.abrirVotacao(id),
                ).pack(side="left", expand=True, fill="x", padx=2)
                
                # Botão fechar eleição (apenas para master)
                if (self.admin_data and self.admin_data.get('master') == 1):
                    ttk.Button(
                        frm_btn,
                        text="Fechar Eleição",
                        bootstyle="warning",
                        command=lambda id=id_eleicao: self.fecharEleicao(id),
                    ).pack(side="left", expand=True, fill="x", padx=2)

            # Botão de editar (apenas para master e eleições agendadas)
            if (self.admin_data and self.admin_data.get('master') == 1 and 
                status.lower() == "agendada"):
                ttk.Button(
                    frm_btn,
                    text="Editar",
                    bootstyle="info",
                    command=lambda id=id_eleicao, t=titulo, di=data_inicio, df=data_fim: 
                        self.editarEleicao(id, t, di, df),
                ).pack(side="left", expand=True, fill="x", padx=2)

            # Botão de ver dados (apenas para admins não-master)
            if (self.admin_data and self.admin_data.get('master') == 0):
                ttk.Button(
                    frm_btn,
                    text="Ver Dados",
                    bootstyle="secondary",
                    command=lambda id=id_eleicao, t=titulo, di=data_inicio, df=data_fim: 
                        self.verDadosEleicao(id, t, di, df),
                ).pack(side="left", expand=True, fill="x", padx=2)

            ttk.Button(
                frm_btn,
                text="Excluir",
                bootstyle="danger",
                command=lambda id=id_eleicao: self.excluirEleicao(id),
            ).pack(side="left", expand=True, fill="x", padx=2)

def iniciarTela(master=None):
    if master is None:
        app = tb.Window(themename="superhero")
        Tela(app)
        app.mainloop()
    else:
        Tela(master)