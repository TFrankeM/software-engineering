import sqlite3
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from review import Review

class ReviewDAO:
    """
        Data Access Object (DAO) for managing reviews in the database.
    """

    def __init__(self, db_connection):
        """
            Initialize the ReviewDAO with a database connection.

        Parameters:
            db_connection (sqlite3.Connection): A connection object to the SQLite database.
        """
        self.connection = db_connection


    def create_table(self):
        """
            Create the reviews table in the database if it doesn't already exist.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id TEXT PRIMARY KEY,
                user_id INTEGER NOT NULL,
                product_id TEXT,
                machine_id TEXT,
                rating INTEGER NOT NULL,
                comment TEXT,
                date TEXT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (machine_id) REFERENCES vending_machines(id)
            );
        ''')
        self.connection.commit()


    def insert_review(self, review):
        """
            Insert a review into the database.

        Parameters:
            review (Review): A Review object to be inserted into the database.
        """
        cursor = self.connection.cursor()
        cursor.execute('''
            INSERT INTO reviews (id, user_id, product_id, machine_id, rating, comment, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(review.id), review.user_id, review.product_id, review.machine_id, review.rating, review.comment, review.date))
        self.connection.commit()


    def get_reviews_for_product(self, product_id):
        """
            Retrieve all reviews for a given product.

        Parameters:
            product_id (str): The UUID of the product to get reviews for.

        Returns:
            list: A list of Review objects.
        """
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM reviews WHERE product_id = ?', (product_id,))
        reviews_data = cursor.fetchall()

        reviews = []
        for row in reviews_data:
            review = Review(
                user_id=row[1],
                product_id=row[2],
                rating=row[4],
                comment=row[5]
            )
            review.id = row[0]      # ID stored in the DB
            review.machine_id = None
            review.date = row[6]    # Date stored in the DB
            reviews.append(review)
        return reviews


    def get_reviews_for_machine(self, machine_id):
            """
                Retrieve all reviews for a given vending machine.

            Parameters:
                machine_id (str): The ID of the vending machine to get reviews for.

            Returns:
                list: A list of Review objects.
            """
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM reviews WHERE machine_id = ?', (machine_id,))
            reviews_data = cursor.fetchall()

            reviews = []
            for row in reviews_data:
                review = Review(
                    user_id=row[1],
                    machine_id=row[3],
                    rating=row[4],
                    comment=row[5]
                )
                review.id = row[0]  # ID stored in the DB
                review.product_id = None
                review.date = row[6]  # Date stored in the DB
                reviews.append(review)
            return reviews


    def calculate_average_rating_for_product(self, product_id):
        """
        Calculate the average rating for a given product.

        Parameters:
            product_id (str): The UUID of the product to calculate the average rating for.

        Returns:
            float: The average rating of the product.
        """
        cursor = self.connection.cursor()
        cursor.execute('SELECT AVG(rating) FROM reviews WHERE product_id = ?', (product_id,))
        avg_rating = cursor.fetchone()[0]

        # Se não houver avaliações, retornar 0
        return avg_rating if avg_rating is not None else 0.0


    def calculate_average_rating_for_machine(self, machine_id):
        """
        Calculate the average rating for a given vending machine.

        Parameters:
            machine_id (str): The ID of the vending machine to calculate the average rating for.

        Returns:
            float: The average rating of the vending machine.
        """
        cursor = self.connection.cursor()
        cursor.execute('SELECT AVG(rating) FROM reviews WHERE machine_id = ?', (machine_id,))
        avg_rating = cursor.fetchone()[0]

        # Se não houver avaliações, retornar 0
        return avg_rating if avg_rating is not None else 0.0
    

    def delete_review(self, review_id):
        """
            Delete a review from the database by its UUID.

        Parameters:
            review_id (str): The UUID of the review to be deleted.
        """
        cursor = self.connection.cursor()
        cursor.execute('DELETE FROM reviews WHERE id = ?', (review_id,))
        self.connection.commit()

