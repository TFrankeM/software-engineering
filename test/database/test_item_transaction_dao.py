import unittest
import sys, os
import sqlite3
import uuid

# Adjust sys.path to point to the "classes" directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))

# Adjust sys.path to point to the "database" directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/database")))

from item_transaction import ItemTransaction
from item_transaction_dao import ItemTransactionDAO

class TestItemTransactionDAO(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.dao = ItemTransactionDAO(self.connection)
        self.dao.create_table()

    def test_insert_item_transaction(self):
        transaction_id = uuid.uuid4()
        product_id = uuid.uuid4()
        item = ItemTransaction(transaction_id=str(transaction_id), product_id=str(product_id), quantity=20, price=2.50)
        self.dao.insert_item_transaction(item)
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM item_transactions WHERE transaction_id = ? AND product_id = ?", (str(transaction_id), str(product_id)))
        data = cursor.fetchone()
        self.assertIsNotNone(data)
        self.assertEqual(data[2], 20)
        self.assertEqual(data[3], 2.50)

    def tearDown(self):
        self.connection.close()

if __name__ == "__main__":
    unittest.main()
