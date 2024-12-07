import sqlite3
import uuid
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from money_deposit import MoneyDeposit

class MoneyDepositDAO:
    """
    Data Access Object (DAO) for managing MoneyDeposit entities in the database.
    """

    def __init__(self, db_connection):
        """
        Initialize the MoneyDepositDAO with a database connection.

        Parameters:
            db_connection (sqlite3.Connection): A connection object to the SQLite database.
        """
        self.connection = db_connection

    def create_table(self):
        """
        Create the money_deposits table in the database if it doesn't already exist.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS money_deposits (
                id TEXT PRIMARY KEY,
                customer_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                deposit_method TEXT NOT NULL,
                timestamp TEXT NOT NULL
            );
        """)
        self.connection.commit()

    def insert_money_deposit(self, money_deposit):
        """
        Insert a MoneyDeposit entity into the database.

        Parameters:
            money_deposit (MoneyDeposit): A MoneyDeposit object to be inserted into the database.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO money_deposits (id, customer_id, amount, deposit_method, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (str(money_deposit.id), money_deposit.customer_id, money_deposit.amount, 
               money_deposit.deposit_method, money_deposit.timestamp))
        self.connection.commit()

    def get_all_deposits(self):
        """
        Retrieve all money deposits from the database.

        Returns:
            list: A list of tuples representing all money deposits.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM money_deposits")
        return cursor.fetchall()

    def find_deposit_by_id(self, deposit_id):
        """
        Find a money deposit by its UUID in the database.

        Parameters:
            deposit_id (str): The UUID of the deposit to be retrieved.

        Returns:
            tuple: A tuple representing the money deposit.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM money_deposits WHERE id = ?", (deposit_id,))
        return cursor.fetchone()

    def get_deposits_by_customer_id(self, customer_id):
        """
        Retrieve all deposits made by a specific customer.

        Parameters:
            customer_id (int): The ID of the customer.

        Returns:
            list: A list of MoneyDeposit objects.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM money_deposits WHERE customer_id = ?", (customer_id,))
        rows = cursor.fetchall()

        deposits = []
        for row in rows:
            deposit = MoneyDeposit(
                customer_id=row[1],
                amount=row[2],
                deposit_method=row[3]
            )
            deposit.id = row[0]
            deposit.timestamp = row[4]
            deposits.append(deposit)

        return deposits

    def delete_deposit(self, deposit_id):
        """
        Delete a money deposit from the database by its UUID.

        Parameters:
            deposit_id (str): The UUID of the deposit to be deleted.
        """
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM money_deposits WHERE id = ?", (deposit_id,))
        self.connection.commit()

    def update_deposit_amount(self, deposit_id, new_amount):
        """
        Update the amount of a specific money deposit.

        Parameters:
            deposit_id (str): The UUID of the deposit to be updated.
            new_amount (float): The new amount for the deposit.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            UPDATE money_deposits
            SET amount = ?
            WHERE id = ?
        """, (new_amount, deposit_id))
        self.connection.commit()
