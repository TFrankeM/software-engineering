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
                average_rating REAL DEFAULT 0,
                FOREIGN KEY (owner_id) REFERENCES usuarios(id) ON DELETE CASCADE
            );
        ''')
        
        self.connection.commit()


    def get_all_vending_machines(self):
        """
        Retrieve all vending machines from the database.
        
        Returns:
            list: A list of VendingMachine objects representing the vending machines in the database.
        """
        cursor = self.connection.cursor()
        
        # Fetch all vending machines
        cursor.execute("SELECT id, name, location, owner_id, average_rating FROM vending_machines")
        rows = cursor.fetchall()

        vending_machines = []
        
        # Create VendingMachine objects for each row
        for row in rows:
            vending_machine = VendingMachine(name=row[1], location=row[2], owner_id=row[3], average_rating=row[4])
            vending_machine.id = row[0]  # Set the id from the database row
            vending_machines.append(vending_machine)

        return vending_machines


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


    def get_vending_machines_by_seller_id(self, seller_id):
        """
        Retrieve all vending machines associated with a specific seller (owner) from the database.

        Parameters:
            seller_id (str): The ID of the seller whose vending machines are to be retrieved.

        Returns:
            list: A list of VendingMachine objects associated with the seller.
        """
        cursor = self.connection.cursor()
        
        # Fetch the vending machines where the owner_id matches the seller_id
        cursor.execute('''
            SELECT id, name, location, average_rating FROM vending_machines WHERE owner_id = ?
        ''', (seller_id,))
        rows = cursor.fetchall()

        vending_machines = []
        
        # Create VendingMachine objects for each row
        for row in rows:
            vending_machine = VendingMachine(name=row[1], location=row[2], owner_id=seller_id, average_rating=row[3])
            vending_machine.id = row[0]
            vending_machines.append(vending_machine)
        
        return vending_machines


    def get_vending_machines_by_name(self, machine_name):
        """
        Retrieve vending machines by name from the database.

        Parameters:
            machine_name (str): The name of the vending machine to search for.

        Returns:
            list: A list of VendingMachine objects that match the name.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM vending_machines WHERE name LIKE ?", ('%' + machine_name + '%',))
        rows = cursor.fetchall()

        machines = []
        for row in rows:
            machine = VendingMachine(name=row[1], location=row[2], owner_id=row[3])
            machine.id = row[0]
            machines.append(machine)
        
        return machines
    
    
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
        #print("Chave inserida no db: ", str(vending_machine.id))
        self.connection.commit()


    def update_machine_average_rating(self, machine_id, avg_rating):
        """
        Update the average rating of a product based on a provided rating.

        Parameters:
            machine_id (str): The UUID of the machine to update.
            avg_rating (float): The average rating to set for the product.
        """
        cursor = self.connection.cursor()

        # Atualiza a média de avaliação do produto no banco de dados
        cursor.execute("""
            UPDATE vending_machines
            SET average_rating = ?
            WHERE id = ?
        """, (avg_rating, machine_id))

        # Commit das alterações no banco de dados
        self.connection.commit()


    def delete_vending_machine(self, vending_machine_id):
        """
        Delete a vending machine from the database by its ID.

        Parameters:
            vending_machine_id (str): The ID of the vending machine to delete.
        """
        cursor = self.connection.cursor()

        try:
            # Delete the vending machine
            cursor.execute('DELETE FROM vending_machines WHERE id = ?', (vending_machine_id,))
            self.connection.commit()
            # print(f"Máquina de venda com ID {vending_machine_id} deletada com sucesso.")
        
        except sqlite3.IntegrityError as e:
            # Se houver restrições de integridade, como chaves estrangeiras
            print(f"Erro ao deletar a máquina de venda: {e}")

