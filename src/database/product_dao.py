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
            Create the product table in the database if it doesn't already exist.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                machine_id TEXT NOT NULL,  -- Foreign key referencing the vending machine
                FOREIGN KEY (machine_id) REFERENCES vending_machines(id)
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
            INSERT INTO products (id, name, description, price, quantity, machine_id)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (str(product.id), product.name, product.description, product.price, product.quantity, product.machine_id))
        self.connection.commit()


    def update_product(self, product):
        """
        Update product information in the database.

        Parameters:
            product (Product): The product object containing updated information.
        """
        cursor = self.connection.cursor()
        
        # Atualiza as informações do produto na tabela 'products'
        cursor.execute("""
            UPDATE products
            SET name = ?, description = ?, price = ?, quantity = ?
            WHERE id = ?
        """, (product.name, product.description, product.price, product.quantity, str(product.id)))

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


    def get_products_by_vending_machine_id(self, vending_machine_id):
        """
        Retrieve all products associated with a specific vending machine by its ID and return them as Product objects.

        Parameters:
            vending_machine_id (str): The ID of the vending machine.

        Returns:
            list: A list of Product objects representing the products in the vending machine.
        """
        cursor = self.connection.cursor()

        # Query to fetch all products related to the given vending machine ID
        cursor.execute('''
            SELECT * FROM products WHERE machine_id = ?
        ''', (vending_machine_id,))

        rows = cursor.fetchall()

        # Create a list of Product objects
        products = []
        for row in rows:
            product = Product(
                name=row[1],            # Name of the product
                description=row[2],     # Description of the product
                price=row[3],           # Price of the product
                quantity=row[4]         # Quantity of the product
            )
            product.id = row[0]           # Set the product ID
            product.machine_id = row[5]   # Set the machine ID
            products.append(product)

        return products


    def get_products_by_name(self, product_name):
        """
        Retrieve products by name from the database.

        Parameters:
            product_name (str): The name of the product to search for.

        Returns:
            list: A list of Product objects that match the name.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + product_name + '%',))
        rows = cursor.fetchall()

        products = []
        for row in rows:
            product = Product(name=row[1], description=row[2], price=row[3], quantity=row[4], machine_id=row[5])
            product.id = row[0]
            products.append(product)
        
        return products
    
    
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

    def delete_products_by_vending_machine_id(self, vending_machine_id):
        """
            Delete all products associated with a specific vending machine.

        Parameters:
            vending_machine_id (str): The ID of the vending machine whose products should be deleted.
        """
        cursor = self.connection.cursor()

        # Deletar todos os produtos associados à máquina de venda
        cursor.execute('DELETE FROM products WHERE machine_id = ?', (vending_machine_id,))

        self.connection.commit()
