import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import messagebox
import sys, os
import telaEleicoes

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_eleicao  # type: ignore


class Tela:
    def __init__(self, master, modo_edicao=False, dados_eleicao=None):
        self.janela = master
        self.modo_edicao = modo_edicao
        self.dados_eleicao = dados_eleicao or {}
        self.janela.title("Editar Eleição" if modo_edicao else "Criar Eleição")

        # limpar tela
        for widget in self.janela.winfo_children():
            widget.destroy()

        self.control = c_eleicao.Control(self)
        self.chapas_selecionadas = []

        # bind ESC para voltar
        self.janela.bind("<Escape>", lambda e: self.voltarEleicoes())

        titulo_tela = "Editar Eleição" if modo_edicao else "Criar Eleição"
        tb.Label(self.janela, text=titulo_tela, font=("Arial", 35, "bold")).pack(
            pady=15
        )

        frm = tb.Frame(self.janela, padding=20)
        frm.pack(pady=10)

        # ---- Campos da Eleição ----
        tb.Label(frm, text="Título:", font=("Arial", 20)).pack(pady=(20, 5))
        self.entry_titulo = tb.Entry(frm, width=40)
        self.entry_titulo.pack(pady=10)

        tb.Label(frm, text="Data de Início:", font=("Arial", 20)).pack()
        self.entry_inicio = tb.DateEntry(
            frm, dateformat="%d-%m-%Y", bootstyle=INFO, width=36
        )
        self.entry_inicio.pack(pady=10)

        tb.Label(frm, text="Data de Encerramento:", font=("Arial", 20)).pack()
        self.entry_fim = tb.DateEntry(
            frm, dateformat="%d-%m-%Y", bootstyle=INFO, width=36
        )
        self.entry_fim.pack(pady=10)

        # ---- Botões ----
        frm_botoes = tb.Frame(self.janela)
        frm_botoes.pack(pady=20)

        # Botão Salvar
        texto_botao = "Atualizar Eleição" if self.modo_edicao else "Salvar Eleição"
        tb.Button(
            frm_botoes,
            text=texto_botao,
            bootstyle="success-outline",
            width=20,
            command=self.salvarEleicao,
        ).pack(side="left", padx=10)

        # Botão Adicionar Chapa
        tb.Button(
            frm_botoes,
            text="Adicionar Chapa",
            bootstyle="info-outline",
            width=20,
            command=self.adicionarChapa,
        ).pack(side="left", padx=10)

        # ---- Treeview para mostrar chapas selecionadas ----
        tb.Label(self.janela, text="Chapas Selecionadas:", font=("Arial", 16, "bold")).pack(pady=(10, 5))
        self.tree_chapas = tb.Treeview(self.janela, columns=("chapa",), show="headings", height=8)
        self.tree_chapas.heading("chapa", text="Chapa")
        self.tree_chapas.column("chapa", width=500)
        self.tree_chapas.pack(fill="both", padx=20, pady=10)

        # Preencher campos se estiver em modo de edição
        if self.modo_edicao and self.dados_eleicao:
            self.carregar_dados_eleicao()

    def voltarEleicoes(self):
        telaEleicoes.iniciarTela(self.janela)

    def carregar_dados_eleicao(self):
        """Carrega os dados da eleição nos campos para edição"""
        from datetime import datetime
        
        # Preencher título
        self.entry_titulo.insert(0, self.dados_eleicao.get('titulo', ''))
        
        # Converter e preencher datas (de YYYY-MM-DD para DD-MM-YYYY)
        data_inicio = self.dados_eleicao.get('data_inicio', '')
        data_fim = self.dados_eleicao.get('data_fim', '')
        
        if data_inicio:
            try:
                data_obj = datetime.strptime(data_inicio, '%Y-%m-%d')
                self.entry_inicio.entry.delete(0, 'end')
                self.entry_inicio.entry.insert(0, data_obj.strftime('%d-%m-%Y'))
            except ValueError:
                pass
                
        if data_fim:
            try:
                data_obj = datetime.strptime(data_fim, '%Y-%m-%d')
                self.entry_fim.entry.delete(0, 'end')
                self.entry_fim.entry.insert(0, data_obj.strftime('%d-%m-%Y'))
            except ValueError:
                pass

        # Carregar chapas associadas à eleição
        if self.dados_eleicao.get('id'):
            chapas_eleicao = self.control.listar_chapas_por_eleicao(self.dados_eleicao['id'])
            for chapa in chapas_eleicao:
                chapa_id, nome, slogan, logo, numero = chapa
                self.chapas_selecionadas.append(nome)
                self.tree_chapas.insert("", "end", values=(nome,))

    def salvarEleicao(self):
        titulo = self.entry_titulo.get().strip()
        data_inicio = self.entry_inicio.entry.get()
        data_fim = self.entry_fim.entry.get()

        if not titulo:
            messagebox.showerror("Erro", "O título da eleição é obrigatório!")
            return
        if not self.chapas_selecionadas:
            messagebox.showerror("Erro", "Adicione pelo menos uma chapa!")
            return
        self.control.tela.entry1 = self.entry_titulo
        self.control.tela.entry2 = self.entry_inicio
        self.control.tela.entry3 = self.entry_fim
        self.control.tela.chapas = self.chapas_selecionadas  # passar chapas selecionadas

        try:
            if self.modo_edicao:
                # Atualizar eleição existente
                id_eleicao = self.dados_eleicao.get('id')
                sucesso = self.control.atualizar_eleicao(id_eleicao, titulo, data_inicio, data_fim)
                mensagem_sucesso = "Eleição atualizada com sucesso!"
            else:
                # Criar nova eleição
                sucesso = self.control.adicionar_eleicao()
                mensagem_sucesso = "Eleição criada com sucesso!"
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar eleição: {e}")
            return

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem_sucesso)
            self.voltarEleicoes()
        else:
            messagebox.showerror("Erro", "Erro ao salvar eleição!")

    def adicionarChapa(self):
        popup = tb.Toplevel(self.janela)
        popup.transient(self.janela)
        popup.grab_set()
        popup.title("Adicionar Chapas à Eleição")
        popup.geometry("600x520")
        popup.resizable(False, False)

        frame = tb.Frame(popup, padding=12)
        frame.pack(fill="both", expand=True)

        tb.Label(frame, text="Selecione a Chapa", font=("Arial", 16, "bold")).pack(pady=(10, 12))

        # carregar chapas do BD - apenas chapas com candidatos
        try:
            import c_chapas  # type: ignore
            chapas_bd = c_chapas.Control().listar_chapas()
            
            # Filtrar chapas que têm candidatos
            chapas_com_candidatos = []
            if chapas_bd:
                sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'conexao'))
                from conexao import Conexao
                conn = Conexao().get_conexao()
                cursor = conn.cursor()
                
                for chapa in chapas_bd:
                    chapa_id = chapa[0]
                    cursor.execute("SELECT COUNT(*) FROM Candidato WHERE chapa_id = ?", (chapa_id,))
                    count = cursor.fetchone()[0]
                    if count > 0:
                        chapas_com_candidatos.append(chapa)
                
                conn.close()
            
            lista_chapas = [f"{c[0]} - {c[1]}" for c in chapas_com_candidatos] if chapas_com_candidatos else ["Nenhuma chapa com candidatos"]
        except Exception as e:
            print(f"[telaCriarEleicao] Erro ao carregar chapas: {e}")
            lista_chapas = ["Erro ao carregar chapas"]

        sel_var = tb.StringVar()
        cbx = tb.Combobox(frame, values=lista_chapas, textvariable=sel_var, state="readonly", width=50)
        if lista_chapas and lista_chapas[0] not in ["Nenhuma chapa com candidatos", "Erro ao carregar chapas"]:
            cbx.current(0)
        cbx.pack(pady=(5, 10))

        tb.Label(frame, text="Chapas Selecionadas:", font=("Arial", 12, "bold")).pack(pady=(10, 4))

        tree_popup = tb.Treeview(frame, columns=("chapa",), show="headings", height=8)
        tree_popup.heading("chapa", text="Chapa")
        tree_popup.column("chapa", width=500)
        tree_popup.pack(fill="both", padx=6, pady=6)

        def adicionar_local():
            chapa = sel_var.get()
            if chapa in ["Nenhuma chapa com candidatos", "Erro ao carregar chapas"]:
                messagebox.showerror("Erro", "Selecione uma chapa válida!")
                return
            if chapa in self.chapas_selecionadas:
                messagebox.showwarning("Aviso", "Chapa já adicionada!")
                return
                
            # Verificar compatibilidade de cargos se já há chapas selecionadas
            if self.chapas_selecionadas:
                try:
                    chapa_id = int(chapa.split(' - ')[0])
                    primeira_chapa_id = int(self.chapas_selecionadas[0].split(' - ')[0])
                    
                    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'conexao'))
                    from conexao import Conexao
                    conn = Conexao().get_conexao()
                    cursor = conn.cursor()
                    
                    # Buscar cargos da primeira chapa
                    cursor.execute("""
                        SELECT DISTINCT cargo_id FROM Candidato WHERE chapa_id = ?
                        ORDER BY cargo_id
                    """, (primeira_chapa_id,))
                    cargos_primeira = set(row[0] for row in cursor.fetchall())
                    
                    # Buscar cargos da chapa atual
                    cursor.execute("""
                        SELECT DISTINCT cargo_id FROM Candidato WHERE chapa_id = ?
                        ORDER BY cargo_id
                    """, (chapa_id,))
                    cargos_atual = set(row[0] for row in cursor.fetchall())
                    
                    conn.close()
                    
                    # Verificar se têm os mesmos cargos
                    if cargos_primeira != cargos_atual:
                        messagebox.showerror("Erro", 
                                           "Esta chapa não possui candidatos para os mesmos cargos que as outras chapas já selecionadas!\n\n"
                                           "Para uma eleição válida, todas as chapas devem ter candidatos para os mesmos cargos.")
                        return
                        
                except (ValueError, IndexError, Exception) as e:
                    print(f"Erro ao verificar compatibilidade: {e}")
                    messagebox.showerror("Erro", "Erro ao verificar compatibilidade da chapa!")
                    return
            
            # adicionar à lista principal e aos Treeviews
            self.chapas_selecionadas.append(chapa)
            tree_popup.insert("", "end", values=(chapa,))
            self.tree_chapas.insert("", "end", values=(chapa,))
            messagebox.showinfo("Sucesso", "Chapa adicionada!")

        # botão dentro do popup para adicionar chapa
        tb.Button(frame, text="Adicionar Chapa", bootstyle="success", command=adicionar_local).pack(pady=5)
        tb.Button(frame, text="Fechar", bootstyle="secondary", command=popup.destroy).pack(pady=6)


def iniciarTela(master=None, modo_edicao=False, dados_eleicao=None):
    if master is None:
        app = tb.Window(themename="superhero")
        Tela(app, modo_edicao=modo_edicao, dados_eleicao=dados_eleicao)
        app.mainloop()
    else:
        Tela(master, modo_edicao=modo_edicao, dados_eleicao=dados_eleicao)
