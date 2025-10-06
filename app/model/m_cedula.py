import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '.'))
from model import Model
from datetime import datetime

class Cedula(Model):
    def __init__(self, eleicao_id, email_votante, id=None):
        super().__init__()  # CONSTRUTOR
        self.id = id
        self.eleicao_id = eleicao_id
        self.email_votante = email_votante
        self.data_emissao = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def salvar(self):
        sql = f"INSERT INTO cedula (eleicao_id, email_votante, data_emissao) VALUES ({self.eleicao_id}, '{self.email_votante}', '{self.data_emissao}')"
        result = self.insert(sql)
        if result:
            aux = self.get(f"SELECT id FROM cedula WHERE eleicao_id = {self.eleicao_id} and email_votante = '{self.email_votante}' ORDER BY id DESC LIMIT 1")
            if aux:
                self.id = aux[0][0]
                print("Cédula salva com sucesso!")
                return True
        print("Erro ao salvar cédula.")
        return False
    
    @classmethod
    def verificar_voto_existente(cls, eleicao_id, email_votante):
        """Verifica se o email já votou nesta eleição"""
        cedula = cls(eleicao_id, email_votante)
        sql = f"SELECT id FROM cedula WHERE eleicao_id = {eleicao_id} AND email_votante = '{email_votante}'"
        result = cedula.get(sql)
        return len(result) > 0 if result else False

#por que criariamos atualizar, deletar, listar e buscar por id em uma cédula?
#se em eleições quando uma cédula é criada uma vez, nunca mais é alterada, deletada ou listada