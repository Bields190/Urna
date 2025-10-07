import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from model import Model

class Voto(Model):
    def __init__(self, eleicao_id, chapa_id, cedula_id, id=None):
        super().__init__()
        self.id = id
        self.eleicao = eleicao_id
        self.chapa = chapa_id
        self.cedula = cedula_id

    def salvar(self):
        sql = f"INSERT INTO voto (eleicao_id, chapa_id, cedula_id) VALUES ({self.eleicao}, {self.chapa}, {self.cedula})"
        result = self.insert(sql)
        if result:
            aux = self.get(f"SELECT id FROM voto WHERE eleicao_id = {self.eleicao} AND chapa_id = {self.chapa} AND cedula_id = {self.cedula} ORDER BY id DESC LIMIT 1")
            if aux:
                self.id = aux[0][0]
                print("Voto salvo com sucesso!")
                return True
        print("Erro ao salvar voto.")
        return False
        
    @classmethod
    def contar_por_chapa(cls, chapa_id, eleicao_id):
        """
        Conta os votos de uma chapa, APENAS para a eleição informada.
        """
        sql = f"SELECT COUNT(*) FROM voto v WHERE v.chapa_id = {chapa_id} AND v.eleicao_id = {eleicao_id}"
        result = Model().get(sql)
        return result[0][0] if result else 0

    @classmethod
    def contar_total_eleicao(cls, eleicao_id):
        """
        Conta o total de votos APENAS para a eleição informada.
        """
        sql = f"SELECT COUNT(*) FROM voto WHERE eleicao_id = {eleicao_id}"
        result = Model().get(sql)
        return result[0][0] if result else 0