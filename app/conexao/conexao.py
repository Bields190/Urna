import sqlite3
from sqlite3 import Error
import sys
import os
import shutil

def get_persistent_db_path():
    """Obtém caminho persistente para o banco de dados"""
    if getattr(sys, 'frozen', False):
        # Executável: usar pasta do usuário
        app_data_dir = os.path.expanduser('~/.urna_eletronica')
        if not os.path.exists(app_data_dir):
            os.makedirs(app_data_dir)
        return os.path.join(app_data_dir, 'db.db')
    else:
        # Desenvolvimento: usar pasta do projeto
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        return os.path.join(base_path, 'db.db')

def resource_path(relative_path):
    """Obtém o caminho absoluto para recursos, funciona tanto em desenvolvimento quanto em executável"""
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # Em desenvolvimento, busca a partir da raiz do projeto
        base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    
    return os.path.join(base_path, relative_path)

def inicializar_banco_persistente():
    """Inicializa banco de dados persistente, copiando do executável se necessário"""
    if getattr(sys, 'frozen', False):
        # Executável: verificar se banco persistente existe
        db_persistente = get_persistent_db_path()
        
        if not os.path.exists(db_persistente):
            # Copiar banco inicial do executável
            db_template = resource_path('db.db')
            if os.path.exists(db_template):
                print(f"Inicializando banco persistente em: {db_persistente}")
                shutil.copy2(db_template, db_persistente)
            else:
                print("Aviso: Banco template não encontrado, criando novo")
        
        return db_persistente
    else:
        # Desenvolvimento: usar banco local
        return get_persistent_db_path()

class Conexao:
    def get_conexao(self):
        # Usar banco persistente em vez do temporário
        caminho = inicializar_banco_persistente()
        try:
            con = sqlite3.connect(caminho)
            print(f"Conectado ao banco: {caminho}")
            return con
        except Error as er:
            print(f"Erro ao conectar ao banco {caminho}: {er}")
            return None