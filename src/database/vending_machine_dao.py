import sqlite3
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from vending_machine import VendingMachine


class VendingMachineDAO:
    """
    Data Access Object (DAO) for managing vending machines in the database.
    """

    def __init__(self, db_connection):
        """
            Initialize the VendingMachineDAO with a database connection.

        Parameters:
            db_connection (sqlite3.Connection): A connection object to the SQLite database.
        """
        self.connection = db_connection


    def create_table(self):
        """
            Create the vending_machines table in the database if it doesn't already exist.
        """
        cursor = self.connection.cursor()
        
        # Create the vending machines table with a reference to the owner (seller)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS vending_machines (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                location TEXT NOT NULL,
                owner_id TEXT NOT NULL,                       -- Owner (Seller) ID as Foreign Key
                FOREIGN KEY (owner_id) REFERENCES usuarios(id) ON DELETE CASCADE
            );
        ''')
        
        self.connection.commit()


    def insert_vending_machine(self, vending_machine):
        """
            Insert a vending machine into the database.

        Parameters:
            vending_machine (VendingMachine): A VendingMachine object to be inserted into the database.
        """
        cursor = self.connection.cursor()
        
        # Insert vending machine details, including the owner_id
        cursor.execute('''
            INSERT INTO vending_machines (id, name, location, owner_id)
            VALUES (?, ?, ?, ?)
        ''', (str(vending_machine.id), vending_machine.name, vending_machine.location, vending_machine.owner_id))
        
        self.connection.commit()


    def get_vending_machine_by_id(self, vending_machine_id):
        """
            Retrieve a vending machine from the database by its ID.

        Parameters:
            vending_machine_id (str): The ID of the vending machine to retrieve.

        Returns:
            VendingMachine: A VendingMachine object with its associated details.
        """
        cursor = self.connection.cursor()
        
        # Fetch the vending machine details
        cursor.execute('''
            SELECT * FROM vending_machines WHERE id = ?
        ''', (vending_machine_id,))
        vending_machine_data = cursor.fetchone()
        
        if vending_machine_data is None:
            return None

        # Create and return the VendingMachine object
        vending_machine = VendingMachine(
            name=vending_machine_data[1],
            location=vending_machine_data[2],
            owner_id=vending_machine_data[3]  # Adding the owner ID
        )
        vending_machine.id = vending_machine_data[0]
        return vending_machine


    def delete_vending_machine(self, vending_machine_id):
        """
            Delete a vending machine from the database by its ID.

        Parameters:
            vending_machine_id (str): The ID of the vending machine to delete.
        """
        cursor = self.connection.cursor()
        
        # Delete the vending machine
        cursor.execute('DELETE FROM vending_machines WHERE id = ?', (vending_machine_id,))
        
        self.connection.commit()
