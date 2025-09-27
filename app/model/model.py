from sqlite3 import Error
import sys
import os

# adiciona a pasta 'conexao' no caminho do Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'conexao'))

import conexao

class Model:
    def __init__(self):
        self.con = conexao.Conexao()

    def get(self, sql):
        try:
            con = self.con.get_conexao()
            cursor = con.cursor()
            result = cursor.execute(sql).fetchall()
            con.close()
            return result
        except Error as er:
            print(er)
            return False

    def insert(self, sql):
        try:
            con = self.con.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            if cursor.rowcount == 1: #Quantidade de linhas afetadas
                con.commit()
            con.close()
            return True
        except Error as er:
            print(er)
            return False

    def delete(self, sql):
        try:
            con = self.con.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            if cursor.rowcount == 1:
                con.commit()
            con.close()
            return cursor.rowcount
        except Error as er:
            print(er)
            return False

    def update(self, sql):
        try:
            con = self.con.get_conexao()
            cursor = con.cursor()
            cursor.execute(sql)
            if cursor.rowcount == 1:
                con.commit()
            con.close()
            return True
        except Error as er:
            print(er)
            return False