import unittest
import sys, os
import sqlite3

# Adjust sys.path to point to the "classes" directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))

# Adjust sys.path to point to the "database" directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/database")))

from review import Review
from review_dao import ReviewDAO

class TestReviewDAO(unittest.TestCase):

    def setUp(self):
        """
            Set up method to initialize the test environment.
            Creates an in-memory SQLite database and the ReviewDAO instance before each test.
        """
        # Connect to an in-memory SQLite database for testing purposes
        self.connection = sqlite3.connect(":memory:")
        
        # Initialize the DAO with the in-memory connection
        self.review_dao = ReviewDAO(self.connection)
        
        # Create the "reviews" table
        self.review_dao.create_table()


    def tearDown(self):
        """
            Tear down method to clean up after each test.
            Closes the SQLite connection after each test.
        """
        self.connection.close()


    def test_insert_review_for_product(self):
        """
            Test inserting a review for a product into the database.
            Ensure that it is inserted and can be retrieved.
        """
        # Create a review for a product
        review = Review(user_id=1, product_id="product_123", rating=5, comment="Excellent product!")
        self.review_dao.insert_review(review)

        # Retrieve reviews for the product
        product_reviews = self.review_dao.get_reviews_for_product("product_123")

        # Verify the inserted review is retrieved correctly
        self.assertEqual(len(product_reviews), 1)
        self.assertEqual(product_reviews[0].user_id, 1)
        self.assertEqual(product_reviews[0].product_id, "product_123")
        self.assertEqual(product_reviews[0].rating, 5)
        self.assertEqual(product_reviews[0].comment, "Excellent product!")
    

    def test_insert_review_for_machine(self):
        """
            Test inserting a review for a vending machine into the database.
            Ensure that it is inserted and can be retrieved.
        """
        # Create a review for a vending machine
        review = Review(user_id=2, machine_id="machine_456", rating=4, comment="Good machine!")
        self.review_dao.insert_review(review)

        # Retrieve reviews for the machine
        machine_reviews = self.review_dao.get_reviews_for_machine("machine_456")

        # Verify the inserted review is retrieved correctly
        self.assertEqual(len(machine_reviews), 1)
        self.assertEqual(machine_reviews[0].user_id, 2)
        self.assertEqual(machine_reviews[0].machine_id, "machine_456")
        self.assertEqual(machine_reviews[0].rating, 4)
        self.assertEqual(machine_reviews[0].comment, "Good machine!")
    

    def test_insert_review_with_both_ids_raises_error(self):
        """
            Test that inserting a review with both product_id and machine_id raises a ValueError.
        """
        with self.assertRaises(ValueError):
            Review(user_id=1, product_id="product_123", machine_id="machine_456", rating=5)


    def test_get_reviews_for_non_existent_product(self):
        """
            Test retrieving reviews for a product that has no reviews.
            Ensure that an empty list is returned.
        """
        reviews = self.review_dao.get_reviews_for_product("non_existent_product")
        self.assertEqual(len(reviews), 0)  # No reviews should be returned


    def test_get_reviews_for_non_existent_machine(self):
        """
            Test retrieving reviews for a vending machine that has no reviews.
            Ensure that an empty list is returned.
        """
        reviews = self.review_dao.get_reviews_for_machine("non_existent_machine")
        self.assertEqual(len(reviews), 0)  # No reviews should be returned
    

    def test_delete_review(self):
        """
            Test deleting a review from the database.
            Ensure that the review is properly deleted.
        """
        # Insert a review for a product
        review = Review(user_id=1, product_id="product_123", rating=5, comment="Great product!")
        self.review_dao.insert_review(review)

        # Delete the review by its ID
        self.review_dao.delete_review(str(review.id))

        # Verify that no reviews exist for the product after deletion
        reviews = self.review_dao.get_reviews_for_product("product_123")
        self.assertEqual(len(reviews), 0)  # No reviews should be returned


    def test_insert_review_with_long_comment(self):
        """
            Test that inserting a review with a comment that exceeds the maximum allowed length raises a ValueError.
        """
        long_comment = "A" * 251  # Comment exceeds the 250 character limit
        with self.assertRaises(ValueError):
            Review(user_id=1, product_id="product_123", rating=5, comment=long_comment)


    def test_str_method_for_product_review(self):
        """
            Test the __str__ method for a review of a product.
            Ensure that the string representation of the review is correct.
        """
        review = Review(user_id=1, product_id="product_123", rating=5, comment="Amazing!")
        expected_str = "Review by User 1 for Product product_123: 5/5 - Amazing!"
        self.assertEqual(str(review), expected_str)


    def test_str_method_for_machine_review(self):
        """
            Test the __str__ method for a review of a vending machine.
            Ensure that the string representation of the review is correct.
        """
        review = Review(user_id=2, machine_id="machine_456", rating=4, comment="Great machine!")
        expected_str = "Review by User 2 for Machine machine_456: 4/5 - Great machine!"
        self.assertEqual(str(review), expected_str)


if __name__ == "__main__":
    unittest.main()
