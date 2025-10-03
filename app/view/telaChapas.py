import tkinter as tk
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
        self.janela.configure(bg="white")  
        self.janela.bind('<Escape>', lambda event: self.voltar_tela_adm())    
    
        self.janela.columnconfigure(2, weight=3)
        self.janela.rowconfigure(3, weight=3)
        self.janela.rowconfigure(3, weight=1)

        self.lbl_ola = tk.Label(text="Controle de Chapas",font=("Arial",20,"bold"), bg="white")
        self.lbl_ola.grid(row=1,column=0, pady=(40, 10), padx=(20,0))
        
        self.btn_criar_chapa = tk.Button(text="+ Criar Nova Chapa", font=("Arial",16,"bold"), command=self.criarChapa)
        self.btn_criar_chapa.grid(row=2,column=0,pady=(30,60))
   
        self.frmChapas = tk.Frame(self.janela, bd=2, padx=5, pady=5,bg="white")
        self.frmChapas.grid(row=3, column=0, columnspan=3, padx=10, pady=(20,20), sticky="nsew")

        # Renderiza as chapas na tela
        self.renderizar_chapas()

    def voltar_tela_adm(self):
        """Volta para a tela do administrador"""
        self.janela.destroy()
        telaADM.iniciarTela()

    # Navegar para tela de criação
    def criarChapa(self):
        self.janela.destroy()
        telaCriarChapas.iniciarTela()

    # Navegar para tela de edição
    def editarChapa(self, id, nome, slogan, logo):
        self.janela.destroy()
        telaCriarChapas.iniciarTela(modo_edicao=True, dados_chapa={'id': id, 'nome': nome, 'slogan': slogan, 'logo': logo})

    def carregar_imagem(self, caminho_imagem, tamanho=(80, 80)):
        """Carrega e redimensiona uma imagem"""
        try:
            if caminho_imagem and caminho_imagem.strip():
                import os
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

    # Renderizar as chapas do banco
    def renderizar_chapas(self):
        # Limpa frames existentes
        for widget in self.frmChapas.winfo_children():
            widget.destroy()

        # Configura o grid para distribuir igualmente as 4 colunas
        self.frmChapas.grid_columnconfigure(0, weight=1)
        self.frmChapas.grid_columnconfigure(1, weight=1)
        self.frmChapas.grid_columnconfigure(2, weight=1)
        self.frmChapas.grid_columnconfigure(3, weight=1)

        chapas = c_chapas.Control(self).listar_chapas()

        if not chapas:
            # Se não há chapas, mostra uma mensagem
            tk.Label(self.frmChapas, 
                text="Nenhuma chapa cadastrada", 
                font=("Arial", 16), 
                fg="gray", 
                bg="white").grid(row=0, column=0, columnspan=4, pady=50)
            return

        for i, chapa in enumerate(chapas):
            id_chapa, nome, slogan, logo = chapa

            # Frame com tamanho fixo para cada chapa
            frame_chapa = tk.Frame(self.frmChapas, bd=2, relief="solid", width=300, height=300, bg="white")
            frame_chapa.grid(row=i//4, column=i%4, padx=10, pady=10, sticky="nsew")
            frame_chapa.grid_propagate(False)
            frame_chapa.pack_propagate(False)

            # Container principal
            container = tk.Frame(frame_chapa, bg="white")
            container.pack(fill="both", expand=True, padx=10, pady=10)

            # Label do número da chapa
            tk.Label(container, 
                text=f"Chapa {id_chapa}", 
                font=("Arial", 15, "bold"), 
                fg="black", 
                bg="white").pack(anchor="n")

            # Frame para a imagem
            frame_imagem = tk.Frame(container, bg="white", height=100)
            frame_imagem.pack(pady=5, fill="x")
            frame_imagem.pack_propagate(False)

            # Tentar carregar e exibir a imagem
            imagem_tk = self.carregar_imagem(logo, (80, 80))
            if imagem_tk:
                lbl_imagem = tk.Label(frame_imagem, image=imagem_tk, bg="white")
                lbl_imagem.image = imagem_tk  # Manter referência
                lbl_imagem.pack()
            else:
                # Placeholder se não há imagem
                tk.Label(frame_imagem, 
                    text="Sem imagem", 
                    font=("Arial", 10), 
                    fg="gray", 
                    bg="white").pack()

            # Label do nome da chapa
            tk.Label(container, 
                text=nome, 
                font=("Arial", 16, "bold"), 
                fg="black", 
                bg="white",
                wraplength=280).pack(pady=5)

            # Label do slogan (se existir)
            if slogan:
                tk.Label(container, 
                    text=slogan, 
                    font=("Arial", 11), 
                    fg="gray", 
                    bg="white",
                    wraplength=280).pack(pady=2)

            # Frame para os botões
            frame_botoes = tk.Frame(container, bg="white")
            frame_botoes.pack(side="bottom", fill="x", pady=5)

            # Botões de ação
            tk.Button(frame_botoes, 
                text="Editar",
                font=("Arial", 12, "bold"),
                height=2, 
                bg="white",
                relief="solid",
                command=lambda id=id_chapa, n=nome, s=slogan, l=logo: self.editarChapa(id, n, s, l)
                ).pack(side="left", fill="x", expand=True, padx=(0, 2))
            
            tk.Button(frame_botoes, 
                text="Excluir", 
                bg="red", 
                fg="white", 
                font=("Arial", 12, "bold"),
                height=2,
                command=lambda id=id_chapa: self.excluirChapa(id)
                ).pack(side="left", fill="x", expand=True, padx=(2, 0))



def iniciarTela():
        gui = tk.Tk()
        Tela(gui)
        gui.mainloop()