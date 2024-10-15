import sqlite3
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from product import Product

class ProductDAO:
    """
        Data Access Object (DAO) for managing Product entities in the database.
    """

    def __init__(self, db_connection):
        """
            Initialize the ProductDAO with a database connection.

        Parameters:
            db_connection (sqlite3.Connection): A connection object to the SQLite database.
        """
        self.connection = db_connection


    def create_table(self):
        """
            Create the product table in the database if it doesn"t already exist.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL
            );
        """)
        self.connection.commit()


    def insert_product(self, product):
        """
            Insert a product into the database.

        Parameters:
            product (Product): A Product object to be inserted into the database.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO products (id, name, description, price, quantity)
            VALUES (?, ?, ?, ?, ?)
        """, (str(product.id), product.name, product.description, product.price, product.quantity))
        self.connection.commit()


    def get_all_products(self):
        """
            Retrieve all products from the database.

        Returns:
            list: A list of tuples representing the products.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()


    def find_product_by_id(self, product_id):
        """
            Find a product by its UUID in the database.

        Parameters:
            product_id (str): The UUID of the product to be retrieved.

        Returns:
            tuple: A tuple representing the product.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        return cursor.fetchone()


    def update_product_quantity(self, product_id, new_quantity):
        """
            Update the quantity of a product.

        Parameters:
            product_id (str): The UUID of the product.
            new_quantity (int): The new quantity of the product.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE products
            SET quantity = ?
            WHERE id = ?
        """, (new_quantity, product_id))
        self.connection.commit()


    def delete_product(self, product_id):
        """
            Delete a product from the database by its UUID.

        Parameters:
            product_id (str): The UUID of the product to be deleted.
        """
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        self.connection.commit()

