import unittest
import sys, os
import uuid

# Corrigir caminhos
# adding src to the system path
"""
    os.path.dirname(__file__): diretório do arquivo atual (A)
    os.path.join(A, "../../src/classes"): combina o diretório atual com o caminho relativo "../../src/classes" (B)
    os.path.abspath(B): converte o caminho relativo "../../src/classes" em um caminho absoluto (C)
    sys.path.insert(0, C): insere o caminho absoluto da pasta src no início da lista sys.path (uma lista de diretórios que o Python procura quando importa um módulo) 
"""
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from product import Product
from review import Review


class TestProduct(unittest.TestCase):

    def test_create_product(self):
        """
            Test creating a new product instance.
        """
        machine_id = uuid.uuid4()
        product = Product(name="Chips", description="A bag of chips", price=4.99, quantity=100, machine_id=str(machine_id))
        self.assertEqual(product.name, "Chips")
        self.assertEqual(product.description, "A bag of chips")
        self.assertEqual(product.price, 4.99)
        self.assertEqual(product.quantity, 100)
        self.assertEqual(product.machine_id, str(machine_id))
        self.assertEqual(len(product.reviews), 0)  # No reviews yet


    def test_add_review(self):
        """
            Test adding a review to the product.
        """
        machine_id = uuid.uuid4()
        product = Product(name="Soda", description="A can of soda", price=1.5, machine_id=str(machine_id))
        review = Review(user_id=101, product_id=product.id, rating=5, comment="Great soda!")
        product.add_review(review)

        self.assertEqual(len(product.reviews), 1)
        self.assertEqual(product.reviews[0].rating, 5)
        self.assertEqual(product.reviews[0].comment, "Great soda!")


    def test_apply_discount(self):
        """
        Test applying a discount to the product"s price.
        """
        machine_id = uuid.uuid4()  # Simulate a machine ID
        product = Product(name="Water", description="A bottle of water", price=2.0, machine_id=str(machine_id))
        product.apply_discount(25)              # Apply a 25% discount

        self.assertEqual(product.price, 1.5)    # 25% discount on $2.00


    def test_invalid_review(self):
        """
        Test that adding an invalid review raises an error.
        """
        machine_id = uuid.uuid4()  # Simulate a machine ID
        product = Product(name="Juice", description="A bottle of juice", price=3.0, machine_id=str(machine_id))
        with self.assertRaises(ValueError):
            product.add_review("This is not a review")  # Should raise ValueError


    def test_invalid_discount(self):
        """
            Test that applying an invalid discount raises an error.
        """
        machine_id = uuid.uuid4()  # Simulate a machine ID
        product = Product(name="Juice", description="A bottle of juice", price=3.0, machine_id=str(machine_id))
        with self.assertRaises(ValueError):
            product.apply_discount(120)  # Discount can"t be more than 100%


if __name__ == "__main__":
    unittest.main()

