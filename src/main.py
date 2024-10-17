from administrator_flow import administrator_actions
from seller_flow import seller_actions
from customer_flow import customer_actions
from db_initializer import initialize_db 
import time
import os


def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def identificar_usuario():
    """
    Function to identify the user type. It can be via login or a simple selection.
    Returns the user type as a string.
    """
    clear_console()
    
    print("~"*10, "Bem-vindo ao Sistema Compre Aqui!", "~"*10, "\n")
    print("Selecione o tipo de usuário:")
    print("1. Administrador")
    print("2. Vendedor")
    print("3. Cliente")
    print("0. Sair")
    
    escolha = input("Digite o número correspondente: ")

    if escolha == "1":
        return "Administrador"
    elif escolha == "2":
        return "Vendedor"
    elif escolha == "3":
        return "Cliente"
    elif escolha == "0":
        return "Sair"
    else:
        print("\rOpção inválida. Tente novamente.", flush=True)
        time.sleep(2)
        return identificar_usuario()


def main():
    # Inicializa o banco de dados
    db_connection = initialize_db()  # Chama a função que inicializa o banco de dados
    
    while True:
        user_type = identificar_usuario()
        
        if user_type == "Administrador":
            administrator_actions()  # Chama as ações do administrador
        elif user_type == "Vendedor":
            seller_id = '1'  # Simulação de um ID de vendedor
            seller_actions(seller_id=seller_id, db_connection=db_connection)  # Chama as ações do vendedor
        elif user_type == "Cliente":
            customer_id = '1'
            customer_actions(customer_id=customer_id, db_connection=db_connection)  # Chama as ações do cliente
        elif user_type == "Sair":
            print("Saindo do sistema...")
            time.sleep(2)
            clear_console()
            print("~"*10, "Volte sempre", "~"*10)
            break  # Finaliza o programa


if __name__ == "__main__":
    main()
