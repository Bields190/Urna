import sys
import os
import sqlite3

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))

import m_administrador # type: ignore

class Control:
    def __init__(self, tela):
        self.tela = tela
        self.conexao = sqlite3.connect('banco.db')
        self.cursor = self.conexao.cursor()
        self.criar_tabela()

    def criar_tabela(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS administradores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                matricula TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL
            )
        """)
        self.conexao.commit()

    def adicionar_administrador(self, nome, matricula, email, senha):
        try:
            self.cursor.execute("""
                INSERT INTO administradores (nome, matricula, email, senha)
                VALUES (?, ?, ?, ?)
            """, (nome, matricula, email, senha))
            self.conexao.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Erro ao adicionar administrador: {e}")
            return False

    def listar_administradores(self):
        self.cursor.execute("SELECT id, nome, matricula, email FROM administradores")
        return self.cursor.fetchall()

    def atualizar_administrador(self, id, nome, matricula, email, senha=None):
        try:
            if senha:
                self.cursor.execute("""
                    UPDATE administradores 
                    SET nome = ?, matricula = ?, email = ?, senha = ?
                    WHERE id = ?
                """, (nome, matricula, email, senha, id))
            else:
                self.cursor.execute("""
                    UPDATE administradores 
                    SET nome = ?, matricula = ?, email = ?
                    WHERE id = ?
                """, (nome, matricula, email, id))
            self.conexao.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Erro ao atualizar administrador: {e}")
            return False

    def deletar_administrador(self, id):
        try:
            self.cursor.execute("DELETE FROM administradores WHERE id = ?", (id,))
            self.conexao.commit()
            return True
        except Exception as e:
            print(f"Erro ao deletar administrador: {e}")
            return False

    def login(self):
        usuario = str(self.tela.entry1.get())
        senha = str(self.tela.entry2.get())
        admin = m_administrador.Admin(usuario, senha)
        if admin.verificar():
            return True
        else:
            return False
