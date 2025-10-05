from ttkbootstrap import ttk
import ttkbootstrap as tb
from tkinter import messagebox
import sys
import os

import telaADM

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_cargos  # type: ignore


class Tela:
    def __init__(self, master):
        self.janela = master

        # Limpa widgets anteriores para carregar essa tela
        for widget in self.janela.winfo_children():
            widget.destroy()

        self.janela.title('Tela de Controle de Cargos')
        self.janela.geometry("1920x1080")

        self.janela.bind('<Escape>', self.voltar_tela_adm)
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=3)
        self.janela.rowconfigure(3, weight=1)

        self.lbl_nomeTela = ttk.Label(
            self.janela,
            text="Controle de Cargos",
            font=("Courier", 20, "bold")
        )
        self.lbl_nomeTela.grid(row=1, column=0, pady=(40, 10), padx=(20, 0))

        self.btn_criar_cargo = ttk.Button(
            self.janela,
            text="+ Criar Novo Cargo",
            bootstyle="primary",
            width=20,
            command=self.criarCargo
        )
        self.btn_criar_cargo.grid(row=2, column=0, pady=(30, 60))


        self.frmCargos = ttk.Frame(self.janela, padding=10)
        self.frmCargos.grid(row=3, column=0, columnspan=3, padx=10, pady=20, sticky="nsew")

        self.renderizar_cargos()

    def voltar_tela_adm(self, event=None):
        telaADM.TelaADM(self.janela)

    def criarCargo(self):
        self.adcCargo = tb.Toplevel(self.janela)
        self.adcCargo.grab_set()
        self.adcCargo.title('Adicionar Cargo')
        self.janelaCentro(self.adcCargo, 450, 250)

        ttk.Label(self.adcCargo, text="Adicionar Cargo",font=("Courier", 16, "bold")).pack(pady=15)

        frm_campos = ttk.Frame(self.adcCargo, padding=10)
        frm_campos.pack(padx=20, fill="x")

        ttk.Label(frm_campos, text="Cargo:", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_cargo = ttk.Entry(frm_campos, width=50)
        self.ent_cargo.pack(pady=(0, 10), ipady=3)

        ttk.Label(frm_campos, text="Descrição:", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_descricao = ttk.Entry(frm_campos, width=50)
        self.ent_descricao.pack(pady=(0, 10), ipady=3)
        self.ent_descricao.bind('<Return>', lambda x: self.salvarCargo())

        ttk.Button(self.adcCargo, text='Adicionar', bootstyle="success",width=15, command=self.salvarCargo).pack(pady=10)

    def salvarCargo(self):
        c_cargos.Control(self).adicionar_cargo()
        messagebox.showinfo("Sucesso", "Cargo adicionado com sucesso!")
        self.adcCargo.destroy()
        self.renderizar_cargos()

    # Editar cargo existente
    def editarCargo(self, id, nome, descricao):
        self.editCargo = tb.Toplevel(self.janela)
        self.editCargo.grab_set()
        self.editCargo.title('Editar Cargo')
        self.janelaCentro(self.editCargo, 450, 250)

        ttk.Label(self.editCargo, text="Editar Cargo", font=("Courier", 16, "bold")).pack(pady=15)

        frm_campos = ttk.Frame(self.editCargo, padding=10)
        frm_campos.pack(padx=20, fill="x")

        ttk.Label(frm_campos, text="Cargo:", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_cargo_edit = ttk.Entry(frm_campos, width=50)
        self.ent_cargo_edit.insert(0, nome)
        self.ent_cargo_edit.pack(pady=(0, 10), ipady=3)

        ttk.Label(frm_campos, text="Descrição:", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_descricao_edit = ttk.Entry(frm_campos, width=50)
        self.ent_descricao_edit.insert(0, descricao)
        self.ent_descricao_edit.pack(pady=(0, 10), ipady=3)
        self.ent_descricao_edit.bind('<Return>', lambda x: self.salvarEdicao(id))

        ttk.Button(self.editCargo,text='Salvar Alterações',bootstyle="info",width=18, command=lambda: self.salvarEdicao(id)).pack(pady=10)

    def salvarEdicao(self, id):
        nome = self.ent_cargo_edit.get()
        descricao = self.ent_descricao_edit.get()
        c_cargos.Control(self).atualizar_cargo(id, nome, descricao)
        messagebox.showinfo("Sucesso", "Cargo atualizado com sucesso!")
        self.editCargo.destroy()
        self.renderizar_cargos()

    # Excluir cargo
    def excluirCargo(self, id):
        confirm = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este cargo?")
        if confirm:
            c_cargos.Control(self).deletar_cargo(id)
            self.renderizar_cargos()

    # Renderizar cargos
    def renderizar_cargos(self):
        for widget in self.frmCargos.winfo_children():
            widget.destroy()

        for col in range(4):
            self.frmCargos.grid_columnconfigure(col, weight=1)

        cargos = c_cargos.Control(self).listar_cargos()

        if not cargos:
            ttk.Label(self.frmCargos, text="Nenhum cargo cadastrado", font=("Courier", 16), bootstyle="secondary").grid(row=0, column=0, columnspan=4, pady=50)
            return

        for i, cargo in enumerate(cargos):
            id_cargo, nome, descricao = cargo

            frame_cargo = ttk.Frame(self.frmCargos, padding=10, relief="ridge", borderwidth=2)
            frame_cargo.grid(row=i // 4, column=i % 4, padx=10, pady=10, sticky="nsew")

            ttk.Label(frame_cargo, text=f"{id_cargo} - {nome}", font=("Courier", 15, "bold"), wraplength=350).pack(anchor="n", pady=(5, 0))

            ttk.Label(frame_cargo,text=descricao,font=("Courier", 11),bootstyle="secondary", wraplength=350, justify="center"
            ).pack(anchor="n", pady=5)

            frm_botoes = ttk.Frame(frame_cargo)
            frm_botoes.pack(side="bottom", fill="x", pady=5)

            ttk.Button(frm_botoes, text="Editar", bootstyle="info-outline",command=lambda id=id_cargo, n=nome, d=descricao: self.editarCargo(id, n, d)).pack(side="left", expand=True, fill="x", padx=2)

            ttk.Button(frm_botoes, text="Excluir", bootstyle="danger",command=lambda id=id_cargo: self.excluirCargo(id)).pack(side="left", expand=True, fill="x", padx=2)

    def janelaCentro(self, window, largura, altura):
        x = (window.winfo_screenwidth() - largura) // 2
        y = (window.winfo_screenheight() - altura) // 2
        window.geometry(f"{largura}x{altura}+{x}+{y}")


def iniciarTela():
    app = tb.Window(themename="superhero")
    Tela(app)
    app.mainloop()
