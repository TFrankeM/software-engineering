import unittest
import sys, os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from favorite_product import FavoriteProduct  # Importe a classe favorita do produto

class TestFavoriteProduct(unittest.TestCase):
    def setUp(self):
        """
        Setup method to initialize the test environment.
        This method is called before each test case.
        """
        self.user_id = "user_123"
        self.product_id = "product_456"
        self.favorite_product = FavoriteProduct(self.user_id, self.product_id)

    def test_favorite_product_creation(self):
        """
        Test the creation of a FavoriteProduct instance.
        Checks whether the attributes are correctly assigned.
        """
        self.assertIsNotNone(self.favorite_product.id)
        self.assertEqual(self.favorite_product.user_id, self.user_id)
        self.assertEqual(self.favorite_product.product_id, self.product_id)

    def test_favorite_product_id_is_uuid(self):
        """
        Test that the id attribute is a valid UUID.
        """
        self.assertIsInstance(self.favorite_product.id, uuid.UUID)

    def test_favorite_product_repr(self):
        """
        Test the __repr__ method.
        Ensure that the string representation of the favorite product is correct.
        """
        expected_repr = f"<FavoriteProduct(id={self.favorite_product.id}, user_id={self.user_id}, product_id={self.product_id})>"
        self.assertEqual(repr(self.favorite_product), expected_repr)

if __name__ == "__main__":
    unittest.main()
    