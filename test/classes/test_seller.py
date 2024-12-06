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
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from seller import Seller


class TestSeller(unittest.TestCase):

    def setUp(self):
        """Set up a Seller instance for testing."""
        self.seller = Seller(
            name="Alice Seller",
            email="alice.seller@example.com",
            address="456 Seller St",
            password="sellerpassword123",
            anonymous_profile=True
        )

    def test_initialization(self):
        """Test that the seller is initialized correctly."""
        self.assertEqual(self.seller.name, "Alice Seller")
        self.assertEqual(self.seller.email, "alice.seller@example.com")
        self.assertEqual(self.seller.address, "456 Seller St")
        self.assertTrue(self.seller.verify_password("sellerpassword123"))
        self.assertTrue(self.seller.anonymous_profile)
        self.assertEqual(self.seller.get_products(), [])
        self.assertEqual(self.seller.get_orders(), [])

    def test_add_product(self):
        """Test that a product can be added to the seller's product list."""
        product = {"name": "Product A", "price": 10.99}
        self.seller.add_product(product)
        self.assertIn(product, self.seller.get_products())

    def test_add_order(self):
        """Test that an order can be added to the seller's order list."""
        order = {"order_id": 1, "product": "Product A", "quantity": 2}
        self.seller.add_order(order)
        self.assertIn(order, self.seller.get_orders())

    def test_get_products(self):
        """Test the retrieval of products."""
        product1 = {"name": "Product A", "price": 10.99}
        product2 = {"name": "Product B", "price": 15.49}
        self.seller.add_product(product1)
        self.seller.add_product(product2)
        self.assertEqual(self.seller.get_products(), [product1, product2])

    def test_get_orders(self):
        """Test the retrieval of orders."""
        order1 = {"order_id": 1, "product": "Product A", "quantity": 2}
        order2 = {"order_id": 2, "product": "Product B", "quantity": 1}
        self.seller.add_order(order1)
        self.seller.add_order(order2)
        self.assertEqual(self.seller.get_orders(), [order1, order2])

if __name__ == '__main__':
    unittest.main()