import unittest
import sys, os

# Corrigir caminhos
# adding src to the system path
"""
    os.path.dirname(__file__): diretório do arquivo atual (A)
    os.path.join(A, '../src'): combina o diretório atual com o caminho relativo '../src' (B)
    os.path.abspath(B): converte o caminho relativo '../src' em um caminho absoluto (C)
    sys.path.insert(0, C): insere o caminho absoluto da pasta src no início da lista sys.path (uma lista de diretórios que o Python procura quando importa um módulo) 
"""
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from administrator import Administrator

class TestAdministrator(unittest.TestCase):
    
    def setUp(self):
        """Configuração inicial para os testes."""
        self.admin = Administrator(
            name="Admin User",
            email="admin@example.com",
            password="adminpassword123",
            address="789 Admin Ave"
        )
        
    def test_initialization(self):
        """Testa se o administrador é inicializado corretamente."""
        self.assertEqual(self.admin.name, "Admin User")
        self.assertEqual(self.admin.email, "admin@example.com")
        self.assertTrue(self.admin.verify_password("adminpassword123"))
        self.assertEqual(self.admin.address, "789 Admin Ave")
        self.assertTrue(self.admin.anonymous_profile)
        self.assertIsInstance(self.admin.vending_machines, list)
        self.assertEqual(len(self.admin.vending_machines), 0)  # Inicialmente sem máquinas

    def test_add_vending_machine(self):
        """Testa a adição de uma máquina de venda automática."""
        vending_machine = "Vending Machine 1"  # Simulação de um objeto de máquina de venda
        self.admin.vending_machines.append(vending_machine)
        self.assertIn(vending_machine, self.admin.vending_machines)
        self.assertEqual(len(self.admin.vending_machines), 1)

    def test_change_address(self):
        """Testa a mudança de endereço do administrador."""
        self.admin.change_address = "456 New Admin St"
        self.assertEqual(self.admin.address, "456 New Admin St")

    def test_change_profile_picture_path(self):
        """Testa a mudança do caminho da imagem do perfil."""
        new_path = "../imgs/admin_profile.png"
        self.admin.change_profile_picture_path = new_path
        self.assertEqual(self.admin.profile_picture_path, new_path)

if __name__ == "__main__":
    unittest.main()