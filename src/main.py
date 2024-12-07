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
    import bcrypt

    print(f"\n--- Login {user_type} ---")
    username = input("Digite seu nome de usuário: ")
    password = input("Digite sua senha: ")

    try:
        cursor = db_connection.cursor()
        table = 'customers' if user_type == 'Customer' else 'sellers'
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
                time.sleep(2)
                return user_id
            else:
                print("Senha incorreta. Tente novamente.")
                time.sleep(3)
        else:
            print("Usuário não encontrado. Tente novamente.")
            time.sleep(3)
    except Exception as e:
        print(f"Erro ao tentar fazer login: {e}")
        time.sleep(3)

    return None

def identificar_usuario():
    """
    Function to identify the user type. Displays the main menu.
    Returns the user's choice as a string.
    """
    clear_console()
    
    print("~"*10, "Bem-vindo ao Sistema Compre Aqui!", "~"*10, "\n")
    print("Selecione uma opção:")
    print("1. Administrador")
    print("2. Fazer Login")
    print("3. Não tem conta? Crie uma conta!")
    print("0. Sair")

    escolha = input("Digite o número correspondente: ")

    if escolha == "1":
        return "Administrador"
    elif escolha == "2":
        return "Login"
    elif escolha == "3":
        return "Criar Conta"
    elif escolha == "0":
        return "Sair"
    else:
        print("\rOpção inválida. Tente novamente.", flush=True)
        time.sleep(2)
        return identificar_usuario()

def criar_conta(db_connection):
    """
    Create either a customer or seller account.

    Args:
        db_connection: Database connection object.
    """
    clear_console()
    print("\n--- Criar Conta ---")
    print("Selecione o tipo de conta:")
    print("1. Cliente")
    print("2. Vendedor")
    opcao = input("Digite o número correspondente: ")

    if opcao == "1":
        create_customer_account(db_connection)
        print("Conta de cliente criada com sucesso!")
    elif opcao == "2":
        create_seller_account(db_connection)
        print("Conta de vendedor criada com sucesso!")
    else:
        print("Opção inválida. Retornando ao menu principal.")
        time.sleep(2)

def main():
    # Inicializa o banco de dados
    db_connection = initialize_db()

    while True:
        user_choice = identificar_usuario()

        if user_choice == "Administrador":
            administrator_actions(db_connection)  # Chama as ações do administrador
        elif user_choice == "Login":
            clear_console()
            print("\nSelecione o tipo de login:")
            print("1. Cliente")
            print("2. Vendedor")
            login_type = input("Digite o número correspondente: ")

            if login_type == "1":
                customer_id = login_user("Customer", db_connection)
                if customer_id:
                    customer_actions(customer_id=customer_id, db_connection=db_connection)
            elif login_type == "2":
                seller_id = login_user("Seller", db_connection)
                if seller_id:
                    seller_actions(seller_id=seller_id, db_connection=db_connection)
            else:
                print("Opção inválida. Retornando ao menu principal.")
                time.sleep(2)
        elif user_choice == "Criar Conta":
            criar_conta(db_connection)
        elif user_choice == "Sair":
            print("Saindo do sistema...")
            time.sleep(2)
            clear_console()
            print("~"*10, "Volte sempre", "~"*10)
            break  # Finaliza o programa


if __name__ == "__main__":
    main()
