import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox
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
        
        titulo = "Editar Chapa" if modo_edicao else "Adicionar Chapa"
        self.janela.title(f'Tela de {titulo}')
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")
        self.janela.bind('<Escape>', lambda event: self.voltar_tela_chapas())

        self.lbl_titulo = tk.Label(self.janela, text=titulo, font=("Arial", 24, "bold"), bg="white")
        self.lbl_titulo.pack(pady=45)

        self.frm_geral = tk.Frame(self.janela, bg="white")
        self.frm_geral.pack(pady=(10, 30))

        self.frm_entradas = tk.Frame(self.frm_geral, bg="white")
        self.frm_entradas.grid(row=0, column=1, padx=20)

        # Frame para a foto da chapa
        self.frm_foto = tk.Frame(self.frm_geral, bg="white", width=225, height=225, highlightthickness=1, highlightbackground="black")
        self.frm_foto.grid(row=0, column=0, padx=20)
        self.frm_foto.grid_propagate(False)

        self.lbl_adcFoto = tk.Label(self.frm_foto, text="Adicionar Foto", font=("Arial", 16), bg="white")
        self.lbl_adcFoto.place(relx=0.5, rely=0.5, anchor="center")
        self.lbl_adcFoto.bind('<Button-1>', lambda event: self.adcFoto())

        # Entrys e Labels de nome e slogan da chapa
        self.lbl_nome = tk.Label(self.frm_entradas, text="Nome da Chapa:", font=("Arial", 16), bg="white")
        self.lbl_nome.pack(anchor="w")
        self.entry_nome = tk.Entry(self.frm_entradas, width=50, highlightthickness=1, highlightbackground="black")
        self.entry_nome.pack(pady=(0, 10), ipady=3)

        self.lbl_slogan = tk.Label(self.frm_entradas, text="Slogan:", font=("Arial", 16), bg="white")
        self.lbl_slogan.pack(anchor="w")
        self.entry_slogan = tk.Entry(self.frm_entradas, width=50, highlightthickness=1, highlightbackground="black")
        self.entry_slogan.pack(pady=(0, 20), ipady=20)

        # Frame para cargos (mantido para funcionalidade futura)
        self.frm_cargos = tk.Frame(self.janela, bg="white", width=1500, height=350, highlightthickness=1, highlightbackground="black")
        self.frm_cargos.pack(pady=(25, 20))
        self.frm_cargos.pack_propagate(False)

        self.btn_designar_cargo = tk.Button(self.frm_cargos, text='Designar Cargo', bg='black', fg='white', width=15, font=("Arial", 14), command=self.abrir)
        self.btn_designar_cargo.pack(pady=10, anchor="w", padx=10)

        # Botão de salvar bem embaixo
        texto_botao = "Atualizar Chapa" if modo_edicao else "Salvar Chapa"
        self.btn_salvar = tk.Button(self.janela, text=texto_botao, bg='black', fg='white', width=20, font=("Arial", 16), command=self.salvar_chapa)
        self.btn_salvar.pack(pady=30)

        # Se estiver em modo de edição, preencher os campos
        if self.modo_edicao:
            self.preencher_campos()

    def preencher_campos(self):
        """Preenche os campos com os dados da chapa em edição"""
        self.entry_nome.insert(0, self.dados_chapa.get('nome', ''))
        self.entry_slogan.insert(0, self.dados_chapa.get('slogan', ''))
        
        # Carregar imagem se existir
        if self.caminho_imagem:
            self.carregar_imagem_preview()

    def carregar_imagem_preview(self):
        """Carrega e exibe a imagem atual no preview"""
        try:
            if self.caminho_imagem and os.path.exists(self.caminho_imagem):
                imagem = Image.open(self.caminho_imagem)
                imagem = imagem.resize((225, 225))
                imagem_tk = ImageTk.PhotoImage(imagem)

                self.lbl_imagem = tk.Label(self.frm_foto, bg="white")
                self.lbl_imagem.place(relx=0.5, rely=0.5, anchor="center")
                self.lbl_imagem.config(image=imagem_tk)
                self.lbl_imagem.image = imagem_tk
                self.lbl_adcFoto.place_forget()
        except Exception as e:
            print(f"Erro ao carregar imagem: {e}")

    def voltar_tela_chapas(self):
        """Volta para a tela de chapas"""
        self.janela.destroy()
        telaChapas.iniciarTela()

    def somente_numeros(self, texto):
        return texto.isdigit() or texto == ""

    # Comando para adicionar foto da chapa
    def adcFoto(self):
        tipos = (('Imagens', '*.jpeg *.jpg *.png *.gif *.bmp'), ('Todos', '*.*'))
        caminho_imagem = fd.askopenfilename(filetypes=tipos, title="Selecionar imagem da chapa")
        if caminho_imagem:
            self.caminho_imagem = caminho_imagem
            print(f"Imagem selecionada: {caminho_imagem}")  # Debug
            self.carregar_imagem_preview()

    def salvar_chapa(self):
        """Salva ou atualiza a chapa no banco de dados"""
        nome = self.entry_nome.get().strip()
        slogan = self.entry_slogan.get().strip()
        logo = self.caminho_imagem if hasattr(self, 'caminho_imagem') else ""

        if not nome:
            messagebox.showerror("Erro", "Nome da chapa é obrigatório!")
            return

        try:
            # Importar o modelo diretamente
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))
            import m_chapa  # type: ignore
            
            if self.modo_edicao:
                # Atualizar chapa existente
                id_chapa = self.dados_chapa['id']
                chapa = m_chapa.Chapa(nome, slogan, logo, id=id_chapa)
                resultado = chapa.atualizar()
                if resultado:
                    messagebox.showinfo("Sucesso", "Chapa atualizada com sucesso!")
                    self.voltar_tela_chapas()
                else:
                    messagebox.showerror("Erro", "Erro ao atualizar chapa.")
            else:
                # Criar nova chapa
                chapa = m_chapa.Chapa(nome, slogan, logo)
                resultado = chapa.salvar()
                if resultado:
                    messagebox.showinfo("Sucesso", "Chapa criada com sucesso!")
                    self.voltar_tela_chapas()
                else:
                    messagebox.showerror("Erro", "Erro ao criar chapa. Pode ser que uma chapa com esses dados já exista.")
        except Exception as e:
            print(f"Erro detalhado: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")

    # PopUp de adicionar cargo com integração ao BD
    def abrir(self):
        self.adcCargo = tk.Toplevel(self.janela)
        self.adcCargo.grab_set()
        self.adcCargo.title('Designar Cargo')
        self.adcCargo.configure(bg="white")
        self.janelaCentro(self.adcCargo, 450, 300)

        self.lbl_tituloCargo = tk.Label(self.adcCargo, text="Designar Cargo", font=("Arial", 16, "bold"), bg="white")
        self.lbl_tituloCargo.pack(pady=15)

        self.frm_campos = tk.Frame(self.adcCargo, bg="white")
        self.frm_campos.pack(padx=20)

        # Carregar cargos do banco de dados
        self.lbl_cargo = tk.Label(self.frm_campos, text="Cargo:", font=("Arial", 10), bg="white")
        self.lbl_cargo.pack(anchor="w")
        
        try:
            # Importar c_cargos para buscar os cargos do BD
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
            import c_cargos  # type: ignore
            cargos_bd = c_cargos.Control().listar_cargos()
            cargos_lista = [f"{cargo[0]} - {cargo[1]}" for cargo in cargos_bd]  # id - nome
            
            if not cargos_lista:
                cargos_lista = ['Nenhum cargo cadastrado']
        except Exception as e:
            print(f"Erro ao carregar cargos: {e}")
            cargos_lista = ['Erro ao carregar cargos']
        
        self.cargos = tk.StringVar()
        self.cbx_cargos = ttk.Combobox(self.frm_campos, values=cargos_lista, textvariable=self.cargos, state='readonly', width=47)
        if cargos_lista and cargos_lista[0] != 'Nenhum cargo cadastrado':
            self.cbx_cargos.current(0)
        self.cbx_cargos.pack(pady=(0, 10))

        self.lbl_candidato = tk.Label(self.frm_campos, text="Nome do Candidato:", font=("Arial", 10), bg="white")
        self.lbl_candidato.pack(anchor="w")
        self.entry_candidato = tk.Entry(self.frm_campos, width=50, highlightthickness=1, highlightbackground="black")
        self.entry_candidato.pack(pady=(0, 10), ipady=3)

        self.btn_adicionar_cargo = tk.Button(self.adcCargo, text='Adicionar Candidato', bg='green', fg='white', width=18, font=("Arial", 12), command=self.adicionar_candidato)
        self.btn_adicionar_cargo.pack(pady=10)
        
        # Lista de candidatos adicionados
        self.lbl_lista = tk.Label(self.adcCargo, text="Candidatos Designados:", font=("Arial", 12, "bold"), bg="white")
        self.lbl_lista.pack(pady=(20, 5))
        
        self.frame_lista = tk.Frame(self.adcCargo, bg="white", height=100)
        self.frame_lista.pack(fill="x", padx=20, pady=5)
        
        # Scrollbar para a lista
        self.lista_candidatos = tk.Listbox(self.frame_lista, height=4)
        scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical")
        self.lista_candidatos.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lista_candidatos.yview)
        
        self.lista_candidatos.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def adicionar_candidato(self):
        """Adiciona um candidato à lista"""
        cargo_selecionado = self.cargos.get()
        nome_candidato = self.entry_candidato.get().strip()
        
        if not cargo_selecionado or cargo_selecionado in ['Nenhum cargo cadastrado', 'Erro ao carregar cargos']:
            messagebox.showerror("Erro", "Selecione um cargo válido!")
            return
            
        if not nome_candidato:
            messagebox.showerror("Erro", "Digite o nome do candidato!")
            return
        
        # Adicionar à lista
        item = f"{cargo_selecionado} -> {nome_candidato}"
        self.lista_candidatos.insert(tk.END, item)
        
        # Limpar campo do candidato
        self.entry_candidato.delete(0, tk.END)
        
        messagebox.showinfo("Sucesso", "Candidato adicionado à lista!")

    def janelaCentro(self, window, largura, altura):
        x = (window.winfo_screenwidth()-largura)//2
        y = (window.winfo_screenheight()-altura)//2
        window.geometry(f"{largura}x{altura}+{x}+{y}")


def iniciarTela(modo_edicao=False, dados_chapa=None):
    app = tk.Tk()
    Tela(app, modo_edicao, dados_chapa)
    app.mainloop()