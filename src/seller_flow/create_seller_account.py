import time
import sys
import os
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))
from seller_dao import SellerDAO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from user import UserFactory


def clear_console():
    """
        Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def create_seller_account(db_connection):
    """
    Create a new seller account and insert it into the database.

    Parameters:
        db_connection (sqlite3.Connection): The database connection.
    """
    print("Criar Conta de Vendedor:")
    name = input("Nome: ")
    email = input("Email: ")
    password = input("Senha: ")
    address = input("Endereço: ")
    
    # Cria um novo objeto Seller
    seller = UserFactory.create_user(user_type="Seller",name=name, email=email, password=password, address=address)
    
    # Insere o novo vendedor no banco de dados
    seller_dao = SellerDAO(db_connection)
    # Check if the 'sellers' table exists and create it if necessary
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sellers';")
    table_exists = cursor.fetchone()

    if not table_exists:
        #print("Creating the seller table as it does not exist.")
        seller_dao.create_table()
    
    seller_dao.insert_seller(seller)
    
    print("==> Conta de vendedor criada com sucesso!")
    
    input("\nPressione qualquer tecla para voltar.")

    #para verificar se o vendedor foi inserido corretamente e inserido na tabela sellers
    """
    cursor.execute("SELECT * FROM sellers")
    print(cursor.fetchall())
    """