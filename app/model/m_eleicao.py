from model import Model

class Eleicao(Model):
    def __init__(self, titulo, data_inicio, data_fim, id=None):
        super().__init__()  # CONSTRUTOR
        self.id = id
        self.titulo = titulo
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def salvar(self):
        sql = f"INSERT INTO eleicao (titulo, data_inicio, data_fim) VALUES ('{self.titulo}', '{self.data_inicio}', '{self.data_fim}')"
        result = self.insert(sql)
        if result:
            print("Eleição salva com sucesso!")
            return True
        else:
            print("Erro ao salvar eleição.")
            return False

    def atualizar(self):
        sql = f"UPDATE eleicao SET titulo = '{self.titulo}', data_inicio = '{self.data_inicio}', data_fim = '{self.data_fim}' WHERE id = {self.id}"
        result = self.update(sql)
        if result:
            print("Eleição atualizada com sucesso!")
            return True
        else:
            print("Erro ao atualizar eleição.")
            return False

    def deletar(self):
        sql = f"DELETE FROM eleicao WHERE id = {self.id}"
        result = self.delete(sql)
        if result:
            print("Eleição deletada com sucesso!")
            return True
        else:
            print("Erro ao deletar eleição.")
            return False