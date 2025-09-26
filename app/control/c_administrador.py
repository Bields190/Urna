import tkinter as tk
from tkinter import messagebox

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'model'))

import m_administrador

class Control:
    def __init__(self, tela):
        self.tela = tela
        self.tela.btn_entrar.config(command=self.login)

    def login(self, usu, sen):
        admin = m_administrador.Admin(usu, sen)
        if admin.verificar():
            return True
        else:
            return False
