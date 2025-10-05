import tkinter as tk
from tkinter import messagebox
import sys
import os
import telaADM

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_administrador  # type: ignore

class Tela:
    def voltar_tela_adm(self, event=None):
        """Volta para a tela do administrador"""
        telaADM.TelaADM(self.janela)
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Administradores')
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")  

        for widget in self.janela.winfo_children():
            widget.destroy()   
    
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=3)
        self.janela.rowconfigure(3, weight=1)
        
        self.janela.bind('<Escape>', self.voltar_tela_adm)

        self.lbl_nomeTela = tk.Label(text="Controle de Administradores", font=("Arial", 20, "bold"), bg="white")
        self.lbl_nomeTela.grid(row=1, column=0, pady=(40, 10), padx=(20,0))

        self.btn_criar_adm = tk.Button(text="+ Adicionar Administrador", font=("Arial",16,"bold"), command=self.criarAdm)
        self.btn_criar_adm.grid(row=2, column=0, pady=(30,60))

        self.frmAdms = tk.Frame(self.janela, bd=2, padx=5, pady=5, bg="white")
        self.frmAdms.grid(row=3, column=0, columnspan=3, padx=10, pady=(20,20), sticky="nsew")
        
        self.renderizar_adms()  # Add this line

    def criarAdm(self):
        self.adcAdm = tk.Toplevel(self.janela)
        self.adcAdm.grab_set()
        self.adcAdm.title('Adicionar Administrador')
        self.adcAdm.configure(bg="white")
        self.janelaCentro(self.adcAdm, 450, 400)

        tk.Label(self.adcAdm, text="Adicionar Administrador", font=("Arial", 16, "bold"), bg="white").pack(pady=15)

        frm_campos = tk.Frame(self.adcAdm, bg="white")
        frm_campos.pack(padx=20)

        tk.Label(frm_campos, text="Nome:", font=("Arial", 10), bg="white").pack(anchor="w")
        self.ent_nome = tk.Entry(frm_campos, width=50, highlightthickness=1, highlightbackground="black")
        self.ent_nome.pack(pady=(0, 10), ipady=3)

        tk.Label(frm_campos, text="Matrícula:", font=("Arial", 10), bg="white").pack(anchor="w")
        self.ent_matricula = tk.Entry(frm_campos, width=50, highlightthickness=1, highlightbackground="black")
        self.ent_matricula.pack(pady=(0, 10), ipady=3)

        tk.Label(frm_campos, text="Email Institucional:", font=("Arial", 10), bg="white").pack(anchor="w")
        self.ent_email = tk.Entry(frm_campos, width=50, highlightthickness=1, highlightbackground="black")
        self.ent_email.pack(pady=(0, 10), ipady=3)

        tk.Label(frm_campos, text="Senha:", font=("Arial", 10), bg="white").pack(anchor="w")
        self.ent_senha = tk.Entry(frm_campos, width=50, show="*",highlightthickness=1, highlightbackground="black")
        self.ent_senha.pack(pady=(0, 10), ipady=3)
        self.ent_senha.bind('<Return>', lambda x: self.salvarAdm())

        self.btn_adc = tk.Button(self.adcAdm, text='Adicionar', bg='black', fg='white', width=15, font=("Arial",14), command=self.salvarAdm)
        self.btn_adc.pack(pady=20)

    def salvarAdm(self):
        nome = self.ent_nome.get()
        matricula = self.ent_matricula.get()
        email = self.ent_email.get()
        senha = self.ent_senha.get()

        if not all([nome, matricula, email, senha]):
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        if "@ufac.br" not in email:
            messagebox.showerror("Erro", "O email deve ser institucional (@ufac.br)!")
            return

        # Tenta salvar no banco de dados
        if c_administrador.Control(self).adicionar_administrador(nome, matricula, email, senha):
            messagebox.showinfo("Sucesso", "Administrador adicionado com sucesso!")
            self.adcAdm.destroy()
            self.renderizar_adms()  # Atualiza a lista
        else:
            messagebox.showerror("Erro", "Matrícula ou email já cadastrados!")

    def janelaCentro(self, window, largura, altura):
        x = (window.winfo_screenwidth()-largura)//2
        y = (window.winfo_screenheight()-altura)//2
        window.geometry(f"{largura}x{altura}+{x}+{y}")

    def renderizar_adms(self):
        for widget in self.frmAdms.winfo_children():
            widget.destroy()

        # Remove os pesos das colunas para evitar expansão
        self.frmAdms.grid_columnconfigure(0, weight=0)
        self.frmAdms.grid_columnconfigure(1, weight=0)
        self.frmAdms.grid_columnconfigure(2, weight=0)

        # Busca administradores do banco
        adms = c_administrador.Control(self).listar_administradores()

        if not adms:
            tk.Label(self.frmAdms, 
                    text="Nenhum administrador cadastrado", 
                    font=("Arial", 16), 
                    fg="gray", 
                    bg="white").grid(row=0, column=0, columnspan=3, pady=50)
            return

        for i, adm in enumerate(adms):
            id_adm, nome, matricula, email = adm

            frame_adm = tk.Frame(self.frmAdms, bd=2, relief="solid", width=400, height=200, bg="white")
            frame_adm.grid(row=i//3, column=i%3, padx=20, pady=20, sticky="")
            frame_adm.grid_propagate(False)
            frame_adm.pack_propagate(False)

            container = tk.Frame(frame_adm, bg="white")
            container.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.9, relheight=0.9)

            tk.Label(container, text=f"#{id_adm} - {nome}", font=("Arial", 15, "bold"), fg="black", bg="white",wraplength=350).pack(anchor="nw", pady=(5,0))
            
            tk.Label(container, text=f"Matrícula: {matricula}", font=("Arial", 11), fg="gray", bg="white",wraplength=350,justify="left").pack(anchor="nw", pady=2)

            tk.Label(container, text=f"Email: {email}", font=("Arial", 11), fg="gray", bg="white", wraplength=350, justify="left").pack(anchor="nw", pady=2)

            frm_botoes = tk.Frame(container, bg="white")
            frm_botoes.pack(side="bottom", fill="x", pady=5)

            tk.Button(frm_botoes, text="Editar", font=("Arial", 12, "bold"), bg="white",relief="solid", height=2, command=lambda id=id_adm, n=nome, m=matricula, e=email: self.editarAdm(id, n, m, e)).pack(side="left", fill="x", expand=True, padx=(0,5))
            
            tk.Button(frm_botoes, text="Excluir", font=("Arial", 12, "bold"), bg="red", fg="white", height=2,command=lambda id=id_adm: self.excluirAdm(id)).pack(side="left", fill="x", expand=True, padx=(5,0))

    def editarAdm(self, id, nome, matricula, email):
        self.editAdm = tk.Toplevel(self.janela)
        self.editAdm.grab_set()
        self.editAdm.title('Editar Administrador')
        self.editAdm.configure(bg="white")
        self.janelaCentro(self.editAdm, 450, 400)

        tk.Label(self.editAdm, text="Editar Administrador", font=("Arial", 16, "bold"), bg="white").pack(pady=15)

        frm_campos = tk.Frame(self.editAdm, bg="white")
        frm_campos.pack(padx=20)

        tk.Label(frm_campos, text="Nome:", font=("Arial", 10), bg="white").pack(anchor="w")

        self.ent_nome_edit = tk.Entry(frm_campos, width=50)
        self.ent_nome_edit.insert(0, nome)
        self.ent_nome_edit.pack(pady=(0, 10), ipady=3)

        tk.Label(frm_campos, text="Matrícula:", font=("Arial", 10), bg="white").pack(anchor="w")
        self.ent_matricula_edit = tk.Entry(frm_campos, width=50)
        self.ent_matricula_edit.insert(0, matricula)
        self.ent_matricula_edit.pack(pady=(0, 10), ipady=3)

        tk.Label(frm_campos, text="Email Institucional:", font=("Arial", 10), bg="white").pack(anchor="w")
        self.ent_email_edit = tk.Entry(frm_campos, width=50)
        self.ent_email_edit.insert(0, email)
        self.ent_email_edit.pack(pady=(0, 10), ipady=3)

        tk.Label(frm_campos, text="Nova Senha (opcional):", font=("Arial", 10), bg="white").pack(anchor="w")
        self.ent_senha_edit = tk.Entry(frm_campos, width=50, show="*")
        self.ent_senha_edit.pack(pady=(0, 10), ipady=3)

        tk.Button(self.editAdm, text='Salvar Alterações', bg='black', fg='white', width=18, font=("Arial",14), command=lambda: self.salvarEdicao(id)).pack(pady=20)

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

        #Tenta atualizar no banco de dados
        if c_administrador.Control(self).atualizar_administrador(id, nome, matricula, email, senha if senha else None):
            messagebox.showinfo("Sucesso", "Administrador atualizado com sucesso!")
            self.editAdm.destroy()
            self.renderizar_adms()  #Atualiza a lista
        else:
            messagebox.showerror("Erro", "Matrícula ou email já cadastrados!")

    def excluirAdm(self, id):
        confirm = messagebox.askyesno("Confirmação", 
            "Tem certeza que deseja excluir este administrador?")
        if confirm:
            if c_administrador.Control(self).deletar_administrador(id):
                messagebox.showinfo("Sucesso", "Administrador excluído com sucesso!")
                self.renderizar_adms()  # Atualiza a lista
            else:
                messagebox.showerror("Erro", "Erro ao excluir administrador!")


gui = tk.Tk()
Tela(gui)
gui.mainloop()