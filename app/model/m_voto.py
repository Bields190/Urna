from model import Model

class Voto(Model):
    def __init__(self, eleicao_id, chapa_id, id=None):
        super().__init__()
        self.id = id
        self.eleicao = eleicao_id
        self.chapa = chapa_id

    def salvar(self):
        sql = f"INSERT INTO voto (eleicao_id, chapa_id) VALUES ({self.eleicao}, {self.chapa})"
        result = self.insert(sql)
        if result:
            aux = self.get(f"SELECT id FROM voto WHERE eleicao_id = {self.eleicao} AND chapa_id = {self.chapa}")
            self.id = aux[0][0]
            print("Voto salvo com sucesso!")
            return True
        else:
            print("Erro ao salvar voto.")
            return False

# sem necessidade de criar o resto do crud, uma vez que votos não são alterados ou deletados