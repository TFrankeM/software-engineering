import sqlite3
import uuid
import sys, os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from administrator import Administrator

class AdministratorDAO:
    """
    Data Access Object (DAO) for managing administrators in the database.
    """

    def __init__(self, db_connection):
        """
        Initialize the AdministratorDAO with a database connection.

        Parameters:
            db_connection (sqlite3.Connection): A connection object to the SQLite database.
        """
        self.connection = db_connection

    def create_table(self):
        """
        Create the administrators table in the database if it doesn't already exist.
        """
        cursor = self.connection.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS administrators (
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

    def insert_administrator(self, administrator):
        """
        Insert a new administrator into the database.

        Parameters:
            administrator (Administrator): The Administrator object to be inserted.
        """
        cursor = self.connection.cursor()

        cursor.execute('''
            INSERT INTO administrators (id, name, email, password, address, profile_picture_path, anonymous_profile)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (str(administrator.user_id), administrator.name, administrator.email, 
              administrator._hash_password(administrator.change_password), administrator.address,
              administrator.profile_picture_path, administrator.anonymous_profile))

        self.connection.commit()

    def get_administrator_by_id(self, administrator_id):
        """
        Retrieve an administrator from the database by their ID.

        Parameters:
            administrator_id (str): The ID of the administrator to retrieve.

        Returns:
            Administrator: An Administrator object with its associated details, or None if not found.
        """
        cursor = self.connection.cursor()

        cursor.execute('SELECT * FROM administrators WHERE id = ?', (administrator_id,))
        admin_data = cursor.fetchone()

        if admin_data is None:
            return None

        admin = Administrator(admin_data[1], admin_data[2], admin_data[3], admin_data[4], admin_data[6])
        admin.change_profile_picture_path = admin_data[5]
        return admin

    def update_administrator(self, administrator):
        """
        Update the details of an existing administrator in the database.

        Parameters:
            administrator (Administrator): The Administrator object with updated details.
        """
        cursor = self.connection.cursor()

        cursor.execute('''
            UPDATE administrators
            SET name = ?, email = ?, password = ?, address = ?, profile_picture_path = ?, anonymous_profile = ?
            WHERE id = ?
        ''', (administrator.name, administrator.email, administrator._hash_password(administrator.change_password),
              administrator.address, administrator.profile_picture_path, administrator.anonymous_profile,
              str(administrator.user_id)))

        self.connection.commit()

    def delete_administrator(self, administrator_id):
        """
        Delete an administrator from the database by their ID.

        Parameters:
            administrator_id (str): The ID of the administrator to delete.
        """
        cursor = self.connection.cursor()

        cursor.execute('DELETE FROM administrators WHERE id = ?', (administrator_id,))
        self.connection.commit()
