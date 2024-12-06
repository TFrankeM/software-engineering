from visualize_problem_reports import visualize_problem_reports
import time
import sys
import os


def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
def administrator_actions(db_connection):
    """
    Funções específicas do administrador.
    Este método deve ser expandido com as opções específicas para administradores.
    """

    while True:
        clear_console()
        print("~"*10, "Bem-vindo, Administrador!", "~"*10, "\n")

        print("1. Visualizar reportes de problemas")
        print("2. Ver Relatórios Básicos")
        print("3. Gerenciar permissões")
        print("0. Sair")
        escolha = input("Digite o número da ação: ")

        if escolha == "1":
            visualize_problem_reports(db_connection)
        elif escolha == "2":
            print("Funcionalidade ainda não disponível. Fique atento para futuras atualizações.")
            time.sleep(2)
            # Área de futura expanção: lógica para gerenciar permissões
        elif escolha == "3":
            print("Funcionalidade ainda não disponível. Fique atento para futuras atualizações.")
            time.sleep(2)
        elif escolha == "0":
            print("\nSaindo do painel do administrador...")
            time.sleep(1.5)
            break
        else:
            print("\nOpção inválida. Tente novamente.")
