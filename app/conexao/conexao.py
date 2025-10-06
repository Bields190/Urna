import sqlite3
from sqlite3 import Error
import sys
import os

def resource_path(relative_path):
    """Obtém o caminho absoluto para recursos, funciona tanto em desenvolvimento quanto em executável"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class Conexao:
    def get_conexao(self):
        caminho = resource_path('db')
        try:
            con = sqlite3.connect(caminho)
            return con
        except Error as er:
            print(er)