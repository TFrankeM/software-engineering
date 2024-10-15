def seller_actions():
    """
    Funções específicas do vendedor.
    Este método deve ser expandido com as opções específicas para vendedores.
    """
    print("Bem-vindo, Vendedor!")
    while True:
        print("1. Ver estoque")
        print("2. Gerenciar produtos")
        print("3. Sair")
        escolha = input("Digite o número da ação: ")

        if escolha == "1":
            print("Exibindo estoque das vending machines...")
            # Lógica para exibir o estoque
        elif escolha == "2":
            print("Gerenciando produtos nas vending machines...")
            # Lógica para gerenciar produtos
        elif escolha == "3":
            print("Saindo do painel do vendedor...")
            break
        else:
            print("Opção inválida. Tente novamente.")
