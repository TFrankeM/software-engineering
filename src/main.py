from db_initializer import initialize_db 
import bcrypt
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "customer_flow")))
from main_customer_flow import customer_actions
from create_customer_account import create_customer_account

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "administrator_flow")))
from main_administrator_flow import administrator_actions
from create_administrator_account import create_administrator_account

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "seller_flow")))
from main_seller_flow import seller_actions
from create_seller_account import create_seller_account

# Variáveis globais para armazenar os IDs do usuário logado
current_customer_id = None
current_seller_id = None

def clear_console():
    """
    Console clearing function, (Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def login_user(user_type, db_connection):
    """
    Handle user login by verifying their credentials.

    Args:
        db_connection: The database connection.
        user_type (str): Either 'Customer' or 'Seller'.

    Returns:
        int: User ID if login is successful, None otherwise.
    """
    clear_console()
    if user_type == "Administrator":
        name = "Admin"
    elif user_type == "Customer":
        name = "Cliente"
    elif user_type == "Seller":
        name = "Vendedor"

    print("~"*10, f"Login {name}", "~"*10, "\n")

    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")

    try:
        cursor = db_connection.cursor()
        if user_type == 'Customer':
            table = 'customers' 
        elif user_type == 'Seller':
            table = 'sellers' 
        else:
            table = 'administrators'
        query = f"SELECT id, password FROM {table} WHERE name = ?"
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        if result:
            user_id, hashed_password = result

            # Certifique-se de que o hash recuperado do banco está em bytes
            if isinstance(hashed_password, str):
                hashed_password = hashed_password.encode('utf-8')

            # Validação da senha
            senha_teste = password
            hash_teste = bcrypt.hashpw(senha_teste.encode('utf-8'), bcrypt.gensalt())
            print(bcrypt.checkpw(senha_teste.encode('utf-8'), hash_teste))  # Deve ser True
            
            
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
                print("Login bem-sucedido!")
                time.sleep(1)
                return user_id
            else:
                print("Senha incorreta. Tente novamente.")
                time.sleep(2)
        else:
            print("Usuário não encontrado. Tente novamente.")
            time.sleep()
    except Exception as e:
        print(f"Erro ao tentar fazer login: {e}")
        time.sleep(2)

    return None

def identificar_usuario():
    """
    Function to identify the user type. Displays the main menu.
    Returns the user's choice as a string.
    """

    while True:
        clear_console()
        print("~"*10, "Bem-vindo ao Sistema Compre Aqui!", "~"*10, "\n")

        print("Selecione uma opção:")
        print("1. Fazer Login")
        print("2. Não tem conta? Crie uma conta!")
        print("0. Sair")

        escolha = input("\nDigite o número correspondente: ")

        if escolha == "1":
            return "Login"
        elif escolha == "2":
            return "Criar Conta"
        elif escolha == "0":
            return "Sair"
        else:
            print("\rOpção inválida. Tente novamente.", flush=True)
            time.sleep(2)

def fazer_login(db_connection_pool):
    while True:
        clear_console()
        print("~"*10, "Selecione o tipo de login", "~"*10, "\n")

        print("1. Administrador ")
        print("2. Cliente")
        print("3. Vendedor")
        print("0. Voltar")
        login_type = input("\nDigite o número correspondente: ")

        if login_type == "0":
            break

        elif login_type == "1":
            db_connection = db_connection_pool.get_connection()         # Pega uma conexão do pool
            customer_id = login_user("Administrator", db_connection)
            db_connection_pool.release_connection(db_connection)        # Devolve a conexão ao pool
            administrator_actions(db_connection_pool)  # Chama as ações do administrador

        elif login_type == "2":
            db_connection = db_connection_pool.get_connection()         # Pega uma conexão do pool
            customer_id = login_user("Customer", db_connection)
            db_connection_pool.release_connection(db_connection)        # Devolve a conexão ao pool

            if customer_id:
                customer_actions(customer_id=customer_id, db_pool=db_connection_pool)

        elif login_type == "3":
            db_connection = db_connection_pool.get_connection()         # Pega uma conexão do pool
            seller_id = login_user("Seller", db_connection)
            db_connection_pool.release_connection(db_connection)        # Devolve a conexão ao pool

            if seller_id:
                seller_actions(seller_id=seller_id, db_pool=db_connection_pool)
        else:
            print("Entrada inválida. Digite uma opção válida.")
            time.sleep(2)

def criar_conta(db_connection):
    """
    Create either a customer or seller account.

    Args:
        db_connection: Database connection object.
    """
    while True:
        clear_console()
        print("~"*10, "Criar conta", "~"*10, "\n")

        print("Selecione o tipo de conta:")
        print("1. Administrador")
        print("2. Cliente")
        print("3. Vendedor")
        print("0. Voltar")
        opcao = input("\nDigite o número correspondente: ")

        if opcao == "0":
            return
        elif opcao == "1":
            create_administrator_account(db_connection)
            break
        elif opcao == "2":
            create_customer_account(db_connection)
            break
        elif opcao == "3":
            create_seller_account(db_connection)
            break
        else:
            print("Entrada inválida. Digite uma opção válida.")
            time.sleep(2)
        

def main():
    # Inicializa o pool de conexões com o banco de dados
    db_connection_pool = initialize_db()

    while True:
        user_choice = identificar_usuario()

        if user_choice == "Login":
            fazer_login(db_connection_pool)

        elif user_choice == "Criar Conta":
            db_connection = db_connection_pool.get_connection()         # Pega uma conexão do pool
            criar_conta(db_connection)
            db_connection_pool.release_connection(db_connection)        # Devolve a conexão ao pool

        elif user_choice == "Sair":
            print("Saindo do sistema...")
            time.sleep(2)

            clear_console()
            print("~"*10, "Volte sempre", "~"*10)
            break  # Finaliza o programa


if __name__ == "__main__":
    main()
