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
from product import Product
from vending_machine import Vending_Machine

class TestVendingMachine(unittest.TestCase):
    
    def test_list_products(self):
        product1 = Product("Chocolate", "p0001", 5.00, 10)
        product2 = Product("Coca-Cola", "p0002", 4.50, 5)
        machine = Vending_Machine("Roda da conveniência", "4o andar", "vm0001")
        machine.products["p0001"] = product1
        machine.products["p0003"] = product2
        self.assertEqual(machine.list_products(), ["Chocolate", "Coca-Cola"])

    def test_check_stock(self):
        product1 = Product("Chocolate", "p0001", 5.00, 10)
        machine = Vending_Machine("Roda da conveniência", "4o andar", "vm0001")
        machine.products["p0001"] = product1
        self.assertEqual(machine.check_stock("p0001"), 10)
        self.assertEqual(machine.check_stock("p0002"), 0)

if __name__ == "__main__":
    unittest.main()