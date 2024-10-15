import unittest
import bcrypt
import sys, os

# Corrigir caminhos
# adding src to the system path
"""
    os.path.dirname(__file__): diretório do arquivo atual (A)
    os.path.join(A, '../../src/classes'): combina o diretório atual com o caminho relativo '../../src/classes' (B)
    os.path.abspath(B): converte o caminho relativo '../../src/classes' em um caminho absoluto (C)
    sys.path.insert(0, C): insere o caminho absoluto da pasta src no início da lista sys.path (uma lista de diretórios que o Python procura quando importa um módulo) 
"""
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from user import User


class TestUser(unittest.TestCase):

    def setUp(self):
        """Set up a User instance for testing."""
        self.user = User(name="John Doe", email="johndoe@example.com", password="password123", address="123 Main St")

    def test_user_id_is_unique(self):
        """Test that the user ID is generated and is unique."""
        user2 = User(name="Jane Doe", email="janedoe@example.com", password="password456")
        self.assertNotEqual(self.user.user_id, user2.user_id)

    def test_name_property(self):
        """Test that the name is set and can be changed."""
        self.assertEqual(self.user.name, "John Doe")
        self.user.change_name = "Jane Doe"
        self.assertEqual(self.user.name, "Jane Doe")

    def test_email_property(self):
        """Test that the email is set and can be changed."""
        self.assertEqual(self.user.email, "johndoe@example.com")
        self.user.change_email = "janedoe@example.com"
        self.assertEqual(self.user.email, "janedoe@example.com")

    def test_address_property(self):
        """Test that the address is set and can be changed."""
        self.assertEqual(self.user.address, "123 Main St")
        self.user.change_address = "456 Another St"
        self.assertEqual(self.user.address, "456 Another St")

    def test_password_hashing(self):
        """Test that the password is hashed and can be verified."""
        self.assertTrue(bcrypt.checkpw("password123".encode('utf-8'), self.user.change_password))

    def test_password_change(self):
        """Test that the password can be changed and verified."""
        self.user.change_password = "newpassword456"
        self.assertTrue(bcrypt.checkpw("newpassword456".encode('utf-8'), self.user.change_password))

    def test_verify_password(self):
        """Test the password verification method."""
        self.assertTrue(self.user.verify_password("password123"))
        self.assertFalse(self.user.verify_password("wrongpassword"))

    def test_profile_picture_path(self):
        """Test that the profile picture path is set to the default and can be changed."""
        self.assertEqual(self.user.profile_picture_path, "../imgs/default.png")
        self.user.change_profile_picture_path = "../imgs/new_profile.png"
        self.assertEqual(self.user.profile_picture_path, "../imgs/new_profile.png")

    def test_anonymous_profile_flag(self):
        """Test the anonymous profile flag is set correctly."""
        self.assertTrue(self.user.anonymous_profile)
        user2 = User(name="John Smith", email="johnsmith@example.com", password="mypassword", anonymous_profile=False)
        self.assertFalse(user2.anonymous_profile)

if __name__ == '__main__':
    unittest.main()
