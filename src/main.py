from administrator_flow import administrator_actions
from seller_flow import seller_actions
from customer_flow import customer_actions


def identificar_usuario():
    """
    Função para identificar o tipo de usuário. Pode ser via login ou uma simples seleção.
    Retorna o tipo de usuário como string.
    """
    print("Bem-vindo ao sistema!")
    print("Selecione o tipo de usuário:")
    print("1. Administrador")
    print("2. Vendedor")
    print("3. Usuário")
    print("4. Sair")
    
    escolha = input("Digite o número correspondente: ")

    if escolha == "1":
        return "Administrador"
    elif escolha == "2":
        return "Vendedor"
    elif escolha == "3":
        return "Cliente"
    elif escolha == "4":
        return "Sair"
    else:
        print("Opção inválida. Tente novamente.")
        return identificar_usuario()


def main():
    while True:
        user_type = identificar_usuario()
        
        if user_type == "Administrador":
            administrator_actions()                     # Chama as ações do administrador
        elif user_type == "Vendedor":
            seller_actions()                            # Chama as ações do vendedor
        elif user_type == "Usuario":
            customer_actions()                          # Chama as ações do usuário
        elif user_type == "Sair":
            print("Saindo do sistema...")
            break                                       # Finaliza o programa


if __name__ == "__main__":
    main()
