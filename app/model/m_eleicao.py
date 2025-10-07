from model import Model

class Eleicao(Model):
    def __init__(self, titulo, data_inicio, data_fim, id=None):
        super().__init__()  # CONSTRUTOR
        self.id = id
        self.titulo = titulo
        self.data_inicio = data_inicio
        self.data_fim = data_fim

    def salvar(self):
        sql_ver = f"SELECT * FROM eleicao WHERE titulo = '{self.titulo}' AND data_inicio = '{self.data_inicio}' AND data_fim = '{self.data_fim}'"
        ver = self.get(sql_ver)
        if not ver:
            sql = f"INSERT INTO eleicao (titulo, data_inicio, data_fim) VALUES ('{self.titulo}', '{self.data_inicio}', '{self.data_fim}')"
            result = self.insert(sql)
            if result:
                aux = self.get(f"SELECT id FROM eleicao WHERE titulo = '{self.titulo}' and data_inicio = '{self.data_inicio}' and data_fim = '{self.data_fim}'")
                self.id = aux[0][0]
                print("Eleição salva com sucesso!")
                return True
            else:
                print("Erro ao salvar eleição.")
                return False
        else:
            print("Eleição já existe no sistema.")
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
        
    def ver(self, id):
        sql = f"SELECT * FROM eleicao WHERE id = {id}"
        result = self.get(sql)
        if result:
            return result
        else:
            print("Eleição não encontrada.")
            return None
    
    @classmethod
    def listar(cls):
        sql = "SELECT * FROM eleicao ORDER BY data_inicio DESC"
        result = Model().get(sql)
        if result:
            return result
        return []