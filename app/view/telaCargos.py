import tkinter as tk
from tkinter import messagebox
import sys
import os

import telaADM

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))

import c_cargos  # type: ignore


class Tela:
    def voltar_tela_adm(self, event=None):
        """Volta para a tela do administrador"""
        telaADM.TelaADM(self.janela)
    def __init__(self, master):
        self.janela = master

        # Limpa widgets anteriores para carregar essa tela
        for widget in self.janela.winfo_children():
            widget.destroy()

        self.janela.title('Tela de Controle de Cargos')
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")     

        self.janela.bind('<Escape>', self.voltar_tela_adm)

   
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=3)
        self.janela.rowconfigure(3, weight=1)

        self.lbl_nomeTela = tk.Label(self.janela, text="Controle de Cargos", font=("Arial", 20, "bold"), bg="white")
        self.lbl_nomeTela.grid(row=1, column=0, pady=(40, 10), padx=(20,0))

        self.btn_criar_cargo = tk.Button(self.janela, text="+ Criar Novo Cargo", font=("Arial",16,"bold"), command=self.criarCargo)
        self.btn_criar_cargo.grid(row=2, column=0, pady=(30,60))
   
        self.frmChapas = tk.Frame(self.janela, bd=2, padx=5, pady=5, bg="white")
        self.frmChapas.grid(row=3, column=0, columnspan=3, padx=10, pady=(20,20), sticky="nsew")

        self.renderizar_cargos()


    # Criar novo cargo
    def criarCargo(self):
        self.adcCargo = tk.Toplevel(self.janela)
        self.adcCargo.grab_set()
        self.adcCargo.title('Adicionar Cargo')
        self.adcCargo.configure(bg="white")
        self.janelaCentro(self.adcCargo, 450, 250)

        tk.Label(self.adcCargo, text="Adicionar Cargo", font=("Arial", 16, "bold"), bg="white").pack(pady=15)

        frm_campos = tk.Frame(self.adcCargo, bg="white")
        frm_campos.pack(padx=20)

        tk.Label(frm_campos, text="Cargo:", font=("Arial", 10), bg="white").pack(anchor="w")
        self.ent_cargo = tk.Entry(frm_campos, width=50, highlightthickness=1, highlightbackground="black")
        self.ent_cargo.pack(pady=(0, 10), ipady=3)

        tk.Label(frm_campos, text="Descrição:", font=("Arial", 10), bg="white").pack(anchor="w")
        self.ent_descricao = tk.Entry(frm_campos, width=50, highlightthickness=1, highlightbackground="black")
        self.ent_descricao.pack(pady=(0, 10), ipady=3)
        self.ent_descricao.bind('<Return>', lambda x: self.salvarCargo())

        self.btn_adc = tk.Button(self.adcCargo, text='Adicionar', bg='black', fg='white', width=15, font=("Arial",14),
                  command=self.salvarCargo)
        self.btn_adc.pack(pady=10)
        
    def salvarCargo(self):
        c_cargos.Control(self).adicionar_cargo()
        messagebox.showinfo("Sucesso", "Cargo adicionado com sucesso!")
        self.adcCargo.destroy()
        self.renderizar_cargos()


    def editarCargo(self, id, nome, descricao):
        self.editCargo = tk.Toplevel(self.janela)
        self.editCargo.grab_set()
        self.editCargo.title('Editar Cargo')
        self.editCargo.configure(bg="white")
        self.janelaCentro(self.editCargo, 450, 250)

        tk.Label(self.editCargo, text="Editar Cargo", font=("Arial", 16, "bold"), bg="white").pack(pady=15)

        frm_campos = tk.Frame(self.editCargo, bg="white")
        frm_campos.pack(padx=20)

        tk.Label(frm_campos, text="Cargo:", font=("Arial", 10), bg="white").pack(anchor="w")
        self.ent_cargo_edit = tk.Entry(frm_campos, width=50, highlightthickness=1, highlightbackground="black")
        self.ent_cargo_edit.insert(0, nome)
        self.ent_cargo_edit.pack(pady=(0, 10), ipady=3)

        tk.Label(frm_campos, text="Descrição:", font=("Arial", 10), bg="white").pack(anchor="w")
        self.ent_descricao_edit = tk.Entry(frm_campos, width=50, highlightthickness=1, highlightbackground="black")
        self.ent_descricao_edit.insert(0, descricao)
        self.ent_descricao_edit.pack(pady=(0, 10), ipady=3)
        self.ent_descricao_edit.bind('<Return>', lambda x: self.salvarEdicao(id))

        tk.Button(self.editCargo, text='Salvar Alterações', bg='black', fg='white', width=18, font=("Arial",14),
                  command=lambda: self.salvarEdicao(id)).pack(pady=10)

    def salvarEdicao(self, id):
        nome = self.ent_cargo_edit.get()
        descricao = self.ent_descricao_edit.get()
        c_cargos.Control(self).atualizar_cargo(id, nome, descricao)
        messagebox.showinfo("Sucesso", "Cargo atualizado com sucesso!")
        self.editCargo.destroy()
        self.renderizar_cargos()


    def excluirCargo(self, id):
        confirm = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este cargo?")
        if confirm:
            c_cargos.Control(self).deletar_cargo(id)
            self.renderizar_cargos()

    # Renderizar os cargos do banco
    def renderizar_cargos(self):
        for widget in self.frmChapas.winfo_children():
            widget.destroy()

        # Configura o grid para distribuir igualmente as 3 colunas
        self.frmChapas.grid_columnconfigure(0, weight=1)
        self.frmChapas.grid_columnconfigure(1, weight=1)
        self.frmChapas.grid_columnconfigure(2, weight=1)

        cargos = c_cargos.Control(self).listar_cargos()

        for i, cargo in enumerate(cargos):
            id_cargo, nome, descricao = cargo

            # Frame com tamanho fixo para cada cargo
            frame_cargo = tk.Frame(self.frmChapas, bd=2, relief="solid", width=400, height=200, bg="white")
            frame_cargo.grid(row=i//3, column=i%3, padx=20, pady=20, sticky="nsew")
            frame_cargo.grid_propagate(False)

            container = tk.Frame(frame_cargo, bg="white")
            container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

            tk.Label(container, text=f"{id_cargo} - {nome}", font=("Arial", 15, "bold"), fg="black", bg="white",wraplength=350).pack(anchor="nw", pady=(5,0))
            
            tk.Label(container, 
                text=descricao, 
                font=("Arial", 11), 
                fg="gray", 
                bg="white",
                wraplength=350,
                justify="left").pack(anchor="nw", pady=5)

            # Frame para os botões
            frm_botoes = tk.Frame(container, bg="white")
            frm_botoes.pack(side="bottom", fill="x", pady=5)

            tk.Button(frm_botoes, 
                text="Editar",
                font=("Arial", 12, "bold"),
                bg="white",
                relief="solid",
                height=2,
                command=lambda id=id_cargo, n=nome, d=descricao: self.editarCargo(id, n, d)
                ).pack(side="left", fill="x", expand=True, padx=(0,5))
            
            tk.Button(frm_botoes,
                text="Excluir",
                font=("Arial", 12, "bold"),
                bg="red",
                fg="white",
                height=2,
                command=lambda id=id_cargo: self.excluirCargo(id)
                ).pack(side="left", fill="x", expand=True, padx=(5,0))

    # Centraliza janelaPOPUP
    def janelaCentro(self, window, largura, altura):
        x = (window.winfo_screenwidth()-largura)//2
        y = (window.winfo_screenheight()-altura)//2
        window.geometry(f"{largura}x{altura}+{x}+{y}")
