import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))
from administrator_dao import AdministratorDAO
from user import UserFactory

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
def create_administrator_account(db_connection):
    """
    Create a new admin account.
    """
    clear_console()
    print("~"*10, "Criar Conta de Administrador:", "~"*10, "\n")

    name = input("Nome: ")
    email = input("Email: ")
    password = input("Senha: ")
    address = input("Endereço: ")
    anonymous_profile = input("Perfil anônimo (sim/nao): ").strip().lower() == 'sim'
    
    confirm = input("\nConfirma criação de conta? [s/n]: ").strip().lower()

    if confirm == "n":
        print("==> Operação cancela.")
        input("\nPressione qualquer tecla para voltar.")
        return
    
    elif confirm == "s":
        # Cria um novo objeto Customer
        admin = UserFactory.create_user(user_type="Administrator", name=name, email=email, password=password, address=address, anonymous_profile=anonymous_profile)

        # Insere o novo cliente no banco de dados
        administrator_dao = AdministratorDAO(db_connection)
        # Check if the 'customer' table exists and create it if necessary
        cursor = db_connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='administrator';")
        table_exists = cursor.fetchone()

        if not table_exists:
            #print("Creating the customer table as it does not exist.")
            administrator_dao.create_table()
        
        administrator_dao.insert_administrator(admin)
        
        print("==> Conta de cliente criada com sucesso!")
    
    else:
        print("==> Entrada inválida. Operação cancela.")

    input("\nPressione qualquer tecla para voltar.")