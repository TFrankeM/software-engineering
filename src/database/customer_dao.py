import sqlite3
import uuid
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from customer import Customer

class CustomerDAO:
    """
    Data Access Object (DAO) for managing customers in the database.
    """

    def __init__(self, db_connection):
        """
        Initialize the CustomerDAO with a database connection.

        Parameters:
            db_connection (sqlite3.Connection): A connection object to the SQLite database.
        """
        self.connection = db_connection

    def create_table(self):
        """
        Create the customers table in the database if it doesn't already exist.
        """
        cursor = self.connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                address TEXT,
                profile_picture_path TEXT,
                anonymous_profile BOOLEAN NOT NULL
            );
        ''')

        self.connection.commit()

    def insert_customer(self, customer):
        """
        Insert a new customer into the database.

        Parameters:
            customer (Customer): The Customer object to be inserted.
        """
        cursor = self.connection.cursor()

        cursor.execute('''
            INSERT INTO customers (id, name, email, password, address, profile_picture_path, anonymous_profile)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(customer.user_id), customer.name, customer.email, customer._hash_password(customer.change_password),
              customer.address, customer.profile_picture_path, customer.anonymous_profile))

        self.connection.commit()

    def get_customer_by_id(self, customer_id):
        """
        Retrieve a customer from the database by their ID.

        Parameters:
            customer_id (str): The ID of the customer to retrieve.

        Returns:
            Customer: A Customer object with its associated details, or None if not found.
        """
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        customer_data = cursor.fetchone()

        if customer_data is None:
            return None

        customer = Customer(customer_data[1], customer_data[2], customer_data[3], customer_data[4], customer_data[6])
        customer.change_profile_picture_path = customer_data[5]
        return customer

    def update_customer(self, customer):
        """
        Update the details of an existing customer in the database.

        Parameters:
            customer (Customer): The Customer object with updated details.
        """
        cursor = self.connection.cursor()

        cursor.execute('''
            UPDATE customers
            SET name = ?, email = ?, password = ?, address = ?, profile_picture_path = ?, anonymous_profile = ?
            WHERE id = ?
        ''', (customer.name, customer.email, customer._hash_password(customer.change_password),
              customer.address, customer.profile_picture_path, customer.anonymous_profile, str(customer.user_id)))

        self.connection.commit()

    def delete_customer(self, customer_id):
        """
        Delete a customer from the database by their ID.

        Parameters:
            customer_id (str): The ID of the customer to delete.
        """
        cursor = self.connection.cursor()

        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        self.connection.commit()