from model import Model

class Candidato(Model):
    def __init__(self, nome, chapa_id, cargo_id, id=None):
        super().__init__()  # CONSTRUTOR
        self.id = id
        self.nome = nome
        self.chapa_id = chapa_id
        self.cargo_id = cargo_id

    def salvar(self):
        sql_ver = f"SELECT * FROM candidato WHERE nome = '{self.nome}' AND chapa_id = {self.chapa_id} AND cargo_id = {self.cargo_id}"
        ver = self.get(sql_ver)
        if not ver:
            sql = f"INSERT INTO candidato (nome, chapa_id, cargo_id) VALUES ('{self.nome}', {self.chapa_id}, {self.cargo_id})"
            result = self.insert(sql)
            if result:
                aux = self.get(f"SELECT id FROM candidato WHERE nome = '{self.nome}' and chapa_id = {self.chapa_id} and cargo_id = {self.cargo_id}")
                self.id = aux[0][0]
                print("Candidato salvo com sucesso!")
                return True
            else:
                print("Erro ao salvar candidato.")
                return False
        else:
            print("Candidato já existe no sistema.")
            return False
    
    def atualizar(self):
        sql = f"UPDATE candidato SET nome = '{self.nome}', chapa_id = {self.chapa_id}, cargo_id = {self.cargo_id} WHERE id = {self.id}"
        result = self.update(sql)
        if result:
            print("Candidato atualizado com sucesso!")
            return True
        else:
            print("Erro ao atualizar candidato.")
            return False

    def deletar(self):
        sql = f"DELETE FROM candidato WHERE id = {self.id}"
        result = self.delete(sql)
        if result:
            print("Candidato deletado com sucesso!")
            return True
        else:
            print("Erro ao deletar candidato.")
            return False

    def ver(self, id):
        sql = f"SELECT * FROM candidato WHERE id = {id}"
        result = self.get(sql)
        if result:
            return result
        else:
            print("Candidato não encontrado.")
            return None