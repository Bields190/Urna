import sqlite3
from sqlite3 import Error
import sys
import os

def resource_path(relative_path):
    """Retorna o caminho absoluto para um recurso.

    - Quando empacotado com PyInstaller, usa sys._MEIPASS.
    - Em desenvolvimento, resolve a partir da raiz do projeto (duas pastas acima deste arquivo).
    """
    # Normalize o relative_path
    relative_path = relative_path.lstrip("/\\")

    base_path = getattr(sys, '_MEIPASS', None)
    if not base_path:
        # raiz do projeto (dois níveis acima de app/conexao)
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    return os.path.join(base_path, relative_path)

class Conexao:
    def get_conexao(self):
        caminho = resource_path('db.db')
        try:
            con = sqlite3.connect(caminho)
            return con
        except Error as er:
            print(er)