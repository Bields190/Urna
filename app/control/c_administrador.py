import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))

import m_administrador

class Control:
    def __init__(self, tela):
        self.tela = tela

    def login(self):
        usuario = str(self.tela.entry1.get())
        senha = str(self.tela.entry2.get())
        admin = m_administrador.Admin(usuario, senha)
        if admin.verificar():
            return True
        else:
            return False
