from datetime import datetime
import unittest
import sys, os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from transaction import Transaction

class TestTransaction(unittest.TestCase):

    def test_create_transaction(self):
        user_id = uuid.uuid4()
        transaction = Transaction(user_id=str(user_id), total_amount=100.00)
        self.assertEqual(transaction.user_id, str(user_id))
        self.assertEqual(transaction.total_amount, 100.00)
        self.assertIsInstance(transaction.transaction_date, datetime)

    def test_transaction_representation(self):
        user_id = uuid.uuid4()
        transaction = Transaction(user_id=str(user_id), total_amount=150.00)
        self.assertIn(str(user_id), repr(transaction))
        self.assertIn("150.0", repr(transaction))


if __name__ == "__main__":
    unittest.main()
