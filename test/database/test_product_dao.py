import unittest
import sys, os
import sqlite3
import uuid

# Adjust sys.path to point to the "classes" directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))

# Adjust sys.path to point to the "database" directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/database")))

from product import Product
from product_dao import ProductDAO

class TestProductDAO(unittest.TestCase):

    def setUp(self):
        """
        Set up an in-memory SQLite database and ProductDAO for testing.
        """
        self.connection = sqlite3.connect(":memory:")           # In-memory database for testing
        self.product_dao = ProductDAO(self.connection)
        self.product_dao.create_table()                          # Create the table for products

    def tearDown(self):
        """
        Tear down the database connection after each test.
        """
        self.connection.close()

    def test_insert_product(self):
        """
        Test inserting a product into the database with machine_id.
        """
        machine_id = str(uuid.uuid4())  # Simulating a machine ID
        product = Product(name="Chips", description="A bag of chips", price=4.99, quantity=100, machine_id=machine_id)
        self.product_dao.insert_product(product)

        # Verify that the product is inserted
        products = self.product_dao.get_all_products()
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0][1], "Chips")           # Name
        self.assertEqual(products[0][2], "A bag of chips")  # Description
        self.assertEqual(products[0][5], machine_id)        # Machine ID

    def test_find_product_by_id(self):
        """
        Test finding a product by its UUID in the database.
        """
        machine_id = str(uuid.uuid4())  # Simulating a machine ID
        product = Product(name="Soda", description="A can of soda", price=1.5, quantity=50, machine_id=machine_id)
        self.product_dao.insert_product(product)

        found_product = self.product_dao.find_product_by_id(str(product.id))
        self.assertIsNotNone(found_product)
        self.assertEqual(found_product[1], "Soda")          # Name
        self.assertEqual(found_product[5], machine_id)      # Machine ID

    def test_update_product_quantity(self):
        """
        Test updating the quantity of a product in the database.
        """
        machine_id = str(uuid.uuid4())  # Simulating a machine ID
        product = Product(name="Water", description="A bottle of water", price=1.0, quantity=200, machine_id=machine_id)
        self.product_dao.insert_product(product)

        # Update the quantity
        self.product_dao.update_product_quantity(str(product.id), 150)

        # Check if the update was successful
        updated_product = self.product_dao.find_product_by_id(str(product.id))
        self.assertEqual(updated_product[4], 150)  # Quantity

    def test_delete_product(self):
        """
        Test deleting a product from the database.
        """
        machine_id = str(uuid.uuid4())  # Simulating a machine ID
        product = Product(name="Juice", description="A bottle of juice", price=3.0, quantity=75, machine_id=machine_id)
        self.product_dao.insert_product(product)

        # Delete the product
        self.product_dao.delete_product(str(product.id))

        # Verify that the product is deleted
        deleted_product = self.product_dao.find_product_by_id(str(product.id))
        self.assertIsNone(deleted_product)
        

if __name__ == "__main__":
    unittest.main()
