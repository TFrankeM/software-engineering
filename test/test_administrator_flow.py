from unittest.mock import patch
import unittest
import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
from administrator_flow import administrator_actions

class TestAdminFlow(unittest.TestCase):
    
    @patch("builtins.input", side_effect=["1", "3"])
    def test_admin_view_reports(self, mock_input):
        with patch("builtins.print") as mocked_print:
            administrator_actions()
            mocked_print.assert_any_call("Exibindo relatórios...")

    @patch("builtins.input", side_effect=["2", "3"])
    def test_admin_manage_permissions(self, mock_input):
        with patch("builtins.print") as mocked_print:
            administrator_actions()
            mocked_print.assert_any_call("Gerenciando permissões...")

    @patch("builtins.input", side_effect=["3"])
    def test_admin_exit(self, mock_input):
        with patch("builtins.print") as mocked_print:
            administrator_actions()
            mocked_print.assert_any_call("Saindo do painel do administrador...")

if __name__ == "__main__":
    unittest.main()
