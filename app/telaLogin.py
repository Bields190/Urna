
import tkinter as tk
from PIL import Image, ImageTk

class Tela:

    def __init__(self, master):
        self.janela = master
        self.janela.title('Tela de Login')
        self.janela.geometry("1920x1080")

        self.frm_principal = tk.Frame(self.janela,bg='white')
        self.frm_principal.pack(fill='both',expand=True)
        self.frm = tk.Frame(self.frm_principal,bg='white')
        self.frm.pack(expand=True)
        
        self.imagem = tk.PhotoImage(file="src\Logo.png")
        self.imagem = self.imagem.subsample(3,3)
        self.lbl = tk.Label(self.frm, image=self.imagem, bg='white')
        self.lbl.image = self.imagem
        self.lbl.pack()
        
#------entry e label de matricula---------
        self.lbl1 = tk.Label(self.frm, text='Matricula:', bg='white',font=("Arial",18))
        self.lbl1.pack(pady=(40, 0))
        self.entry1 = tk.Entry(self.frm, width=40)
        self.entry1.pack()
        
#------entry e label de senha---------
        self.lbl2 = tk.Label(self.frm, text='Senha:',bg='white',font=("Arial",18))
        self.lbl2.pack()
        self.entry2 = tk.Entry(self.frm, show='*', width=40)
        self.entry2.pack(pady=5)
        
        self.btn_entrar = tk.Button(self.frm, text='Entrar',bg='black',fg='white', width=10,font=("Arial",14))
        self.btn_entrar.pack(pady=10)


app = tk.Tk()
Tela(app)
app.mainloop()