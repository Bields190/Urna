from model import Model

class Admin(Model):
    def __init__(self, usuario, senha, matricula=None, email_institucional=None, master=0, id=None):
        super().__init__()  # CONSTRUTOR
        self.id = id
        self.usuario = usuario
        self.senha = senha
        self.matricula = matricula
        self.email_institucional = email_institucional
        self.master = master

    def verificar(self):
        sql = f"SELECT * FROM Administrador WHERE usuario = '{self.usuario}' AND senha = '{self.senha}'"
        result = self.get(sql)
        if result:
            print("Usuário Encontrado e Logado com sucesso!")
            return True
        else:
            print("Usuário ou Senha incorretos!")
            return False

    def salvar(self):
        # Verificar se já existe administrador com a mesma matrícula ou email
        sql_ver = f"SELECT * FROM Administrador WHERE matricula = '{self.matricula}' OR email_institucional = '{self.email_institucional}'"
        ver = self.get(sql_ver)
        if not ver:
            sql = f"INSERT INTO Administrador (usuario, senha, matricula, email_institucional, master) VALUES ('{self.usuario}', '{self.senha}', '{self.matricula}', '{self.email_institucional}', {self.master})"
            result = self.insert(sql)
            if result:
                aux = self.get(f"SELECT id FROM Administrador WHERE matricula = '{self.matricula}'")
                self.id = aux[0][0]
                print("Administrador salvo com sucesso!")
                return True
            else:
                print("Erro ao salvar administrador.")
                return False
        else:
            print("Administrador com esta matrícula ou email já existe no sistema.")
            return False
    
    def atualizar(self):
        # Verificar duplicatas excluindo o próprio registro
        sql_ver = f"SELECT * FROM Administrador WHERE (matricula = '{self.matricula}' OR email_institucional = '{self.email_institucional}') AND id != {self.id}"
        ver = self.get(sql_ver)
        if not ver:
            if self.senha:
                sql = f"UPDATE Administrador SET usuario = '{self.usuario}', matricula = '{self.matricula}', email_institucional = '{self.email_institucional}', senha = '{self.senha}' WHERE id = {self.id}"
            else:
                sql = f"UPDATE Administrador SET usuario = '{self.usuario}', matricula = '{self.matricula}', email_institucional = '{self.email_institucional}' WHERE id = {self.id}"
            result = self.update(sql)
            if result:
                print("Administrador atualizado com sucesso!")
                return True
            else:
                print("Erro ao atualizar administrador.")
                return False
        else:
            print("Já existe outro administrador com esta matrícula ou email.")
            return False

    def deletar(self):
        sql = f"DELETE FROM Administrador WHERE id = {self.id}"
        result = self.delete(sql)
        if result:
            print("Administrador deletado com sucesso!")
            return True
        else:
            print("Erro ao deletar administrador.")
            return False

    def ver(self, id):
        sql = f"SELECT * FROM Administrador WHERE id = {id}"
        result = self.get(sql)
        if result:
            return result
        
    @classmethod
    def listar(cls):
        sql = f"SELECT id, usuario, matricula, email_institucional FROM Administrador"
        result = Model().get(sql)
        if result:
            return result
        return []