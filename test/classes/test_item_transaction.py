import unittest
import sys, os
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from item_transaction import ItemTransaction

class TestItemTransaction(unittest.TestCase):

    def test_create_item_transaction(self):
        transaction_id = uuid.uuid4()
        product_id = uuid.uuid4()
        item = ItemTransaction(transaction_id=str(transaction_id), product_id=str(product_id), quantity=10, price=5.50)
        self.assertEqual(item.transaction_id, str(transaction_id))
        self.assertEqual(item.product_id, str(product_id))
        self.assertEqual(item.quantity, 10)
        self.assertEqual(item.price, 5.50)

    def test_item_transaction_representation(self):
        transaction_id = uuid.uuid4()
        product_id = uuid.uuid4()
        item = ItemTransaction(transaction_id=str(transaction_id), product_id=str(product_id), quantity=5, price=3.25)
        self.assertIn(str(transaction_id), repr(item))
        self.assertIn(str(product_id), repr(item))
        self.assertIn("5", repr(item))
        self.assertIn("3.25", repr(item))

if __name__ == "__main__":
    unittest.main()
