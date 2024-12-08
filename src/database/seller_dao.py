import sys, os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from seller import Seller

class SellerDAO:
    """
    Data Access Object (DAO) for managing sellers in the database.
    """

    def __init__(self, db_connection):
        """
        Initialize the SellerDAO with a database connection.

        Parameters:
            db_connection (sqlite3.Connection): A connection object to the SQLite database.
        """
        self.connection = db_connection

    def create_table(self):
        """
        Create the sellers table in the database if it doesn't already exist.
        """
        cursor = self.connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sellers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                address TEXT,
                profile_picture_path TEXT,
                anonymous_profile BOOLEAN NOT NULL,
                coins NUMERIC
            );
        ''')

        self.connection.commit()

    def insert_seller(self, seller):
        """
        Insert a new seller into the database.

        Parameters:
            seller (Seller): The Seller object to be inserted.
        """
        cursor = self.connection.cursor()

        cursor.execute('''
            INSERT INTO sellers (id, name, email, password, address, profile_picture_path, anonymous_profile, coins)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (str(seller.user_id), seller.name, seller.email, seller._hash_password(seller.change_password),
              seller.address, seller.profile_picture_path, seller.anonymous_profile, seller.coins))

        self.connection.commit()

    def get_seller_by_id(self, seller_id):
        """
        Retrieve a seller from the database by their ID.

        Parameters:
            seller_id (str): The ID of the seller to retrieve.

        Returns:
            Seller: A Seller object with its associated details, or None if not found.
        """
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM sellers WHERE id = ?', (seller_id,))
        seller_data = cursor.fetchone()

        if seller_data is None:
            return None

        seller = Seller(seller_data[1], seller_data[2], seller_data[3], seller_data[4], seller_data[6])
        seller.change_profile_picture_path = seller_data[5]
        return seller

    def update_seller(self, seller):
        """
        Update the details of an existing seller in the database.

        Parameters:
            seller (Seller): The Seller object with updated details.
        """
        cursor = self.connection.cursor()

        cursor.execute('''
            UPDATE sellers
            SET name = ?, email = ?, password = ?, address = ?, profile_picture_path = ?, anonymous_profile = ?, coins = ?
            WHERE id = ?
        ''', (seller.name, seller.email, seller._hash_password(seller.change_password),
              seller.address, seller.profile_picture_path, seller.anonymous_profile, str(seller.user_id), seller.coins))

        self.connection.commit()

    def delete_seller(self, seller_id):
        """
        Delete a seller from the database by their ID.

        Parameters:
            seller_id (str): The ID of the seller to delete.
        """
        cursor = self.connection.cursor()

        cursor.execute('DELETE FROM sellers WHERE id = ?', (seller_id,))
        self.connection.commit()
    
    def add_balance(self, seller_id, amount):
        """
        Add balance to a customer's account.

        Parameters:
            seller_id (str): The ID of the seller.
            amount (float): The amount to be added to the customer's balance.

        Returns:
            bool: True if the balance was updated successfully, False otherwise.
        """
        cursor = self.connection.cursor()

        try:
            # Atualiza o saldo do cliente
            cursor.execute('''
                UPDATE sellers
                SET coins = COALESCE(coins, 0) + ?
                WHERE id = ?
            ''', (amount, seller_id))

            # Verifica se algum registro foi afetado
            if cursor.rowcount == 0:
                return False  # Cliente não encontrado

            self.connection.commit()
            return True
        except Exception as e:
            print(f"Erro ao adicionar saldo: {e}")
            self.connection.rollback()
            return False
