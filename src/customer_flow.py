def customer_actions():
    """
    Funções específicas do usuário comum.
    Este método deve ser expandido com as opções específicas para usuários.
    """
    print("Bem-vindo, Usuário!")
    while True:
        print("1. Visualizar vending machines")
        print("2. Reportar problemas")
        print("3. Sair")
        escolha = input("Digite o número da ação: ")

        if escolha == "1":
            print("Exibindo vending machines disponíveis...")
            # Lógica para exibir as máquinas de vendas
        elif escolha == "2":
            print("Reportando problemas...")
            # Chama a função de reportar problemas
        elif escolha == "3":
            print("Saindo do painel do usuário...")
            break
        else:
            print("Opção inválida. Tente novamente.")
