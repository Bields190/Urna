from model import Model

class Cedula(Model):
    def __init__(self, eleicao_id, votado_em, id=None):
        super().__init__()  # CONSTRUTOR
        self.id = id
        self.eleicao_id = eleicao_id
        self.votado_em = votado_em

    def salvar(self):
        sql = f"INSERT INTO cedula (eleicao_id, votado_em) VALUES ({self.eleicao_id}, '{self.votado_em}')"
        result = self.insert(sql)
        if result:
            aux = self.get(f"SELECT id FROM cedula WHERE eleicao_id = {self.eleicao_id} and votado_em = '{self.votado_em}'")
            self.id = aux[0][0]
            print("Cédula salva com sucesso!")
            return True
        else:
            print("Erro ao salvar cédula.")
            return False

#por que criariamos atualizar, deletar, listar e buscar por id em uma cédula?
#se em eleições quando uma cédula é criada uma vez, nunca mais é alterada, deletada ou listada