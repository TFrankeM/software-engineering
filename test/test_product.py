import unittest
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
from product import Product

print("boi: ", os.path.join(os.path.dirname(__file__), "../src"))
class TestProduct(unittest.TestCase):

    def test_initial_attributes(self):
        product = Product("Chocolate", "p0001", 5.00, 10)
        self.assertEqual(product.name, "Chocolate")
        self.assertEqual(product.id, "p0001")
        self.assertEqual(product.price, 5.00)
        self.assertEqual(product.quantity, 10)

    def test_initial_attibutes(self):
        product = Product("Chocolate", "p0001", 5.00, 10)
        product.update_quantity(0)
        self.assertEqual(product.quantity, 15)
    
if __name__ == "__main__":
    unittest.main()