import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))


from customer_dao import CustomerDAO
from user import UserFactory

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
def create_customer_account(db_connection):
    """
    Create a new customer account.
    """
    clear_console()
    print("~"*10, "Criar Conta de Cliente:", "~"*10, "\n")

    name = input("Nome: ")
    email = input("Email: ")
    password = input("Senha: ")
    address = input("Endereço: ")
    anonymous_profile = input("Perfil anônimo (sim/não): ").strip().lower() == 'sim'
    
    # Cria um novo objeto Customer
    customer = UserFactory.create_user(user_type="Customer", name=name, email=email, password=password, address=address, anonymous_profile=anonymous_profile)

    # Insere o novo cliente no banco de dados
    customer_dao = CustomerDAO(db_connection)
    # Check if the 'customer' table exists and create it if necessary
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers';")
    table_exists = cursor.fetchone()

    if not table_exists:
        #print("Creating the customer table as it does not exist.")
        customer_dao.create_table()
    
    customer_dao.insert_customer(customer)
    
    print("==> Conta de cliente criada com sucesso!")
    
    input("\nPressione qualquer tecla para voltar.")
    
    
    #para verificar se o cliente foi criado com sucesso e inserido na tabela customers
    """
    cursor.execute("SELECT * FROM customers")
    print(cursor.fetchall())
    """