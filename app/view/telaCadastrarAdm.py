from ttkbootstrap import ttk
import ttkbootstrap as tb
from tkinter import messagebox
import sys
import os
import telaADM

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_administrador  # type: ignore

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Administradores')
        self.janela.geometry("1920x1080")

        # Estilo geral
        self.janela.bind('<Escape>', self.voltar_tela_adm)
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=3)
        self.janela.rowconfigure(3, weight=1)

        # Título
        self.lbl_nomeTela = ttk.Label(self.janela, text="Controle de Administradores", font=("Courier", 20, "bold"))
        self.lbl_nomeTela.grid(row=1, column=0, pady=(40, 10), padx=(20,0))

        # Botão criar administrador
        self.btn_criar_adm = ttk.Button(self.janela, text="+ Adicionar Administrador", bootstyle="primary", width=25, command=self.criarAdm)
        self.btn_criar_adm.grid(row=2, column=0, pady=(30,60))

        # Frame container
        self.frmAdms = ttk.Frame(self.janela, padding=10)
        self.frmAdms.grid(row=3, column=0, columnspan=3, padx=10, pady=20, sticky="nsew")

        self.renderizar_adms()

    # Voltar à tela ADM
    def voltar_tela_adm(self, event=None):
        telaADM.TelaADM(self.janela)

    # Criar administrador
    def criarAdm(self):
        self.adcAdm = tb.Toplevel(self.janela)
        self.adcAdm.grab_set()
        self.adcAdm.title('Adicionar Administrador')
        self.janelaCentro(self.adcAdm, 600, 520)

        ttk.Label(self.adcAdm, text="Adicionar Administrador", font=("Courier", 16, "bold")).pack(pady=15)

        frm_campos = ttk.Frame(self.adcAdm, padding=10)
        frm_campos.pack(padx=20, fill="x")

        ttk.Label(frm_campos, text="Nome:", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_nome = ttk.Entry(frm_campos, width=50)
        self.ent_nome.pack(pady=(0, 10), ipady=3)

        ttk.Label(frm_campos, text="Matrícula:", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_matricula = ttk.Entry(frm_campos, width=50)
        self.ent_matricula.pack(pady=(0, 10), ipady=3)

        ttk.Label(frm_campos, text="Email Institucional:", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_email = ttk.Entry(frm_campos, width=50)
        self.ent_email.pack(pady=(0, 10), ipady=3)

        ttk.Label(frm_campos, text="Senha:", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_senha = ttk.Entry(frm_campos, width=50, show="*")
        self.ent_senha.pack(pady=(0, 10), ipady=3)
        self.ent_senha.bind('<Return>', lambda x: self.salvarAdm())

        ttk.Button(self.adcAdm, text='Adicionar', bootstyle="success", width=15, command=self.salvarAdm).pack(pady=20)

    def salvarAdm(self):
        nome = self.ent_nome.get()
        matricula = self.ent_matricula.get()
        email = self.ent_email.get()
        senha = self.ent_senha.get()

        if not all([nome, matricula, email, senha]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return
        if "@sou.ufac.br" not in email:
            messagebox.showerror("Erro", "O email deve ser institucional (@sou.ufac.br)!")
            return
        if c_administrador.Control(self).adicionar_administrador(nome, matricula, email, senha):
            messagebox.showinfo("Sucesso", "Administrador adicionado com sucesso!")
            self.adcAdm.destroy()
            self.renderizar_adms()
        else:
            messagebox.showerror("Erro", "Matrícula ou email já cadastrados!")

    # Centralizar janela
    def janelaCentro(self, window, largura, altura):
        x = (window.winfo_screenwidth() - largura) // 2
        y = (window.winfo_screenheight() - altura) // 2
        window.geometry(f"{largura}x{altura}+{x}+{y}")

    # Renderizar administradores
    def renderizar_adms(self):
        for widget in self.frmAdms.winfo_children():
            widget.destroy()

        for col in range(3):
            self.frmAdms.grid_columnconfigure(col, weight=1)

        adms = c_administrador.Control(self).listar_administradores()

        if not adms:
            ttk.Label(self.frmAdms, text="Nenhum administrador cadastrado", font=("Courier", 16), bootstyle="secondary").grid(row=0, column=0, columnspan=3, pady=50)
            return

        for i, adm in enumerate(adms):
            id_adm, nome, matricula, email = adm

            frame_adm = ttk.Frame(self.frmAdms, padding=10, relief="ridge")
            frame_adm.grid(row=i//3, column=i%3, padx=20, pady=20, sticky="nsew")

            ttk.Label(frame_adm, text=f"#{id_adm} - {nome}", font=("Courier", 15, "bold"), wraplength=350).pack(anchor="n", pady=(5,0))

            ttk.Label(frame_adm, text=f"Matrícula: {matricula}\nEmail: {email}", font=("Courier", 11), bootstyle="secondary", wraplength=350, justify="left").pack(anchor="n", pady=5)

            frm_botoes = ttk.Frame(frame_adm)
            frm_botoes.pack(side="bottom", fill="x", pady=5)

            ttk.Button(frm_botoes, text="Editar", bootstyle="info-outline",command=lambda id=id_adm, n=nome, m=matricula, e=email: self.editarAdm(id, n, m, e)).pack(side="left", expand=True, fill="x", padx=(0,5))

            ttk.Button(frm_botoes, text="Excluir", bootstyle="danger", command=lambda id=id_adm: self.excluirAdm(id)).pack(side="left", expand=True, fill="x", padx=(5,0))

    # Editar administrador
    def editarAdm(self, id, nome, matricula, email):
        self.editAdm = tb.Toplevel(self.janela)
        self.editAdm.grab_set()
        self.editAdm.title('Editar Administrador')
        self.janelaCentro(self.editAdm, 600, 520)

        ttk.Label(self.editAdm, text="Editar Administrador", font=("Courier", 16, "bold")).pack(pady=15)

        frm_campos = ttk.Frame(self.editAdm, padding=10)
        frm_campos.pack(padx=20, fill="x")

        ttk.Label(frm_campos, text="Nome:", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_nome_edit = ttk.Entry(frm_campos, width=50)
        self.ent_nome_edit.insert(0, nome)
        self.ent_nome_edit.pack(pady=(0, 10), ipady=3)

        ttk.Label(frm_campos, text="Matrícula:", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_matricula_edit = ttk.Entry(frm_campos, width=50)
        self.ent_matricula_edit.insert(0, matricula)
        self.ent_matricula_edit.pack(pady=(0, 10), ipady=3)

        ttk.Label(frm_campos, text="Email Institucional:", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_email_edit = ttk.Entry(frm_campos, width=50)
        self.ent_email_edit.insert(0, email)
        self.ent_email_edit.pack(pady=(0, 10), ipady=3)

        ttk.Label(frm_campos, text="Nova Senha (opcional):", font=("Courier", 10, "bold")).pack(anchor="w")
        self.ent_senha_edit = ttk.Entry(frm_campos, width=50, show="*")
        self.ent_senha_edit.pack(pady=(0, 10), ipady=3)

        ttk.Button(self.editAdm, text='Salvar Alterações', bootstyle="info", width=18, command=lambda: self.salvarEdicao(id)).pack(pady=20)

    def salvarEdicao(self, id):
        nome = self.ent_nome_edit.get()
        matricula = self.ent_matricula_edit.get()
        email = self.ent_email_edit.get()
        senha = self.ent_senha_edit.get()

        if not all([nome, matricula, email]):
            messagebox.showerror("Erro", "Nome, matrícula e email são obrigatórios!")
            return
        if "@sou.ufac.br" not in email:
            messagebox.showerror("Erro", "O email deve ser institucional (@sou.ufac.br)!")
            return
        if c_administrador.Control(self).atualizar_administrador(id, nome, matricula, email, senha if senha else None):
            messagebox.showinfo("Sucesso", "Administrador atualizado com sucesso!")
            self.editAdm.destroy()
            self.renderizar_adms()
        else:
            messagebox.showerror("Erro", "Matrícula ou email já cadastrados!")

    def excluirAdm(self, id):
        confirm = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este administrador?")
        if confirm:
            if c_administrador.Control(self).deletar_administrador(id):
                messagebox.showinfo("Sucesso", "Administrador excluído com sucesso!")
                self.renderizar_adms()
            else:
                messagebox.showerror("Erro", "Erro ao excluir administrador!")

def iniciarTela():
    app = tb.Window(themename="superhero")
    Tela(app)
    app.mainloop()
