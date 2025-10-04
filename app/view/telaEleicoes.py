import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_eleicao #type: ignore

import telaADM, telaCriarEleicao


class Tela:
    def voltar_tela_adm(self):
        """Volta para a tela do administrador"""
        telaADM.TelaADM(self.janela)

    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Eleições')
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")
        self.janela.bind('<Escape>', lambda event: self.voltar_tela_adm())

        # --- limpar widgets antigos (IMPORTANTE) ---
        for widget in self.janela.winfo_children():
            widget.destroy()

        # Inicializar controlador
        self.control = c_eleicao.Control(self)

        self.setup_interface()
        self.carregar_eleicoes()

    def setup_interface(self):
        """Configura a interface básica"""
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=3)
        self.janela.rowconfigure(3, weight=1)

        self.lbl_ola = tk.Label(self.janela, text="Controle de Eleições",
                                font=("Arial", 20, "bold"), bg="white")
        self.lbl_ola.grid(row=1, column=0, pady=(40, 10), padx=(20, 0))

        # Frame para botões de ação
        self.frm_botoes = tk.Frame(self.janela, bg="white")
        self.frm_botoes.grid(row=2, column=0, pady=(30, 60), sticky="w", padx=(20, 0))

        self.btn_criar_eleicao = tk.Button(
            self.frm_botoes, text="+ Criar Nova Eleição",
            font=("Arial", 16, "bold"), bg="black", fg="white",
            command=lambda: telaCriarEleicao.iniciarTela(self.janela)
        )
        self.btn_criar_eleicao.pack(side="left", padx=(0, 10))

        self.btn_atualizar = tk.Button(
            self.frm_botoes, text="🔄 Atualizar",
            font=("Arial", 16, "bold"), bg="gray", fg="white",
            command=self.carregar_eleicoes
        )
        self.btn_atualizar.pack(side="left")

        # Frame para listar eleições
        self.frmEleicoes = tk.Frame(self.janela, bd=2, padx=5, pady=5, bg="white")
        self.frmEleicoes.grid(row=3, column=0, columnspan=3, padx=10, pady=(20, 20), sticky="nsew")

    def carregar_eleicoes(self):
        """Carrega as eleições do banco de dados e exibe na tela"""
        for widget in self.frmEleicoes.winfo_children():
            widget.destroy()

        eleicoes = self.control.listar_eleicoes()

        if not eleicoes:
            lbl_vazio = tk.Label(self.frmEleicoes, text="Nenhuma eleição cadastrada",
                                 font=("Arial", 16), fg="gray", bg="white")
            lbl_vazio.pack(pady=50)
            return

        num_colunas = min(3, len(eleicoes))  # Máximo 3 colunas
        for i in range(num_colunas):
            self.frmEleicoes.columnconfigure(i, weight=1)

        for idx, eleicao in enumerate(eleicoes):
            linha = idx // 3
            coluna = idx % 3
            self.criar_card_eleicao(eleicao, linha, coluna)

    def criar_card_eleicao(self, eleicao, linha, coluna):
        id_eleicao, titulo, data_inicio, data_fim = eleicao
        status = self.control.obter_status_eleicao(data_inicio, data_fim)
        data_inicio_fmt = self.control.formatar_data_exibicao(data_inicio)
        data_fim_fmt = self.control.formatar_data_exibicao(data_fim)

        card = tk.Frame(self.frmEleicoes, bd=2, relief="solid",
                        width=350, height=300, bg="white")
        card.grid(row=linha, column=coluna, padx=10, pady=10, sticky="nsew")
        card.grid_propagate(False)
        card.pack_propagate(False)

        lbl_titulo = tk.Label(card, text=titulo, font=("Arial", 15, "bold"),
                              fg="black", bg="white")
        lbl_titulo.pack(anchor="nw", padx=15, pady=(15, 5))

        info_text = f"Início: {data_inicio_fmt}\nFim: {data_fim_fmt}"
        lbl_info = tk.Label(card, text=info_text, font=("Arial", 10),
                            fg="gray", bg="white", justify="left")
        lbl_info.pack(anchor="nw", padx=15, pady=5)

        cor_status = self.obter_cor_status(status)
        lbl_status = tk.Label(card, text=status, bg=cor_status, fg="white",
                              font=("Arial", 13, "bold"), height=2)
        lbl_status.pack(fill="x", pady=5, padx=10, side="bottom")

        self.criar_botoes_acao(card, eleicao, status)

    def obter_cor_status(self, status):
        cores = {
            "Ativa": "green",
            "Agendada": "blue",
            "Encerrada": "red",
            "Indefinido": "gray"
        }
        return cores.get(status, "gray")

    def criar_botoes_acao(self, card, eleicao, status):
        id_eleicao = eleicao[0]

        if status == "Ativa":
            tk.Button(card, text="Abrir Urna", font=("Arial", 11, "bold"),
                      height=2, bg="white", relief="solid",
                      command=lambda: self.abrir_urna(id_eleicao)).pack(fill="x", pady=2, padx=10, side="bottom")

            tk.Button(card, text="Encerrar", font=("Arial", 11, "bold"),
                      height=2, bg="white", relief="solid",
                      command=lambda: self.encerrar_eleicao(id_eleicao)).pack(fill="x", pady=2, padx=10, side="bottom")

        elif status == "Agendada":
            tk.Button(card, text="Editar", font=("Arial", 11, "bold"),
                      height=2, bg="white", relief="solid",
                      command=lambda: self.editar_eleicao(eleicao)).pack(fill="x", pady=2, padx=10, side="bottom")

            tk.Button(card, text="Deletar", font=("Arial", 11, "bold"),
                      height=2, bg="white", relief="solid",
                      command=lambda: self.deletar_eleicao(id_eleicao)).pack(fill="x", pady=2, padx=10, side="bottom")

        elif status == "Encerrada":
            tk.Button(card, text="Resultados", font=("Arial", 11, "bold"),
                      height=2, bg="white", relief="solid",
                      command=lambda: self.ver_resultados(id_eleicao)).pack(fill="x", pady=2, padx=10, side="bottom")

            tk.Button(card, text="Arquivar", font=("Arial", 11, "bold"),
                      height=2, bg="white", relief="solid",
                      command=lambda: self.arquivar_eleicao(id_eleicao)).pack(fill="x", pady=2, padx=10, side="bottom")

    # ---------------- ações ----------------
    def abrir_urna(self, id_eleicao):
        messagebox.showinfo("Urna", f"Abrindo urna para eleição ID: {id_eleicao}")

    def encerrar_eleicao(self, id_eleicao):
        if messagebox.askyesno("Confirmar", "Deseja realmente encerrar esta eleição?"):
            messagebox.showinfo("Encerrar", f"Eleição {id_eleicao} encerrada")
            self.carregar_eleicoes()

    def editar_eleicao(self, eleicao):
        messagebox.showinfo("Editar", f"Editando eleição: {eleicao[1]}")

    def deletar_eleicao(self, id_eleicao):
        if messagebox.askyesno("Confirmar", "Deseja realmente deletar esta eleição?"):
            if self.control.deletar_eleicao(id_eleicao):
                messagebox.showinfo("Sucesso", "Eleição deletada com sucesso!")
                self.carregar_eleicoes()
            else:
                messagebox.showerror("Erro", "Erro ao deletar eleição!")

    def ver_resultados(self, id_eleicao):
        messagebox.showinfo("Resultados", f"Mostrando resultados da eleição ID: {id_eleicao}")

    def arquivar_eleicao(self, id_eleicao):
        if messagebox.askyesno("Confirmar", "Deseja arquivar esta eleição?"):
            messagebox.showinfo("Arquivar", f"Eleição {id_eleicao} arquivada")


# -------- iniciarTela --------
def iniciarTela(master=None):
    if master is None:  # se abrir sozinho
        gui = tk.Tk()
        Tela(gui)
        gui.mainloop()
    else:  # se abrir pelo ADM
        Tela(master)
