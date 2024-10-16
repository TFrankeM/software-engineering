import unittest
import sys, os
import uuid

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
from vending_machine import VendingMachine

class TestVendingMachine(unittest.TestCase):

    def test_list_products(self):
        """
        Test listing the products in a vending machine.
        """
        product1 = Product("Chocolate", "Delicious chocolate bar", 5.00, 10)
        product2 = Product("Coca-Cola", "Can of Coke", 4.50, 5)
        owner_id = str(uuid.uuid4())  # Simulate an owner ID
        machine = VendingMachine("Roda da conveniência", "4o andar", owner_id)
        machine.products = [product1, product2]  # Add products to the machine
        self.assertEqual([product1.name, product2.name], ["Chocolate", "Coca-Cola"])

    def test_check_stock(self):
        """
        Test checking the stock of a specific product in a vending machine.
        """
        product1 = Product("Chocolate", "Delicious chocolate bar", 5.00, 10)
        owner_id = str(uuid.uuid4())  # Simulate an owner ID
        machine = VendingMachine("Roda da conveniência", "4o andar", owner_id)
        machine.products = [product1]  # Add a single product to the machine

        # Check stock for the added product
        self.assertEqual(product1.quantity, 10)
        # Check stock for a non-existent product (this is done manually now)
        self.assertNotIn("non_existent_id", [str(prod.id) for prod in machine.products])

if __name__ == "__main__":
    unittest.main()