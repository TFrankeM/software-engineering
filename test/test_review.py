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
    
    def setUp(self):
        """
        Método de configuração inicial. Este método é executado antes de cada teste.
        Cria uma conexão com o banco de dados SQLite em memória e a tabela 'reviews'.
        """
        # Conectar a um banco de dados temporário em memória
        self.connection = sqlite3.connect(':memory:')
        
        # Criar a tabela 'reviews' no banco de dados em memória
        self.connection.execute("""
            CREATE TABLE reviews (
                id TEXT PRIMARY KEY,
                date TEXT,
                comment TEXT,
                rating INTEGER,
                user_id INTEGER,
                recipient_id INTEGER
            )
        """)

        # Exemplo de avaliação para uso nos testes
        self.review = Review(user_id=101, recipient_id=202, rating=4, comment="Good product!")
    
    def tearDown(self):
        """
        Método de finalização. Este método é executado após cada teste.
        Fecha a conexão com o banco de dados.
        """
        self.connection.close()
    
    def test_review_creation(self):
        """
        Testa se a criação de uma instância da classe Review ocorre corretamente.
        Verifica se os atributos são corretamente atribuídos.
        """
        self.assertIsNotNone(self.review.id)  # O id deve ser criado automaticamente com uuid
        self.assertEqual(self.review.user_id, 101)
        self.assertEqual(self.review.recipient_id, 202)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, "Good product!")
        self.assertIsNotNone(self.review.date)  # A data deve ser gerada automaticamente
    

    def test_validate_rating(self):
        """
        Testa a função de validação de nota (rating). Deve retornar True para notas entre 0 e 5.
        """
        valid_review = Review(user_id=102, recipient_id=203, rating=5)
        invalid_review = Review(user_id=103, recipient_id=204, rating=6)
        
        self.assertTrue(valid_review.validate_rating())  # Nota válida
        self.assertFalse(invalid_review.validate_rating())  # Nota inválida
    

    def test_save_to_db(self):
        """
        Testa se uma avaliação pode ser salva corretamente no banco de dados SQLite.
        """
        self.review.save_to_db(self.connection)
        
        # Recupera a avaliação do banco de dados
        cursor = self.connection.execute("SELECT * FROM reviews WHERE id = ?", (str(self.review.id),))
        result = cursor.fetchone()
        
        self.assertIsNotNone(result)  # Deve existir um resultado
        self.assertEqual(result[3], 4)  # O campo 'rating' deve ser 4
        self.assertEqual(result[4], 101)  # O campo 'user_id' deve ser 101
        self.assertEqual(result[5], 202)  # O campo 'recipient_id' deve ser 202
    

    def test_str_method(self):
        """
        Testa se o método __str__ retorna a string correta.
        """
        expected_str = "Review by User 101 for 202: 4/5 - Good product!"
        self.assertEqual(str(self.review), expected_str)


# Executar os testes
if __name__ == '__main__':
    unittest.main()
