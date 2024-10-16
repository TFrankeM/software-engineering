from unittest.mock import patch
import unittest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from main import main

class TestMainFlow(unittest.TestCase):

    @patch("builtins.input", side_effect=["1", "1", "3", "4"])  # Adicionando mais entradas para o fluxo do administrador
    def test_admin_login_and_exit(self, mock_input):
        with patch("builtins.print") as mocked_print:
            main()
            mocked_print.assert_any_call("Saindo do sistema...")

    @patch("builtins.input", side_effect=["2", "1", "3", "4"])  # Adicionando mais entradas para o fluxo do vendedor
    def test_seller_login_and_exit(self, mock_input):
        with patch("builtins.print") as mocked_print:
            main()
            mocked_print.assert_any_call("Saindo do sistema...")

    @patch("builtins.input", side_effect=["3", "1", "3", "4"])  # Adicionando mais entradas para o fluxo do cliente
    def test_customer_login_and_exit(self, mock_input):
        with patch("builtins.print") as mocked_print:
            main()
            mocked_print.assert_any_call("Saindo do sistema...")

    @patch("builtins.input", side_effect=["4"])  # Apenas uma entrada para sair do sistema
    def test_system_exit(self, mock_input):
        with patch("builtins.print") as mocked_print:
            main()
            mocked_print.assert_any_call("Saindo do sistema...")

    @patch("builtins.input", side_effect=["5", "4"])  # Testando uma seleção inválida seguida de saída
    def test_invalid_user_selection(self, mock_input):
        with patch("builtins.print") as mocked_print:
            main()
            mocked_print.assert_any_call("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    unittest.main()
