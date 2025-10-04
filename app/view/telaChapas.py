from ttkbootstrap import ttk
import ttkbootstrap as tb
from tkinter import messagebox
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import sys
import os

import telaADM, telaCriarChapas

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'control'))
import c_chapas  # type: ignore


class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Controle de Chapas')
        self.janela.geometry("1920x1080")

        # Bind para voltar à tela ADM com ESC
        self.janela.bind('<Escape>', lambda event: self.voltar_tela_adm())

        # Configurar grid
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=3)
        self.janela.rowconfigure(3, weight=1)

        # Label título
        self.lbl_ola = ttk.Label(self.janela,text="Controle de Chapas",font=("Courier", 20, "bold"))
        self.lbl_ola.grid(row=1, column=0, pady=(40, 10), padx=(20, 0))

        # Botão criar chapa
        self.btn_criar_chapa = ttk.Button(self.janela,text="+ Criar Nova Chapa",bootstyle="primary",width=20,command=self.criarChapa)
        self.btn_criar_chapa.grid(row=2, column=0, pady=(30, 60))

        # Frame container das chapas
        self.frmChapas = ttk.Frame(self.janela, padding=10)
        self.frmChapas.grid(row=3, column=0, columnspan=3, padx=10, pady=20, sticky="nsew")

        # Renderiza as chapas
        self.renderizar_chapas()

    def voltar_tela_adm(self):
        """Volta para a tela do administrador"""
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaADM.TelaADM(self.janela)

    # Navegar para tela de criação
    def criarChapa(self):
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaCriarChapas.iniciarTela()

    # Navegar para tela de edição
    def editarChapa(self, id, nome, slogan, logo, numero):
        for widget in self.janela.winfo_children():
            widget.destroy()
        telaCriarChapas.iniciarTela(
            modo_edicao=True,
            dados_chapa={'id': id, 'nome': nome, 'slogan': slogan, 'logo': logo, 'numero': numero}
        )

    def carregar_imagem(self, caminho_imagem, tamanho=(80, 80)):
        """Carrega e redimensiona uma imagem"""
        try:
            if caminho_imagem and caminho_imagem.strip():
                if os.path.exists(caminho_imagem):
                    imagem = Image.open(caminho_imagem)
                    imagem = imagem.resize(tamanho, Image.Resampling.LANCZOS)
                    return ImageTk.PhotoImage(imagem)
        except Exception as e:
            print(f"Erro ao carregar imagem {caminho_imagem}: {e}")
        return None

    # Excluir chapa
    def excluirChapa(self, id):
        confirm = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir esta chapa?")
        if confirm:
            resultado = c_chapas.Control(self).deletar_chapa(id)
            if resultado:
                messagebox.showinfo("Sucesso", "Chapa excluída com sucesso!")
                self.renderizar_chapas()
            else:
                messagebox.showerror("Erro", "Erro ao excluir chapa.")

    # Renderizar chapas
    def renderizar_chapas(self):
        # Limpa frames existentes
        for widget in self.frmChapas.winfo_children():
            widget.destroy()

        # Configura o grid para distribuir igualmente as 4 colunas
        for col in range(4):
            self.frmChapas.grid_columnconfigure(col, weight=1)

        chapas = c_chapas.Control(self).listar_chapas()

        if not chapas:
            ttk.Label(self.frmChapas,text="Nenhuma chapa cadastrada",font=("Courier", 16),bootstyle="secondary").grid(row=0, column=0, columnspan=4, pady=50)
            return

        for i, chapa in enumerate(chapas):
            # Mudança para suportar número
            if len(chapa) == 4:
                id_chapa, nome, slogan, logo = chapa
                numero = ""
            else:
                id_chapa, nome, slogan, numero, logo = chapa

            # Card de cada chapa
            frame_chapa = ttk.Frame(self.frmChapas, padding=10, relief="ridge", borderwidth=2)
            frame_chapa.grid(row=i // 4, column=i % 4, padx=10, pady=10, sticky="nsew")

            numero_exibicao = numero if numero else str(id_chapa)

            ttk.Label(frame_chapa,text=f"Chapa {numero_exibicao}",font=("Courier", 15, "bold")).pack(anchor="n", pady=5)

            # Imagem/logo
            imagem_tk = self.carregar_imagem(logo, (80, 80))
            if imagem_tk:
                lbl_imagem = ttk.Label(frame_chapa, image=imagem_tk)
                lbl_imagem.image = imagem_tk
                lbl_imagem.pack(pady=5)
            else:
                ttk.Label(frame_chapa,text="Sem imagem",font=("Courier", 10),bootstyle="secondary").pack(pady=5)

            # Nome da chapa
            ttk.Label(frame_chapa,text=nome,font=("Courier", 14, "bold"),wraplength=250).pack(pady=5)

            # Slogan
            if slogan:
                ttk.Label(frame_chapa,text=slogan,font=("Courier", 11),bootstyle="secondary",wraplength=250).pack(pady=2)

            # Botões ação
            frm_botoes = ttk.Frame(frame_chapa)
            frm_botoes.pack(fill="x", pady=10)

            ttk.Button(frm_botoes,text="Editar",bootstyle="info-outline",command=lambda id=id_chapa, n=nome, s=slogan, l=logo, num=numero: self.editarChapa(id, n, s, l, num)).pack(side="left", expand=True, fill="x", padx=2)

            ttk.Button(frm_botoes,text="Excluir",bootstyle="danger",command=lambda id=id_chapa: self.excluirChapa(id)).pack(side="left", expand=True, fill="x", padx=2)


def iniciarTela():
    app = tb.Window(themename="superhero")
    Tela(app)
    app.mainloop()
