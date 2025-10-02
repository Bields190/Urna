import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))

import m_cargos  # type: ignore


class Control:
    def __init__(self, tela=None):
        self.tela = tela

    def adicionar_cargo(self):
        nome = str(self.tela.ent_cargo.get())
        descricao = str(self.tela.ent_descricao.get())
        cargo = m_cargos.Cargo(nome, descricao)
        cargo.salvar()

    def listar_cargos(self):
        return m_cargos.Cargo.listar()

    def atualizar_cargo(self, id, nome, descricao):
        cargo = m_cargos.Cargo(nome, descricao, id=id)
        cargo.atualizar()

    def deletar_cargo(self, id):
        cargo = m_cargos.Cargo("", "", id=id)
        cargo.deletar()
