import sqlite3
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from transaction import Transaction


class TransactionDAO:
    """
    Data Access Object (DAO) for managing transactions in the database.
    """

    def __init__(self, db_connection):
        """
        Initialize the TransactionDAO with a database connection.

        Parameters:
            db_connection (sqlite3.Connection): A connection object to the SQLite database.
        """
        self.connection = db_connection

    def create_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    seller_id TEXT NOT NULL,
                    vending_machine_id TEXT NOT NULL,
                    total_amount REAL NOT NULL,
                    transaction_date TEXT NOT NULL,
                );
            """)
            self.connection.commit()
            print("Tabela criada com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao criar a tabela: {e}")

    def insert_transaction(self, transaction):
        """
        Insert a transaction into the database.

        Parameters:
            transaction (Transaction): A Transaction object to be inserted into the database.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO transactions (id, user_id, seller_id, vending_machine_id, total_amount, transaction_date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(transaction.id), transaction.user_id, transaction.seller_id, transaction.vending_machine_id, transaction.total_amount, transaction.transaction_date))
        self.connection.commit()
        
        # Obter o ID da transação recém-criada
        return str(transaction.id)