import ttkbootstrap as ttk

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Urna Eletrônica")
        self.janela.geometry("1920x1080")
        self.oi = ttk.Label(self.janela, text="TÁ FUNCIONANDO", font=("Arial", 100))
        self.oi.pack()

gui = ttk.Window()
tela = Tela(gui)
gui.mainloop()