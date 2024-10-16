import unittest
import sys, os
import sqlite3

# Adjust sys.path to point to the "classes" directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))

# Adjust sys.path to point to the "database" directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/database")))

from vending_machine import VendingMachine
from vending_machine_dao import VendingMachineDAO



class TestVendingMachineDAO(unittest.TestCase):

    def setUp(self):
        """
             Set up an in-memory SQLite database and VendingMachineDAO for testing.
        """
        # Connect to an in-memory database for testing
        self.connection = sqlite3.connect(":memory:")
        self.vending_machine_dao = VendingMachineDAO(self.connection)

        # Create the vending_machines table for testing
        self.vending_machine_dao.create_table()


    def tearDown(self):
        """
            Tear down the database connection after each test.
        """
        self.connection.close()


    def test_create_vending_machine(self):
        """
            Test inserting a vending machine into the database.
        """
        vending_machine = VendingMachine(name="Vending Machine A", location="Floor 1", owner_id="owner123")
        self.vending_machine_dao.insert_vending_machine(vending_machine)

        # Retrieve the inserted vending machine and verify its details
        retrieved_vending_machine = self.vending_machine_dao.get_vending_machine_by_id(str(vending_machine.id))
        self.assertIsNotNone(retrieved_vending_machine)
        self.assertEqual(retrieved_vending_machine.name, "Vending Machine A")
        self.assertEqual(retrieved_vending_machine.location, "Floor 1")
        self.assertEqual(retrieved_vending_machine.owner_id, "owner123")


    def test_get_vending_machine_by_id(self):
        """
            Test retrieving a vending machine by its ID from the database.
        """
        vending_machine = VendingMachine(name="Vending Machine B", location="Floor 2", owner_id="owner456")
        self.vending_machine_dao.insert_vending_machine(vending_machine)

        # Retrieve the vending machine by its ID
        retrieved_vending_machine = self.vending_machine_dao.get_vending_machine_by_id(str(vending_machine.id))
        self.assertIsNotNone(retrieved_vending_machine)
        self.assertEqual(retrieved_vending_machine.name, "Vending Machine B")
        self.assertEqual(retrieved_vending_machine.location, "Floor 2")
        self.assertEqual(retrieved_vending_machine.owner_id, "owner456")


    def test_delete_vending_machine(self):
        """
            Test deleting a vending machine from the database.
        """
        vending_machine = VendingMachine(name="Vending Machine C", location="Floor 3", owner_id="owner789")
        self.vending_machine_dao.insert_vending_machine(vending_machine)

        # Delete the vending machine
        self.vending_machine_dao.delete_vending_machine(str(vending_machine.id))

        # Verify that the vending machine has been deleted
        retrieved_vending_machine = self.vending_machine_dao.get_vending_machine_by_id(str(vending_machine.id))
        self.assertIsNone(retrieved_vending_machine)


    def test_vending_machine_not_found(self):
        """
            Test retrieving a non-existent vending machine.
        """
        # Try to get a vending machine that does not exist
        non_existent_vending_machine = self.vending_machine_dao.get_vending_machine_by_id("invalid_id")
        self.assertIsNone(non_existent_vending_machine)


if __name__ == "__main__":
    unittest.main()