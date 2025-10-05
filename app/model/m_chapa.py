from model import Model

class Chapa(Model):
    def __init__(self, nome, slogan, logo, numero=None, id=None):
        super().__init__()  # CONSTRUTOR
        self.id = id
        self.nome = nome
        self.slogan = slogan
        self.logo = logo
        self.numero = numero

    def salvar(self):
        sql_ver = f"SELECT * FROM chapa WHERE nome = '{self.nome}' AND slogan = '{self.slogan}' AND logo = '{self.logo}'"
        ver = self.get(sql_ver)
        if not ver:
            sql = f"INSERT INTO chapa (nome, slogan, logo, numero) VALUES ('{self.nome}', '{self.slogan}', '{self.logo}', '{self.numero}')"
            result = self.insert(sql)
            if result:
                aux = self.get(f"SELECT id FROM chapa WHERE nome = '{self.nome}' and slogan = '{self.slogan}'")
                self.id = aux[0][0]
                print("Chapa salva com sucesso!")
                return True
            else:
                print("Erro ao salvar chapa.")
                return False
        else:
            print("Chapa já existe no sistema.")
            return False
    
    def atualizar(self):
        sql = f"UPDATE chapa SET nome = '{self.nome}', slogan = '{self.slogan}', logo = '{self.logo}', numero = '{self.numero}' WHERE id = {self.id}"
        result = self.update(sql)
        if result:
            print("Chapa atualizada com sucesso!")
            return True
        else:
            print("Erro ao atualizar chapa.")
            return False

    def deletar(self):
        sql = f"DELETE FROM chapa WHERE id = {self.id}"
        result = self.delete(sql)
        if result:
            print("Chapa deletada com sucesso!")
            return True
        else:
            print("Erro ao deletar chapa.")
            return False

    def ver(self, id):
        sql = f"SELECT * FROM chapa WHERE id = {id}"
        result = self.get(sql)
        if result:
            return result
        else:
            print("Chapa não encontrada.")
            return None
    
    @classmethod
    def listar(cls):
        sql = "SELECT * FROM chapa"
        result = Model().get(sql)
        if result:
            return result
        return []
    
    @classmethod
    def listar_por_eleicao(cls, eleicao_id):
        """
        Retorna todas as chapas que têm candidatos na eleição específica.
        """
        sql = f"""
        SELECT DISTINCT c.id, c.nome, c.slogan, c.logo
        FROM Chapa c
        JOIN Candidato ca ON ca.chapa_id = c.id
        """
        result = Model().get(sql)
        return result if result else []