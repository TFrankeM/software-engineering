import unittest
import sys, os
import sqlite3
import uuid

# Adjust sys.path to point to the "classes" directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))

# Adjust sys.path to point to the "database" directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/database")))

from transaction import Transaction
from transaction_dao import TransactionDAO

class TestTransactionDAO(unittest.TestCase):

    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.dao = TransactionDAO(self.connection)
        self.dao.create_table()

    def test_insert_transaction(self):
        user_id = uuid.uuid4()
        transaction = Transaction(user_id=str(user_id), total_amount=120.00)
        self.dao.insert_transaction(transaction)
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM transactions WHERE id = ?", (str(transaction.id),))
        data = cursor.fetchone()
        self.assertIsNotNone(data)
        self.assertEqual(data[1], str(user_id))

    def tearDown(self):
        self.connection.close()

if __name__ == "__main__":
    unittest.main()
