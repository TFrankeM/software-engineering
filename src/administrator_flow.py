def administrator_actions():
    """
    Funções específicas do administrador.
    Este método deve ser expandido com as opções específicas para administradores.
    """
    print("Bem-vindo, Administrador!")
    while True:
        print("1. Ver relatórios")
        print("2. Gerenciar permissões")
        print("3. Sair")
        escolha = input("Digite o número da ação: ")

        if escolha == "1":
            print("Exibindo relatórios...")
            # Aqui você adiciona a lógica para exibir relatórios
        elif escolha == "2":
            print("Gerenciando permissões...")
            # Lógica para gerenciar permissões
        elif escolha == "3":
            print("Saindo do painel do administrador...")
            break
        else:
            print("Opção inválida. Tente novamente.")
