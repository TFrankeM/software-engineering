def administrator_actions(db_connection):
    """
    Funções específicas do administrador.
    Este método deve ser expandido com as opções específicas para administradores.
    """
    print("Bem-vindo, Administrador!")
    while True:
        print("1. Ver relatórios")
        print("2. Gerenciar permissões")
        print("3. Visualizar reportes de problemas")
        print("4. Sair")
        escolha = input("Digite o número da ação: ")

        if escolha == "1":
            print("Exibindo relatórios...")
            # Aqui você adiciona a lógica para exibir relatórios
        elif escolha == "2":
            print("Gerenciando permissões...")
            # Lógica para gerenciar permissões
        elif escolha == "3":
            # Lógica para visualizar reportes de problemas
            visualize_problem_reports(db_connection)
        elif escolha == "4":
            print("Saindo do painel do administrador...")
            break
        else:
            print("Opção inválida. Tente novamente.")


def visualize_problem_reports(db_connection):
    """
    Visualize the problem reports made by customers.
    """
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM problem_reports")
    reports = cursor.fetchall()
    if not reports:
        print("Nenhum reporte de problema encontrado.")
    else:
        print("Reportes de problemas:")
        for report in reports:
            print(f"ID do reporte: {report[0]}")
            print(f"ID do autor (customer_id): {report[1]}")
            print(f"Tipo de Problema: {report[2]}")
            print(f"Descrição: {report[3]}")
            print(f"ID da máquina: {report[4]}")
            print(f"Data e Hora: {report[5]}")
            print("-"*10)
    cursor.close()
    