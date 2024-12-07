from datetime import datetime
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
from review import Review, ProductReview, MachineReview, ReviewFactory


class TestReview(unittest.TestCase):
    MAX_COMMENT_LENGTH = 250

    def setUp(self):
        """
        Set up method to initialize the test environment.
        """
        # Example review for testing (with product_id)
        self.review = ProductReview(user_id=101, product_id="product_1", rating=4, comment="Good product!")
    
    def test_review_creation_with_product(self):
        """
        Test the creation of a ProductReview instance for a product.
        Checks whether the attributes are correctly assigned.
        """
        self.assertIsNotNone(self.review.id)  # The id should be automatically created with uuid
        self.assertEqual(self.review.user_id, 101)
        self.assertEqual(self.review.product_id, "product_1")
        self.assertIsNone(self.review.machine_id)  # machine_id should be None
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, "Good product!")
        self.assertIsNotNone(self.review.date)  # The date should be automatically generated

    def test_review_creation_with_machine(self):
        """
        Test the creation of a MachineReview instance for a vending machine.
        """
        review = MachineReview(user_id=101, machine_id="machine_1", rating=5, comment="Good machine!")
        self.assertIsNotNone(review.id)
        self.assertEqual(review.user_id, 101)
        self.assertEqual(review.machine_id, "machine_1")
        self.assertIsNone(review.product_id)  # product_id should be None
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Good machine!")
        self.assertIsNotNone(review.date)

    def test_both_ids_provided(self):
        """
        Test that providing both product_id and machine_id raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Review(user_id=101, product_id="product_1", machine_id="machine_1", rating=4)

    def test_no_ids_provided(self):
        """
        Test that providing neither product_id nor machine_id raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Review(user_id=101, rating=4)

    def test_validate_rating(self):
        """
        Test the rating validation function.
        Ensure it accepts valid ratings between 0 and 5 and rejects invalid ratings.
        """
        valid_review = ProductReview(user_id=102, product_id="product_1", rating=5)
        self.assertEqual(valid_review.validate_rating(5), 5)  # Valid rating

        # Test for invalid ratings
        with self.assertRaises(ValueError):
            ProductReview(user_id=103, product_id="product_1", rating=6)  # Invalid rating (above 5)
        
        with self.assertRaises(ValueError):
            ProductReview(user_id=103, product_id="product_1", rating=-1)  # Invalid rating (below 0)

    def test_validate_comment(self):
        """
        Test the comment validation function.
        Ensure it accepts valid comments and rejects comments exceeding the character limit.
        """
        # Test for a valid comment
        valid_review = ProductReview(user_id=102, product_id="product_1", rating=4, comment="This is a valid comment.")
        self.assertEqual(valid_review.validate_comment("This is a valid comment."), "This is a valid comment.")
        
        # Test for a comment that exceeds the maximum allowed length
        long_comment = "A" * 251  # 251 characters
        with self.assertRaises(ValueError):
            ProductReview(user_id=102, product_id="product_1", rating=4, comment=long_comment)

    def test_str_method(self):
        """
        Test the __str__ method.
        Ensure that the string representation of the review is correct.
        """
        expected_str = "Review by User 101 for Product product_1: 4/5 - Good product!"
        self.assertEqual(str(self.review), expected_str)

        review_machine = MachineReview(user_id=101, machine_id="machine_1", rating=5, comment="Good machine!")
        expected_str_machine = "Review by User 101 for Machine machine_1: 5/5 - Good machine!"
        self.assertEqual(str(review_machine), expected_str_machine)

    def test_empty_comment(self):
        """
        Test the scenario where the comment is None.
        Ensure that it handles optional comments.
        """
        review_no_comment = ProductReview(user_id=101, product_id="product_1", rating=4)
        self.assertEqual(review_no_comment.comment, None)

    def test_empty_rating(self):
        """
        Test to check if an empty or None rating raises an exception.
        """
        with self.assertRaises(ValueError):
            ProductReview(user_id=102, product_id="product_1", rating=None)

    def test_max_rating_boundary(self):
        """
        Test the boundary case where the rating is exactly 5.
        """
        review_max_rating = ProductReview(user_id=101, product_id="product_1", rating=5, comment="Supimpa!")
        self.assertEqual(review_max_rating.rating, 5)

    def test_min_rating_boundary(self):
        """
        Test the boundary case where the rating is exactly 0.
        """
        review_min_rating = ProductReview(user_id=101, product_id="product_1", rating=0, comment="It would have been better to go and watch the Pelé film.")
        self.assertEqual(review_min_rating.rating, 0)

    def test_factory_product_review_creation(self):
        """
        Test the creation of a product review using the factory.
        """
        review = ReviewFactory.create_review('product', user_id=101, rating=4, comment="Good product!", product_id="product_1")
        self.assertIsInstance(review, ProductReview)
        self.assertEqual(review.user_id, 101)
        self.assertEqual(review.rating, 4)
        self.assertEqual(review.comment, "Good product!")
        self.assertEqual(review.product_id, "product_1")
        self.assertIsNone(review.machine_id)

    def test_factory_machine_review_creation(self):
        """
        Test the creation of a machine review using the factory.
        """
        review = ReviewFactory.create_review('machine', user_id=101, rating=5, comment="Good machine!", machine_id="machine_1")
        self.assertIsInstance(review, MachineReview)
        self.assertEqual(review.user_id, 101)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Good machine!")
        self.assertEqual(review.machine_id, "machine_1")
        self.assertIsNone(review.product_id)


if __name__ == "__main__":
    unittest.main()
