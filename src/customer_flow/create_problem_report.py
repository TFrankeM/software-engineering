import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))


from problem_report_dao import ProblemReportDAO
from problem_report import ProblemReport
from problem_types import SYSTEM_PROBLEM_TYPES, MACHINE_PROBLEM_TYPES

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def create_problem_report(customer_id, db_connection):
    """
    Create a problem report for a vending machine or the system.
    """
    clear_console()
    print("~"*10, "Reportar Problema", "~"*10)

    # Pergunta se o problema é relacionado a uma máquina ou ao sistema
    tipo_problema = input("\nO problema está relacionado a uma máquina ou ao sistema? (Digite 'm' para máquina ou 's' para sistema): ").strip().lower()
    
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