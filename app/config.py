import tkinter as tk

class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.title("Urna Eletrônica")
        self.janela.geometry("1920x1080")
        self.oi = tk.Label(self.janela, text="TÁ FUNCIONANDO", font=("Arial", 100))
        self.oi.pack()

gui = tk.Tk()
tela = Tela(gui)
gui.mainloop()