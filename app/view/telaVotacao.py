import tkinter as tk

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.geometry("1920x1080")
        self.janela.configure(bg="white")

        frmPrincipal = tk.Frame(self.janela, bg="white")
        frmPrincipal.pack(fill="both", expand=True)

        frmTopo = tk.Frame(frmPrincipal, bg="white")
        frmTopo.pack(fill="both", pady=20)

        self.labelEleicao = tk.Label(frmTopo, text="Eleição 15", font=("Arial", 26, "bold"), bg="white")
        self.labelEleicao.pack(side="left", padx=45)

        frmNumero = tk.Frame(frmPrincipal, bg="white")
        frmNumero.pack(pady=(30,20))

        self.lblInserirNumero = tk.Label(frmNumero, text="Escreva o número da chapa:", font=("Arial", 18), bg="white")
        self.lblInserirNumero.pack()

        self.entInserirNumero = tk.Entry(frmNumero, font=("Arial", 14), width=10)
        self.entInserirNumero.pack(pady=10, ipady=3)

# -----------informações do voto (chaopa)--------------
        frmChapa = tk.Frame(frmPrincipal, bg="white")
        frmChapa.pack(pady=5, expand=True)

#--------foto da chapa selecionada---------------
        self.frmFoto = tk.Frame(frmChapa, width=400, height=400, relief="solid", bd=1, bg="#f5f5f5")
        self.frmFoto.pack(side="left", padx=50)
        self.frmFoto.pack_propagate(False)

# ------------slogan e informações----------------
        frmInformacoes = tk.Frame(frmChapa, bg="white")
        frmInformacoes.pack(side="left", padx=20)

        self.frmSlogan = tk.Frame(frmInformacoes, width=600, height=80, relief="solid", bd=1, bg="white")
        self.frmSlogan.pack(pady=10)
        self.frmSlogan.pack_propagate(False)

        self.frmInfoChapa = tk.Frame(frmInformacoes, width=600, height=200, relief="solid", bd=1, bg="white")
        self.frmInfoChapa.pack(pady=10)
        self.frmInfoChapa.pack_propagate(False)

# ---------------- Botões de confirmar ou cancelar voto----------------
        frmConfirmacao = tk.Frame(frmPrincipal, bg="white")
        frmConfirmacao.pack(pady=(30,150))

        self.btnConfirmar = tk.Button(frmConfirmacao, text="Confirmar", font=("Arial", 18), bg="green", fg="white", width=12, height=2)
        self.btnConfirmar.pack(side="left", padx=40)

        self.btnCancelar = tk.Button(frmConfirmacao, text="Cancelar", font=("Arial", 18), bg="red", fg="white", width=12, height=2)
        self.btnCancelar.pack(side="left", padx=40)


gui = tk.Tk()
Tela(gui)
gui.mainloop()
