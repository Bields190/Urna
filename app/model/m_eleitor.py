from model import Model

class Eleitor(Model):
    def __init__(self, matricula, nome, email=None):
        super().__init__()
        self.matricula = matricula
        self.nome = nome
        self.email = email


    def verificar(self):
        sql = f"SELECT * FROM eleitor WHERE matricula = '{self.matricula}' AND nome LIKE '{self.nome}%';"
        result = self.get(sql)
        if result:
            print("Usuário Encontrado e Logado com sucesso!")
            return True
        else:
            print("Usuário ou Senha incorretos!")
            return False

    def inserir(self):
        if self.get(f"SELECT * FROM eleitor WHERE matricula = '{self.matricula}';"):
            print("Matrícula já cadastrada!")
            return False
        else:
            sql = f"INSERT INTO eleitor(matricula, nome, email_institucional) VALUES ('{self.matricula}', '{self.nome}', '{self.email}');"
            print("Cadastrado com sucesso!")
            return self.insert(sql)
        

# TESTES
e1 = Eleitor('20170300016', 'Fernanda')
e1.verificar()


e2 = Eleitor('20170300099', 'Joao', 'joao@sou.ufac.br')
e2.inserir()
e2.verificar()