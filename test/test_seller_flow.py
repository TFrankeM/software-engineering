from unittest.mock import patch
import unittest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from seller_flow import seller_actions

class TestSellerFlow(unittest.TestCase):

    @patch("builtins.input", side_effect=["1", "3"])
    def test_seller_view_stock(self, mock_input):
        with patch("builtins.print") as mocked_print:
            seller_actions()
            mocked_print.assert_any_call("Exibindo estoque das vending machines...")

    @patch("builtins.input", side_effect=["2", "3"])
    def test_seller_manage_products(self, mock_input):
        with patch("builtins.print") as mocked_print:
            seller_actions()
            mocked_print.assert_any_call("Gerenciando produtos nas vending machines...")

    @patch("builtins.input", side_effect=["3"])
    def test_seller_exit(self, mock_input):
        with patch("builtins.print") as mocked_print:
            seller_actions()
            mocked_print.assert_any_call("Saindo do painel do vendedor...")

if __name__ == "__main__":
    unittest.main()
