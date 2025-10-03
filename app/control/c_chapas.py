import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))

import m_chapa  # type: ignore


class Control:
    def __init__(self, tela=None):
        self.tela = tela

    def adicionar_chapa(self):
        nome = str(self.tela.ent_nome.get())
        slogan = str(self.tela.ent_slogan.get())
        numero = str(self.tela.ent_numero.get()) if hasattr(self.tela, 'ent_numero') else ""
        logo = str(self.tela.ent_logo.get()) if hasattr(self.tela, 'ent_logo') else ""
        chapa = m_chapa.Chapa(nome, slogan, logo, numero)
        return chapa.salvar()

    def listar_chapas(self):
        return m_chapa.Chapa.listar()

    def atualizar_chapa(self, id, nome, slogan, logo, numero):
        chapa = m_chapa.Chapa(nome, slogan, logo, numero, id=id)
        return chapa.atualizar()

    def deletar_chapa(self, id):
        chapa = m_chapa.Chapa("", "", "", "", id=id)
        return chapa.deletar()