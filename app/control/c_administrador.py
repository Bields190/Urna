import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))

import m_administrador  # type: ignore

class Control:
    def __init__(self, tela=None):
        self.tela = tela

    def adicionar_administrador(self, nome, matricula, email, senha):
        admin = m_administrador.Admin(nome, senha, matricula, email)
        return admin.salvar()

    def listar_administradores(self):
        return m_administrador.Admin.listar()

    def atualizar_administrador(self, id, nome, matricula, email, senha=None):
        admin = m_administrador.Admin(nome, senha, matricula, email, 0, id)
        return admin.atualizar()

    def deletar_administrador(self, id):
        admin = m_administrador.Admin("", "", "", "", 0, id)
        return admin.deletar()

    def login(self):
        usuario = str(self.tela.entry1.get())
        senha = str(self.tela.entry2.get())
        admin = m_administrador.Admin(usuario, senha)
        return admin.verificar()
