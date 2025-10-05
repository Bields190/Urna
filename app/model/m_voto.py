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
        
    @classmethod
    def contar_por_chapa(cls, chapa_id):
        sql = f"SELECT COUNT(*) FROM voto WHERE chapa_id = {chapa_id}"
        result = Model().get(sql)
        return result[0][0] if result else 0

    @classmethod
    def contar_total_eleicao(cls, eleicao_id):
        sql = f"SELECT COUNT(*) FROM voto WHERE eleicao_id = {eleicao_id}"
        result = Model().get(sql)
        return result[0][0] if result else 0

# sem necessidade de criar o resto do crud, uma vez que votos não são alterados ou deletados