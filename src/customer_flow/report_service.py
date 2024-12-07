from abc import ABC, abstractmethod
import pandas as pd
import time
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from problem_report import ProblemReport, ProblemReportFactory

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../database")))
from problem_report_dao import ProblemReportDAO
from problem_types import SYSTEM_PROBLEM_TYPES, MACHINE_PROBLEM_TYPES
from vending_machine_dao import VendingMachineDAO

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


class ProblemReportStrategy(ABC):
    """
    Interface de estratégia para coleta de dados para o relatório de problema.
    """

    @abstractmethod
    def collect_data(self):
        pass


class MachineProblemReportStrategy(ProblemReportStrategy):
    """
    Strategy for collecting data related to a machine problem.
    """
    def __init__(self, db_connection):
        self.db_connection = db_connection  # Recebe a conexão com o banco de dados


    def collect_data(self):
        """
        Collects specific data for system problems.

        Parameters: 
            tuple: containing the associated machine, the problem type, and a comment.
        """

        while True:
            clear_console()
            # Get Machine ID
            machine_name = input("Digite o nome da máquina de venda que deseja reportar ou 'cancelar' para cancelar: ")
            
            if machine_name == "cancelar":
                print("Operação cancelada.")    # Sair da tela de report
                time.sleep(1)
                return
            
            # Search for machines with that name
            vending_machine_dao = VendingMachineDAO(self.db_connection)

            machines = vending_machine_dao.get_vending_machines_by_name(machine_name)

            if not machines:
                print("Nenhuma máquina encontrada com esse nome. Tente novamente.")
                time.sleep(2)
                continue
            
            # Display the machines found in a DataFrame
            machine_data = {
                "Index": [],
                "Nome": [],
                "Localização": []
            }

            for index, machine in enumerate(machines, start=1):
                machine_data["Index"].append(index)
                machine_data["Nome"].append(machine.name)
                machine_data["Localização"].append(machine.location)

            df = pd.DataFrame(machine_data)
            print(df.to_string(index=False))

            # Confirm selection
            selected_machine = int(input("Digite o número da máquina que deseja reportar ou 0 para cancelar: "))

            if selected_machine == 0 or selected_machine > len(machines):
                print("Operação cancelada.")    # Sair da tela de avaliação
                time.sleep(2)
                return

            # Get the selected machine and save the ID
            selected_machine_id = machines[selected_machine - 1].id

            print("Opção selecionada.")
            time.sleep(1)

            # Get problem type
            while True:
                clear_console()
                for idx, problem in enumerate(MACHINE_PROBLEM_TYPES, 1):
                    print(f"{idx}. {problem}")

                try:
                    problem_choice = int(input("Digite o número do tipo de problema: "))

                    if problem_choice < 1 or problem_choice > len(MACHINE_PROBLEM_TYPES):
                        raise ValueError(f"Escolha um número válido entre 1 e {len(MACHINE_PROBLEM_TYPES)}.")

                    problem_type = MACHINE_PROBLEM_TYPES[problem_choice - 1]
                    break

                except ValueError as e:
                    print(f"Entrada inválida. {e}")
                    time.sleep(2)
            
            # Get comment
            while True:
                clear_console()
                # Comentário opcional ou obrigatório dependendo do tipo de problema
                if problem_choice != len(MACHINE_PROBLEM_TYPES):  # Se não for a opção 'Outro'
                    comment = input("Escreva um comentário sobre o problema (opcional, pressione Enter para pular): ")
                else:
                    comment = input("Escreva um comentário sobre o problema (obrigatório): ")

                if len(comment) > ProblemReport.MAX_COMMENT_LENGTH:
                    print(f"Comentário muito longo. Deve ter no máximo {ProblemReport.MAX_COMMENT_LENGTH} caracteres.")
                    time.sleep(2.5)
                elif not comment and problem_choice == len(MACHINE_PROBLEM_TYPES):  # Se 'Outro' e comentário vazio
                    print("Comentário é obrigatório para esse tipo de problema.")
                    time.sleep(2)
                else:
                    break

            return selected_machine_id, problem_type, comment


class SystemProblemReportStrategy(ProblemReportStrategy):
    """
    Estratégia para coletar dados relacionados a um problema de sistema.
    """

    def collect_data(self):
        """
        Coleta dados específicos para problemas do sistema.

        Parâmetros: 
            tuple: contendo a máquina associada (None se não houver máquina), o tipo de problema e o comentário.
        """
        
        machine_id = None  # Não há máquina associada
        while True:
            clear_console()
            print("Selecione o tipo de problema do sistema:")
            for idx, problem in enumerate(SYSTEM_PROBLEM_TYPES, 1):
                print(f"{idx}. {problem}")
            
            try:
                problem_choice = int(input("Digite o número do tipo de problema: "))
                
                if problem_choice < 1 or problem_choice > len(SYSTEM_PROBLEM_TYPES):
                    raise ValueError(f"Escolha um número válido entre 1 e {len(SYSTEM_PROBLEM_TYPES)}.")
                problem_type = SYSTEM_PROBLEM_TYPES[problem_choice - 1]
                break

            except ValueError as e:
                print(f"Entrada inválida. {e}")
                time.sleep(2)

        while True:
            clear_console()
            # Comentário opcional ou obrigatório dependendo do tipo de problema
            if problem_choice != len(SYSTEM_PROBLEM_TYPES):  # Se não for a opção 'Outro'
                comment = input("Escreva um comentário sobre o problema (opcional, pressione Enter para pular): ")
            else:
                comment = input("Escreva um comentário sobre o problema (obrigatório): ")

            if len(comment) > ProblemReport.MAX_COMMENT_LENGTH:
                print(f"Comentário muito longo. Deve ter no máximo {ProblemReport.MAX_COMMENT_LENGTH} caracteres.")
                time.sleep(2.5)
            elif not comment and problem_choice == len(SYSTEM_PROBLEM_TYPES):  # Se 'Outro' e comentário vazio
                print("Comentário é obrigatório para esse tipo de problema.")
                time.sleep(2)
            else:
                break

        return machine_id, problem_type, comment

    
def create_problem_report(customer_id, db_connection):
    """
    Create a problem report for a vending machine or the system.
    """

    while True:
        clear_console()
        print("~"*10, "Reportar Problema", "~"*10, "\n")

        print("1. Reportar problema do sistema")
        print("2. Reportar problema de máquina de vendas")
        print("0. Voltar")

        option = input("\n==> Escolha uma opção: ")

        if option == "0":
            print("Voltando...")
            time.sleep(0.5)
            break
        
        report_type = None
        if option == "1":
            report_type = "system"
            strategy = SystemProblemReportStrategy()
            break
        elif option == "2":
            report_type = "machine"
            strategy = MachineProblemReportStrategy(db_connection)
            break
        else:
            print("Opção inválida.")
            time.sleep(1)
            continue

    # Coletar dados usando a estratégia escolhida
    machine_id, problem_type, comment = strategy.collect_data()

    # Cria um novo relatório de problema usando o Factory Method
    problem_report = ProblemReportFactory.create_report(
        report_type,
        customer_id,
        problem_type,
        comment,
        machine_id
    )
    
    # Salva o relatório de problema no banco de dados
    problem_report_dao = ProblemReportDAO(db_connection)
    problem_report_dao.insert_problem_report(problem_report)
    
    print("==> Problema reportado com sucesso!")

    input("\nPressione qualquer tecla para voltar.")

