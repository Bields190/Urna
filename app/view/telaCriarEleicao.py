import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Criação de Eleições')
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")

        self.lbl_topo = tk.Label(self.janela, text="Criar Eleição", font=("Arial", 35, "bold"), bg="white")
        self.lbl_topo.pack(pady=15)

        self.frm_entrada = tk.Frame(self.janela, bg="white")
        self.frm_entrada.pack(pady=5)

#------entry e títula da eleição------
        self.lbl1 = tk.Label(self.frm_entrada, text='Título:', bg='white',font=("Arial",25))
        self.lbl1.pack(pady=(40, 0))
        self.entry1 = tk.Entry(self.frm_entrada, width=40)
        self.entry1.pack(pady=15)

#------implementação de data em formato dataentry------
        self.lbl2 = tk.Label(self.frm_entrada, text='Data de Início:', bg='white', font=("Arial",25))
        self.lbl2.pack()
        self.entry2 = ttk.DateEntry(self.frm_entrada, dateformat='%d-%m-%Y', bootstyle=DARK, width=36)
        self.entry2.pack(pady=15)

        self.lbl3 = tk.Label(self.frm_entrada, text='Data de Encerramento:', bg='white', font=("Arial",25))
        self.lbl3.pack()
        self.entry3 = ttk.DateEntry(self.frm_entrada, dateformat='%d-%m-%Y', bootstyle=DARK, width=36)
        self.entry3.pack(pady=15)

#------botão de salvar------
        style = ttk.Style()
        style.configure("Salvar.TButton", font=("Arial", 20, "bold"), foreground="white", background="black", borderwidth=0)
        self.btn_salvar = ttk.Button(self.janela, text="Salvar", style="Salvar.TButton")
        self.btn_salvar.pack(pady=20)

#------chapa------
        self.frm_chapa = tk.Frame(self.janela, bg="white")
        self.frm_chapa.pack(side="left", anchor="s", padx=20, pady=20)

        self.chapas = []

        self.add_chapa_btn = self.criar_card_adicionar()
        self.add_chapa_btn.grid(row=0, column=0, padx=10)

    def criar_card_adicionar(self):
        frm_card = tk.Frame(
            self.frm_chapa, 
            bg="white", 
            highlightbackground="black", 
            highlightthickness=2, 
            width=425, height=425
        )
        frm_card.pack_propagate(False)

        lbl = tk.Label(frm_card, text="Adicionar Chapa", font=("Arial", 30), bg="white")
        lbl.pack(pady=(80,45))

        style = ttk.Style()
        style.configure("Preto.TButton", font=("Arial", 40, "bold"), foreground="white", background="black", borderwidth=0, focusthickness=0, focustcolor="black")

        btn = ttk.Button(frm_card, text="+", style="Preto.TButton", command=self.abrir_tela_chapa)
        btn.pack()

        return frm_card
    
    def criar_card_chapa(self, nome):
        frm_card = tk.Frame(
            self.frm_chapa, 
            bg="white", 
            highlightbackground="black", 
            highlightthickness=2, 
            width=425, height=425
        )
        frm_card.pack_propagate(False)

        lbl = tk.Label(frm_card, text=nome, font=("Arial", 40, "bold"), bg="white")
        lbl.pack(expand=True)

        return frm_card
    
    def abrir_tela_chapa(self):
        self.janela_chapa = tk.Toplevel(self.janela)
        self.janela_chapa.title("Cadastrar Chapa")
        self.janela_chapa.geometry("1920x1080")
        self.janela_chapa.configure(bg="white")

        self.lbl_topo_tela_nova = tk.Label(self.janela_chapa, text="Adicionar Chapa", font=("Arial", 35, "bold"), bg="white")
        self.lbl_topo_tela_nova.pack(pady=15)

        self.frm_tela2 = tk.Frame(self.janela_chapa, bg="white")
        self.frm_tela2.pack(pady=10)

        tk.Label(self.frm_tela2, text="Nome da Chapa:", font=("Arial", 25), bg="white").pack(pady=15)
        self.entry_nome_chapa = tk.Entry(self.frm_tela2, width=40)
        self.entry_nome_chapa.pack(pady=15)

#-----função para o entry número da chapa aceitar somente número------
        def validar_numero(texto):
            if texto == "" or texto.isdigit():
                return True
            return False

        vcmd = (self.frm_tela2.register(validar_numero), '%P')

        tk.Label(self.frm_tela2, text="Número da Chapa", font=("Arial", 25), bg="white").pack(pady=15)
        self.entry_nmr_chapa = tk.Entry(self.frm_tela2, width=40, validate="key", validatecommand=vcmd)
        self.entry_nmr_chapa.pack(pady=15)

        tk.Label(self.frm_tela2, text="Slogan:", font=("Arial", 25), bg="white").pack(pady=15)
        self.entry_slogan_chapa = tk.Entry(self.frm_tela2, width=40)
        self.entry_slogan_chapa.pack(pady=15)

        style = ttk.Style()
        style.configure("Salvar.TButton", font=("Arial", 20, "bold"), foreground="white", background="black", borderwidth=0)
        btn_salvar = ttk.Button(self.janela_chapa, text="Salvar", style="Salvar.TButton", command=self.salvar_chapa)
        btn_salvar.pack(pady=20)

    def salvar_chapa(self):
        nome_chapa = self.entry_nome_chapa.get().strip()
        if not nome_chapa:
            nome_chapa = f"Chapa {len(self.chapas)+1}"

        nova_chapa = self.criar_card_chapa(nome_chapa)
        col = len(self.chapas)  #posição
        nova_chapa.grid(row=0, column=col, padx=10)

        self.chapas.append(nova_chapa)

#------mover o "Adicionar Chapa" para a próxima posição------
        self.add_chapa_btn.grid(row=0, column=len(self.chapas), padx=10)
        self.janela_chapa.destroy()

app = tk.Tk()
Tela(app)
app.mainloop()