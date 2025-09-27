import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))

import m_eleitor

class Control:
    def __init__(self, tela):
        self.tela = tela

    def login(self):
        usuario = str(self.tela.entry1.get())
        senha = str(self.tela.entry2.get())
        eleitor = m_eleitor.Eleitor(usuario, senha)
        if eleitor.verificar():
            return True
        else:
            return False