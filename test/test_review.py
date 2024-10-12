import unittest
import sqlite3
import sys, os

# Corrigir caminhos
# adding src to the system path
"""
    os.path.dirname(__file__): diretório do arquivo atual (A)
    os.path.join(A, '../src'): combina o diretório atual com o caminho relativo '../src' (B)
    os.path.abspath(B): converte o caminho relativo '../src' em um caminho absoluto (C)
    sys.path.insert(0, C): insere o caminho absoluto da pasta src no início da lista sys.path (uma lista de diretórios que o Python procura quando importa um módulo) 
"""
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from review import Review


class TestReview(unittest.TestCase):
    
    def test_review_creation(self):
        """
        Testa se a criação de uma instância da classe Review ocorre corretamente.
        Verifica se os atributos são corretamente atribuídos.
        """
        # Exemplo de avaliação para uso nos testes
        self.review = Review(user_id=101, recipient_id=202, rating=4, comment="Good product!")

        self.assertIsNotNone(self.review.id)  # O id deve ser criado automaticamente com uuid
        self.assertEqual(self.review.user_id, 101)
        self.assertEqual(self.review.recipient_id, 202)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, "Good product!")
        self.assertIsNotNone(self.review.date)  # A data deve ser gerada automaticamente



# Executar os testes
if __name__ == '__main__':
    unittest.main()
