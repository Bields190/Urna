from model import Model

class Cargo(Model):
    def __init__(self, nome, descricao, id=None):
        super().__init__()  # CONSTRUTOR
        self.id = id
        self.nome = nome
        self.descricao = descricao

    def salvar(self):
        sql_ver = f"SELECT * FROM cargo WHERE nome = '{self.nome}' AND descricao = '{self.descricao}'"
        ver = self.get(sql_ver)
        if not ver:
            sql = f"INSERT INTO cargo (nome, descricao) VALUES ('{self.nome}', '{self.descricao}')"
            result = self.insert(sql)
            if result:
                aux = self.get(f"SELECT id FROM cargo WHERE nome = '{self.nome}'")
                self.id = aux[0][0]
                print("Cargo salvo com sucesso!")
                return True
            else:
                print("Erro ao salvar cargo.")
                return False
        else:
            print("Cargo já existe no sistema.")
            return False
    
    def atualizar(self):
        sql = f"UPDATE cargo SET nome = '{self.nome}', descricao = '{self.descricao}' WHERE id = {self.id}"
        result = self.update(sql)
        if result:
            print("Cargo atualizado com sucesso!")
            return True
        else:
            print("Erro ao atualizar cargo.")
            return False

    def deletar(self):
        sql = f"DELETE FROM cargo WHERE id = {self.id}"
        result = self.delete(sql)
        if result:
            print("Cargo deletado com sucesso!")
            return True
        else:
            print("Erro ao deletar cargo.")
            return False

    def ver(self, id):
        sql = f"SELECT * FROM cargo WHERE id = {id}"
        result = self.get(sql)
        if result:
            return result
        
    @classmethod
    def listar(self):
        sql = f"SELECT * FROM cargo"
        result = Model().get(sql)
        if result:
            return result
        return []
