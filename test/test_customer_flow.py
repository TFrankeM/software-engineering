from unittest.mock import patch
import unittest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from customer_flow import customer_actions

class TestCustomerFlow(unittest.TestCase):

    @patch("builtins.input", side_effect=["1", "3"])
    def test_customer_view_vending_machines(self, mock_input):
        with patch("builtins.print") as mocked_print:
            customer_actions()
            mocked_print.assert_any_call("Exibindo vending machines disponíveis...")

    @patch("builtins.input", side_effect=["2", "3"])
    def test_customer_report_problem(self, mock_input):
        with patch("builtins.print") as mocked_print:
            customer_actions()
            mocked_print.assert_any_call("Reportando problemas...")

    @patch("builtins.input", side_effect=["3"])
    def test_customer_exit(self, mock_input):
        with patch("builtins.print") as mocked_print:
            customer_actions()
            mocked_print.assert_any_call("Saindo do painel do usuário...")

if __name__ == "__main__":
    unittest.main()
