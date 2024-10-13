import unittest
import sqlite3
import sys, os
import uuid

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
        Set up method to initialize the test environment.
        Creates an in-memory SQLite database connection and the 'reviews' table before each test.
        """
        # Connect to a temporary in-memory SQLite database
        self.connection = sqlite3.connect(":memory:")
        
        # Create the 'reviews' table in the in-memory database
        self.connection.execute("""
            CREATE TABLE reviews (
                id TEXT PRIMARY KEY,
                date TEXT,
                comment TEXT,
                rating INTEGER,
                user_id TEXT,
                recipient_id TEXT
            )
        """)

        # Example review for testing
        self.review = Review(user_id=101, recipient_id=202, rating=4, comment="Good product!")
    

    def tearDown(self):
        """
        Tear down method to clean up after each test.
        Closes the SQLite connection after each test.
        """
        self.connection.close()
    

    def test_review_creation(self):
        """
        Test the creation of a Review instance.
        Checks whether the attributes are correctly assigned.
        """
        self.assertIsNotNone(self.review.id)  # The id should be automatically created with uuid
        self.assertEqual(self.review.user_id, 101)
        self.assertEqual(self.review.recipient_id, 202)
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.comment, "Good product!")
        self.assertIsNotNone(self.review.date)  # The date should be automatically generated
    

    def test_validate_rating(self):
        """
        Test the rating validation function.
        Ensure it accepts valid ratings between 0 and 5 and rejects invalid ratings.
        """
        valid_review = Review(user_id=102, recipient_id=203, rating=5)
        self.assertEqual(valid_review.validate_rating(5), 5)  # Valid rating

        # Test for invalid ratings
        with self.assertRaises(ValueError):
            Review(user_id=103, recipient_id=204, rating=6)  # Invalid rating (above 5)
        
        with self.assertRaises(ValueError):
            Review(user_id=103, recipient_id=204, rating=-1)  # Invalid rating (below 0)


    def test_validate_comment(self):
        """
        Test the comment validation function.
        Ensure it accepts valid comments and rejects comments exceeding the character limit.
        """
        # Test for a valid comment
        valid_review = Review(user_id=102, recipient_id=203, rating=4, comment="This is a valid comment.")
        self.assertEqual(valid_review.validate_comment("This is a valid comment."), "This is a valid comment.")
        
        # Test for a comment that exceeds the maximum allowed length
        long_comment = "A" * 251  # 251 characters
        with self.assertRaises(ValueError):
            Review(user_id=102, recipient_id=203, rating=4, comment=long_comment)
    

    def test_save_to_db(self):
        """
        Test if a review can be saved correctly in the SQLite database.
        """
        self.review.save_to_db(self.connection)
        
        # Retrieve the review from the database
        cursor = self.connection.execute("SELECT * FROM reviews WHERE id = ?", (str(self.review.id),))
        result = cursor.fetchone()
        
        self.assertIsNotNone(result)            # There should be a result
        self.assertEqual(result[3], 4)          # The 'rating' field should be 4
        self.assertEqual(result[4], str(101))   # The 'user_id' field should be 101
        self.assertEqual(result[5], str(202))   # The 'recipient_id' field should be 202
    

    def test_save_invalid_review_to_db(self):
        """
        Test that an invalid review (with invalid rating or comment) cannot be saved to the database.
        """
        with self.assertRaises(ValueError):
            invalid_review = Review(user_id=102, recipient_id=203, rating=6, comment="Invalid rating")
            invalid_review.save_to_db(self.connection)

        long_comment_review = Review(user_id=102, recipient_id=203, rating=4, comment="A" * 251)
        with self.assertRaises(ValueError):
            long_comment_review.save_to_db(self.connection)
    

    def test_str_method(self):
        """
        Test the __str__ method.
        Ensure that the string representation of the review is correct.
        """
        expected_str = "Review by User 101 for 202: 4/5 - Good product!"
        self.assertEqual(str(self.review), expected_str)


    def test_empty_comment(self):
        """
        Test the scenario where the comment is None.
        Ensure that it handles optional comments.
        """
        review_no_comment = Review(user_id=101, recipient_id=202, rating=4)
        self.assertEqual(review_no_comment.comment, None)
    

    def test_empty_rating(self):
        """
        Test to check if an empty or None rating raises an exception.
        """
        with self.assertRaises(ValueError):
            Review(user_id=102, recipient_id=203, rating=None)
    

    def test_max_rating_boundary(self):
        """
        Test the boundary case where the rating is exactly 5.
        """
        review_max_rating = Review(user_id=101, recipient_id=202, rating=5, comment="Supimpa!")
        self.assertEqual(review_max_rating.rating, 5)
    

    def test_min_rating_boundary(self):
        """
        Test the boundary case where the rating is exactly 0.
        """
        review_min_rating = Review(user_id=101, recipient_id=202, rating=0, comment="Era melhor ter ido assitir ao filme do Pelé.")
        self.assertEqual(review_min_rating.rating, 0)


# Executar os teste
if __name__ == "__main__":
    unittest.main()

