from visualize_problem_reports import visualize_problem_reports
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))
from sales_report import main_menu

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
def administrator_actions(db_pool):
    """
    Administrator-specific functions.
    This method will gradually be expanded with administrator-specific options.
    
    Parameters:
        db_pool: database connection pool.
    """

    db_connection = db_pool.get_connection()         # Pega uma conexão do pool
    
    while True:
        clear_console()
        print("~"*10, "Bem-vindo, Administrador!", "~"*10, "\n")

        print("1. Visualizar reportes de problemas")
        print("2. Gerar Relatórios")
        print("3. Gerenciar permissões")
        print("0. Sair")
        escolha = input("Digite o número da ação: ")

        if escolha == "1":
            visualize_problem_reports(db_connection)
        elif escolha == "2":
            main_menu(db_connection)
            time.sleep(2)
        elif escolha == "3":
            print("Funcionalidade ainda não disponível. Fique atento para futuras atualizações.")
            time.sleep(2)
        elif escolha == "0":
            break
        else:
            print("\nOpção inválida. Tente novamente.")
    
    db_pool.release_connection(db_connection)        # Devolve a conexão ao pool

