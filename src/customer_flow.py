import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src/database")))

from problem_report_dao import ProblemReportDAO
from problem_report import ProblemReport
from problem_types import SYSTEM_PROBLEM_TYPES, MACHINE_PROBLEM_TYPES

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def customer_actions(customer_id, db_connection):    
    """
    Main function for the customer panel.
    """
    clear_console()
    
    problem_report_dao = ProblemReportDAO(db_connection)

    # Check if the 'problem_report' table exists and create it if necessary
    cursor = db_connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='problem_report';")
    table_exists = cursor.fetchone()

    if not table_exists:
        print("Creating the problem_report table as it does not exist.")
        problem_report_dao.create_table()


    print("Bem-vindo, Cliente!")
    while True:
        print("1. Visualizar vending machines")
        print("2. Reportar problemas")
        print("3. Sair")
        escolha = input("Digite o número da ação: ")

        if escolha == "1":
            print("Exibindo vending machines disponíveis...")
            # Lógica para exibir as máquinas de vendas
        elif escolha == "2":
            create_problem_report(customer_id, db_connection)
        elif escolha == "3":
            print("Saindo do painel do usuário...")
            break
        else:
            print("Opção inválida. Tente novamente.")


def select_problem_type():
    """
    Provide a menu to select the problem type.
    """
    print("\nSelecione o tipo de problema:")
    print("1. Problema no Sistema")
    print("2. Problema na Máquina")

    problem_category = input("Digite o número da categoria de problema: ")

    if problem_category == "1":
        return select_system_problem_type()
    elif problem_category == "2":
        return select_machine_problem_type()
    else:
        print("Opção inválida. Tente novamente.")
        return select_problem_type()


def select_system_problem_type():
    """
    Provide a menu to select the system problem type.
    """
    print("\nTipos de Problema no Sistema:")
    for i, problem in enumerate(SYSTEM_PROBLEM_TYPES, 1):
        print(f"{i}. {problem}")
    
    choice = input("Escolha o tipo de problema (número): ")
    
    try:
        choice_int = int(choice)
        if 1 <= choice_int <= len(SYSTEM_PROBLEM_TYPES):
            return SYSTEM_PROBLEM_TYPES[choice_int - 1]
        else:
            raise ValueError
    except ValueError:
        print("Seleção inválida. Tente novamente.")
        return select_system_problem_type()


def select_machine_problem_type():
    """
    Provide a menu to select the machine problem type.
    """
    print("\nTipos de Problema na Máquina:")
    for i, problem in enumerate(MACHINE_PROBLEM_TYPES, 1):
        print(f"{i}. {problem}")
    
    choice = input("Escolha o tipo de problema (número): ")

    try:
        choice_int = int(choice)
        if 1 <= choice_int <= len(MACHINE_PROBLEM_TYPES):
            return MACHINE_PROBLEM_TYPES[choice_int - 1]
        else:
            raise ValueError
    except ValueError:
        print("Seleção inválida. Tente novamente.")
        return select_machine_problem_type()


def create_problem_report(customer_id, db_connection):
    """
    Create a problem report for a vending machine or the system.
    """
    print("Reportar Problema:")

    # Pergunta se o problema é relacionado a uma máquina ou ao sistema
    tipo_problema = input("O problema está relacionado a uma máquina ou ao sistema? (Digite 'm' para máquina ou 's' para sistema): ").strip().lower()
    
    # Se for um problema de máquina
    if tipo_problema == 'm':
        machine_id = input("Digite o ID da máquina com problema: ")
        print("Selecione o tipo de problema de máquina:")
        for idx, problem in enumerate(MACHINE_PROBLEM_TYPES, 1):
            print(f"{idx}. {problem}")
        problem_choice = int(input("Digite o número do tipo de problema: "))
        problem_type = MACHINE_PROBLEM_TYPES[problem_choice - 1]

    # Se for um problema do sistema
    elif tipo_problema == 's':
        machine_id = None  # O problema de sistema não está associado a uma máquina
        print("Selecione o tipo de problema do sistema:")
        for idx, problem in enumerate(SYSTEM_PROBLEM_TYPES, 1):
            print(f"{idx}. {problem}")
        problem_choice = int(input("Digite o número do tipo de problema: "))
        problem_type = SYSTEM_PROBLEM_TYPES[problem_choice - 1]

    else:
        print("Opção inválida. Por favor, tente novamente.")
        return

    # Comentário opcional
    if problem_choice != 4:
        comment = input("Escreva um comentário sobre o problema (opcional): ")
    # Comentário obrigatório(para "Outro" problema)
    else:
        comment = input("Escreva um comentário sobre o problema (obrigatório): ")

    # Cria um novo relatório de problema
    problem_report = ProblemReport(author_id=customer_id, machine_id=machine_id, problem_type=problem_type, comment=comment)
    
    # Salva o relatório de problema no banco de dados
    problem_report_dao = ProblemReportDAO(db_connection)
    problem_report_dao.insert_problem_report(problem_report)
    
    print("Problema reportado com sucesso!")
    time.sleep(2)

    

