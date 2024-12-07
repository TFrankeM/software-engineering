import sqlite3
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from item_transaction import ItemTransaction


class ItemTransactionDAO:
    """
    Data Access Object (DAO) for managing items within a transaction.
    """

    def __init__(self, db_connection):
        """
        Initialize the ItemTransactionDAO with a database connection.

        Parameters:
            db_connection (sqlite3.Connection): A connection object to the SQLite database.
        """
        self.connection = db_connection

    def create_table(self):
        """
        Create the item_transactions table in the database if it doesn't already exist.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS item_transactions (
                transaction_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                FOREIGN KEY (transaction_id) REFERENCES transactions(id),
                FOREIGN KEY (product_id) REFERENCES products(id),
                PRIMARY KEY (transaction_id, product_id)
            );
        """)
        self.connection.commit()

    def insert_item_transaction(self, item_transaction):
        """
        Insert an item transaction into the database.

        Parameters:
            item_transaction (ItemTransaction): An ItemTransaction object to be inserted into the database.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO item_transactions (transaction_id, product_id, quantity, price)
            VALUES (?, ?, ?, ?)
        """, (item_transaction.transaction_id, item_transaction.product_id, item_transaction.quantity, item_transaction.price))
        self.connection.commit()
