from administrator_flow import administrator_actions
from seller_flow import seller_actions
from customer_flow import customer_actions
from customer_flow import create_customer_account
from seller_flow import create_seller_account
from db_initializer import initialize_db 
import time
import os

# Variáveis globais para armazenar os IDs do usuário logado
current_customer_id = None
current_seller_id = None

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def criar_nova_conta(db_connection):
    """
    Função para criar uma nova conta.
    Permite escolher entre cliente ou vendedor e direciona para a tela de cadastro.
    """
    clear_console()
    print("~"*10, "Criar Conta", "~"*10, "\n")
    print("Selecione o tipo de conta a criar:")
    print("1. Cliente")
    print("2. Vendedor")
    print("0. Voltar")

    escolha = input("Digite o número correspondente: ")

    if escolha == "1":
        clear_console()
        print("Criando conta de cliente...")
        create_customer_account(db_connection)
        print("Conta de cliente criada com sucesso!")
    elif escolha == "2":
        clear_console()
        print("Criando conta de vendedor...")
        create_seller_account(db_connection)
        print("Conta de vendedor criada com sucesso!")
    elif escolha == "0":
        return
    else:
        print("Opção inválida. Tente novamente.")
        time.sleep(2)
        criar_nova_conta(db_connection)

def identificar_usuario():
    """
    Função para identificar o tipo de usuário. Permite login ou criação de conta.
    Retorna o tipo de usuário como uma string.
    """
    clear_console()
    
    print("~"*10, "Bem-vindo ao Sistema Compre Aqui!", "~"*10, "\n")
    print("Selecione uma opção:")
    print("1. Administrador")
    print("2. Vendedor")
    print("3. Cliente")
    print("4. Não tem conta? Crie uma conta!")
    print("0. Sair")
    
    escolha = input("Digite o número correspondente: ")

    if escolha == "1":
        return "Administrador"
    elif escolha == "2":
        return "Vendedor"
    elif escolha == "3":
        return "Cliente"
    elif escolha == "4":
        return "Criar Conta"
    elif escolha == "0":
        return "Sair"
    else:
        print("\rOpção inválida. Tente novamente.", flush=True)
        time.sleep(2)
        return identificar_usuario()


def main():
    global current_customer_id, current_seller_id

    # Inicializa o banco de dados
    db_connection = initialize_db()  # Chama a função que inicializa o banco de dados
    
    while True:
        user_type = identificar_usuario()
        
        if user_type == "Administrador":
            administrator_actions(db_connection)  # Chama as ações do administrador
        elif user_type == "Vendedor":
            current_seller_id = '1'  # Aqui você pode implementar o fluxo de login para vendedores
            seller_actions(seller_id=current_seller_id, db_connection=db_connection)
        elif user_type == "Cliente":
            current_customer_id = '1'  # Aqui você pode implementar o fluxo de login para clientes
            customer_actions(customer_id=current_customer_id, db_connection=db_connection)
        elif user_type == "Criar Conta":
            criar_nova_conta(db_connection)  # Chama o fluxo de criação de conta
        elif user_type == "Sair":
            print("Saindo do sistema...")
            time.sleep(2)
            clear_console()
            print("~"*10, "Volte sempre", "~"*10)
            break  # Finaliza o programa


if __name__ == "__main__":
    main()
