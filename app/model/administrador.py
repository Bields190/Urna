from model import Model

class Admin(Model):
    def __init__(self, usuario, senha, id=None):
        super().__init__()  # CONSTRUTOR
        self.id = id
        self.usuario = usuario
        self.senha = senha


    def verificar(self):
        sql = f"SELECT * FROM administrador WHERE usuario = '{self.usuario}' AND senha = '{self.senha}'"
        result = self.get(sql)
        if result:
            print("Usuário Encontrado e Logado com sucesso!")
            return True
        else:
            print("Usuário ou Senha incorretos!")
            return False
        
u1 = Admin('limeira', 'tesi25')

u1.verificar()