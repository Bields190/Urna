from ttkbootstrap import ttk
import ttkbootstrap as tb
from tkinter import messagebox, filedialog as fd, StringVar
from PIL import Image, ImageTk
import sys
import os

import telaChapas

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_chapas  # type: ignore


class Tela:
    def __init__(self, master, modo_edicao=False, dados_chapa=None):
        self.janela = master
        self.modo_edicao = modo_edicao
        self.dados_chapa = dados_chapa or {}
        self.caminho_imagem = self.dados_chapa.get('logo', '') or ''

       
        for w in self.janela.winfo_children():
            w.destroy()

        self.janela.title("Editar Chapa" if modo_edicao else "Adicionar Chapa")
        self.janela.geometry("1920x1080")

        # bind ESC para voltar 
        self.janela.bind('<Escape>', lambda e: self.voltar_tela_chapas())

        # container principal
        container = ttk.Frame(self.janela, padding=18)
        container.pack(fill="both", expand=True)


        titulo_text = "Editar Chapa" if modo_edicao else "Adicionar Chapa"
        ttk.Label(container, text=titulo_text, font=("Courier", 24, "bold"), bootstyle="primary").pack(pady=(6, 18))

        # corpo: foto | campos
        corpo = ttk.Frame(container)
        corpo.pack(fill="x", pady=(0, 8))

        # ---- foto (lado esquerdo) ----
        self.frm_foto = ttk.Frame(corpo, width=240, height=240, bootstyle="light")
        self.frm_foto.grid_propagate(False)
        self.frm_foto.grid(row=0, column=0, padx=20, sticky="n")

        self.lbl_adcFoto = ttk.Label(self.frm_foto, text="Adicionar Foto", font=("Courier", 12))
        self.lbl_adcFoto.place(relx=0.5, rely=0.5, anchor="center")
        self.lbl_adcFoto.bind("<Button-1>", lambda e: self.adcFoto())


        entradas = ttk.Frame(corpo)
        entradas.grid(row=0, column=1, sticky="nw")

        ttk.Label(entradas, text="Nome da Chapa:", font=("Courier", 14)).pack(anchor="w")
        self.entry_nome = ttk.Entry(entradas, width=60)
        self.entry_nome.pack(pady=(4, 10), anchor="w")

        ttk.Label(entradas, text="Número da Chapa:", font=("Courier", 14)).pack(anchor="w")
        # validação para aceitar apenas números no "Número da Chapa"
        vcmd = self.janela.register(self.validar_inteiro)
        self.entry_numero = ttk.Entry(entradas, width=60, validate="key", validatecommand=(vcmd, "%P"))
        self.entry_numero.pack(pady=(4, 10), anchor="w")

        ttk.Label(entradas, text="Slogan:", font=("Courier", 14)).pack(anchor="w")
        self.entry_slogan = ttk.Entry(entradas, width=60)
        self.entry_slogan.pack(pady=(4, 10), anchor="w")

        self.frm_cargos = ttk.Labelframe(container, text="Designações", padding=10)
        self.frm_cargos.pack(fill="both", padx=8, pady=(16, 6), expand=False)

        # Frame para os botões de designação
        btn_frame = ttk.Frame(self.frm_cargos)
        btn_frame.pack(anchor="w", pady=(0, 8))
        
        self.btn_designar_cargo = ttk.Button(btn_frame, text="Designar Cargo", bootstyle="primary-outline",
                                             command=self.abrir_designar_cargo)
        self.btn_designar_cargo.pack(side="left", padx=(0, 8))
        
        self.btn_excluir_candidato = ttk.Button(btn_frame, text="Excluir Candidato", bootstyle="danger-outline",
                                               command=self.excluir_candidato_selecionado)
        self.btn_excluir_candidato.pack(side="left")

        # Treeview para mostrar as designações já adicionadas
        self.designados = []  
        self.tree_designados = ttk.Treeview(self.frm_cargos, columns=("cargo", "nome"), show="headings", height=6)
        self.tree_designados.heading("cargo", text="Cargo")
        self.tree_designados.heading("nome", text="Candidato")
        self.tree_designados.column("cargo", width=220)
        self.tree_designados.column("nome", width=420)
        self.tree_designados.pack(fill="both", expand=True, padx=4, pady=6)

        # ---- botões Salvar / Voltar ----
        botoes = ttk.Frame(container)
        botoes.pack(fill="x", pady=(12, 4))

        texto_botao = "Atualizar Chapa" if modo_edicao else "Salvar Chapa"
        self.btn_salvar = ttk.Button(botoes, text=texto_botao, bootstyle="success", width=18,
                                     command=self.salvar_chapa)
        self.btn_salvar.pack(side="left", padx=(6, 8))

        self.btn_voltar = ttk.Button(botoes, text="Voltar", bootstyle="secondary", command=self.voltar_tela_chapas)
        self.btn_voltar.pack(side="left")

    
        if self.modo_edicao:
            self.preencher_campos()
            # Carregar candidatos após a interface estar completa
            self.carregar_candidatos_existentes()

    def preencher_campos(self):
        self.entry_nome.insert(0, self.dados_chapa.get('nome', ''))
        self.entry_numero.insert(0, self.dados_chapa.get('numero', ''))
        self.entry_slogan.insert(0, self.dados_chapa.get('slogan', ''))
        if self.caminho_imagem:
            self.carregar_imagem_preview()

    def carregar_candidatos_existentes(self):
        """Carrega candidatos existentes da chapa no modo edição"""
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'conexao'))
            from conexao import Conexao
            conn = Conexao().get_conexao()
            cursor = conn.cursor()
            
            # Buscar candidatos da chapa com informações do cargo
            cursor.execute("""
                SELECT c.nome, ca.id, ca.nome as cargo_nome
                FROM Candidato c
                JOIN Cargo ca ON c.cargo_id = ca.id
                WHERE c.chapa_id = ?
            """, (self.dados_chapa.get('id'),))
            
            candidatos = cursor.fetchall()
            conn.close()
            
            # Adicionar à lista e ao tree
            for nome_candidato, cargo_id, cargo_nome in candidatos:
                cargo_str = f"{cargo_id} - {cargo_nome}"
                self.designados.append((cargo_str, nome_candidato))
                self.tree_designados.insert("", "end", values=(cargo_str, nome_candidato))
                
        except Exception as e:
            print(f"Erro ao carregar candidatos existentes: {e}")

    def excluir_candidato_selecionado(self):
        """Exclui o candidato selecionado no treeview"""
        selecao = self.tree_designados.selection()
        
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um candidato para excluir!")
            return
        
        # Confirmar exclusão
        resposta = messagebox.askyesno("Confirmar Exclusão", 
                                     "Tem certeza que deseja excluir o candidato selecionado?")
        if not resposta:
            return
        
        try:
            # Pegar os dados do item selecionado
            item = selecao[0]
            valores = self.tree_designados.item(item, 'values')
            cargo_str = valores[0]
            nome_candidato = valores[1]
            
            # Remover da lista de designados
            self.designados = [(c, n) for c, n in self.designados 
                             if not (c == cargo_str and n == nome_candidato)]
            
            # Remover do treeview
            self.tree_designados.delete(item)
            
            messagebox.showinfo("Sucesso", "Candidato excluído com sucesso!")
            
        except Exception as e:
            print(f"Erro ao excluir candidato: {e}")
            messagebox.showerror("Erro", "Erro ao excluir candidato!")

    def validar_inteiro(self, valor):
        if valor == "":
            return True
        return valor.isdigit()

    def adcFoto(self):
        tipos = (('Imagens', '*.jpeg *.jpg *.png *.gif *.bmp'), ('Todos', '*.*'))
        caminho = fd.askopenfilename(filetypes=tipos, title="Selecionar imagem da chapa")
        if caminho:
            self.caminho_imagem = caminho
            self.carregar_imagem_preview()

    def carregar_imagem_preview(self):
        try:
            if self.caminho_imagem and os.path.exists(self.caminho_imagem):
                imagem = Image.open(self.caminho_imagem).resize((225, 225), Image.Resampling.LANCZOS)
                imagem_tk = ImageTk.PhotoImage(imagem)
                # limpar conteúdo do frame foto
                for ch in self.frm_foto.winfo_children():
                    ch.destroy()
                lbl_img = ttk.Label(self.frm_foto, image=imagem_tk)
                lbl_img.image = imagem_tk
                lbl_img.place(relx=0.5, rely=0.5, anchor="center")
        except Exception as e:
            print(f"[telaCriarChapas] Erro ao carregar imagem: {e}")

    def voltar_tela_chapas(self, event=None):
        for w in self.janela.winfo_children():
            w.destroy()
        telaChapas.Tela(self.janela)

    def salvar_chapa(self):
        nome = self.entry_nome.get().strip()
        numero = self.entry_numero.get().strip()
        slogan = self.entry_slogan.get().strip()
        logo = getattr(self, 'caminho_imagem', '')

        if not nome:
            messagebox.showerror("Erro", "Nome da chapa é obrigatório!")
            return

        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))
            import m_chapa  # type: ignore
            import m_candidato  # type: ignore

            if self.modo_edicao:
                id_chapa = self.dados_chapa.get('id')
                chapa = m_chapa.Chapa(nome, slogan, logo, numero, id=id_chapa)
                resultado = chapa.atualizar()
                
                # Em modo edição, primeiro remove todos os candidatos da chapa
                if resultado:
                    sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'conexao'))
                    from conexao import Conexao
                    conn = Conexao().get_conexao()
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM Candidato WHERE chapa_id = ?", (id_chapa,))
                    conn.commit()
                    conn.close()
            else:
                chapa = m_chapa.Chapa(nome, slogan, logo, numero)
                resultado = chapa.salvar()

            if resultado:
                # Salvar os candidatos designados
                chapa_id = chapa.id
                candidatos_salvos = 0
                
                for cargo_str, nome_candidato in self.designados:
                    try:
                        # Extrair o ID do cargo da string "ID - Nome"
                        cargo_id = int(cargo_str.split(' - ')[0])
                        
                        candidato = m_candidato.Candidato(nome_candidato, chapa_id, cargo_id)
                        if candidato.salvar():
                            candidatos_salvos += 1
                        else:
                            print(f"Aviso: Candidato {nome_candidato} para {cargo_str} já existe ou houve erro")
                    except (ValueError, IndexError) as e:
                        print(f"Erro ao processar cargo {cargo_str}: {e}")
                        continue
                
                if self.designados and candidatos_salvos == 0:
                    messagebox.showwarning("Aviso", "Chapa salva, mas nenhum candidato pôde ser adicionado (possível duplicidade).")
                else:
                    messagebox.showinfo("Sucesso", f"Chapa salva com sucesso! {candidatos_salvos} candidatos adicionados.")
                
                self.voltar_tela_chapas()
            else:
                messagebox.showerror("Erro", "Não foi possível salvar a chapa (possível duplicidade).")
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro inesperado", str(e))

    # ---------------- popup designar cargo ----------------
    def abrir_designar_cargo(self):
        popup = tb.Toplevel(self.janela)
        popup.transient(self.janela)
        popup.grab_set()
        popup.title("Designar Cargo")
        popup.geometry("520x420")
        popup.resizable(False, False)

        frame = ttk.Frame(popup, padding=12)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Designar Cargo", font=("Courier", 16, "bold")).pack(pady=(2, 12))

        # carregar cargos do BD, excluindo os já ocupados
        try:
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
            import c_cargos  # type: ignore
            cargos_bd = c_cargos.Control().listar_cargos()
            
            # Filtrar cargos já ocupados
            cargos_ocupados = set()
            for cargo_str, _ in self.designados:
                try:
                    cargo_id = int(cargo_str.split(' - ')[0])
                    cargos_ocupados.add(cargo_id)
                except (ValueError, IndexError):
                    continue
            
            # Criar lista apenas com cargos disponíveis
            cargos_disponiveis = [c for c in cargos_bd if c[0] not in cargos_ocupados] if cargos_bd else []
            lista = [f"{c[0]} - {c[1]}" for c in cargos_disponiveis] if cargos_disponiveis else ["Todos os cargos já estão ocupados"]
        except Exception as e:
            print(f"[telaCriarChapas] Erro ao carregar cargos: {e}")
            lista = ["Erro ao carregar cargos"]

        sel_var = StringVar()
        cbx = ttk.Combobox(frame, values=lista, textvariable=sel_var, state="readonly", width=56)
        if lista and lista[0] not in ["Todos os cargos já estão ocupados", "Nenhum cargo cadastrado", "Erro ao carregar cargos"]:
            cbx.current(0)
        cbx.pack(pady=(4, 8), anchor="w")

        ttk.Label(frame, text="Nome do Candidato:", font=("Courier", 12)).pack(anchor="w")
        entry_candidato = ttk.Entry(frame, width=56)
        entry_candidato.pack(pady=(4, 10), anchor="w")

        btn_add = ttk.Button(frame, text="Adicionar Candidato", bootstyle="success")
        btn_add.pack(pady=(4, 8))

        ttk.Label(frame, text="Candidatos Designados:", font=("Courier", 12, "bold")).pack(pady=(8, 4))

        # tree local do popup para feedback imediato
        tree_popup = ttk.Treeview(frame, columns=("cargo", "nome"), show="headings", height=6)
        tree_popup.heading("cargo", text="Cargo")
        tree_popup.heading("nome", text="Candidato")
        tree_popup.column("cargo", width=200)
        tree_popup.column("nome", width=300)
        tree_popup.pack(fill="both", pady=6, padx=4)

        def adicionar_local():
            cargo_sel = sel_var.get()
            nome_cand = entry_candidato.get().strip()
            if not cargo_sel or cargo_sel in ["Todos os cargos já estão ocupados", "Nenhum cargo cadastrado", "Erro ao carregar cargos"]:
                messagebox.showerror("Erro", "Selecione um cargo válido!")
                return
            if not nome_cand:
                messagebox.showerror("Erro", "Digite o nome do candidato!")
                return
                
            # Verificar se o cargo já está ocupado (dupla verificação)
            for cargo_existente, _ in self.designados:
                if cargo_existente == cargo_sel:
                    messagebox.showerror("Erro", "Este cargo já está ocupado na chapa!")
                    return
            
            # adiciona no tree do popup e na lista da tela principal
            tree_popup.insert("", "end", values=(cargo_sel, nome_cand))
            self._add_designacao(cargo_sel, nome_cand)
            entry_candidato.delete(0, "end")
            
            # Atualizar combobox removendo o cargo selecionado
            try:
                cargo_id = int(cargo_sel.split(' - ')[0])
                lista_atualizada = [item for item in lista if not item.startswith(f"{cargo_id} - ")]
                if not lista_atualizada:
                    lista_atualizada = ["Todos os cargos já estão ocupados"]
                cbx.configure(values=lista_atualizada)
                if lista_atualizada[0] != "Todos os cargos já estão ocupados":
                    cbx.current(0)
                else:
                    cbx.set("")
            except (ValueError, IndexError):
                pass
            
            # mensagem de confirmação sem fechar popup
            messagebox.showinfo("Sucesso", "Candidato adicionado à lista!")

        btn_add.configure(command=adicionar_local)

        ttk.Button(frame, text="Fechar", bootstyle="secondary", command=popup.destroy).pack(pady=(6, 6))

    def _add_designacao(self, cargo_str, candidato_str):
        self.designados.append((cargo_str, candidato_str))
        self.tree_designados.insert("", "end", values=(cargo_str, candidato_str))


def iniciarTela(master=None, modo_edicao=False, dados_chapa=None):
    if master is None:
        app = tb.Window(themename="litera")
        Tela(app, modo_edicao=modo_edicao, dados_chapa=dados_chapa)
        app.mainloop()
    else:
        Tela(master, modo_edicao=modo_edicao, dados_chapa=dados_chapa)