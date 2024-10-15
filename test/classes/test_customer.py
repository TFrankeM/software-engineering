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
from customer import Customer

class TestCustomer(unittest.TestCase):

    def setUp(self):
        """
        Create a Customer instance to be used in the tests.
        """
        self.customer = Customer(
            name="John Doe", 
            email="john@example.com", 
            address="123 Main St", 
            password="securepassword123", 
            anonymous_profile=False
        )

    def test_initialization(self):
        """
        Test that the customer is initialized correctly.
        """
        self.assertEqual(self.customer.name, "John Doe")
        self.assertEqual(self.customer.email, "john@example.com")
        self.assertEqual(self.customer.address, "123 Main St")
        self.assertFalse(self.customer.anonymous_profile)
        self.assertEqual(self.customer.get_reviews(), [])
        self.assertEqual(self.customer.get_orders(), [])

    def test_add_review(self):
        """
        Test that a review can be added to the customer.
        """
        review = "Great product!"
        self.customer.add_review(review)
        self.assertIn(review, self.customer.get_reviews())
        self.assertEqual(len(self.customer.get_reviews()), 1)

    def test_add_multiple_reviews(self):
        """
        Test adding multiple reviews to the customer.
        """
        review1 = "Great product!"
        review2 = "Fast delivery!"
        self.customer.add_review(review1)
        self.customer.add_review(review2)
        self.assertIn(review1, self.customer.get_reviews())
        self.assertIn(review2, self.customer.get_reviews())
        self.assertEqual(len(self.customer.get_reviews()), 2)

    def test_add_order(self):
        """
        Test that an order can be added to the customer.
        """
        order = "Order #1234"
        self.customer.add_order(order)
        self.assertIn(order, self.customer.get_orders())
        self.assertEqual(len(self.customer.get_orders()), 1)

    def test_add_multiple_orders(self):
        """
        Test adding multiple orders to the customer.
        """
        order1 = "Order #1234"
        order2 = "Order #5678"
        self.customer.add_order(order1)
        self.customer.add_order(order2)
        self.assertIn(order1, self.customer.get_orders())
        self.assertIn(order2, self.customer.get_orders())
        self.assertEqual(len(self.customer.get_orders()), 2)

if __name__ == "__main__":
    unittest.main()