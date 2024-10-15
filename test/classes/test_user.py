from datetime import datetime
import unittest
import sys, os

# Corrigir caminhos
# adding src to the system path
"""
    os.path.dirname(__file__): diretório do arquivo atual (A)
    os.path.join(A, '../../src/classes'): combina o diretório atual com o caminho relativo '../../src/classes' (B)
    os.path.abspath(B): converte o caminho relativo '../../src/classes' em um caminho absoluto (C)
    sys.path.insert(0, C): insere o caminho absoluto da pasta src no início da lista sys.path (uma lista de diretórios que o Python procura quando importa um módulo) 
"""
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from user import User


# implemente aqui a lógica de testes para a classe usuário