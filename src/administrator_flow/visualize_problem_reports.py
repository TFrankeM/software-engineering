import time
import os

def clear_console():
    """
    Console clearing function, (just works in Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def visualize_problem_reports(db_connection):
    """
    Visualize the problem reports made by customers.
    """
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM problem_reports")
    reports = cursor.fetchall()

    clear_console()
    
    if not reports:
        print(">>> Nenhum reporte de problema encontrado. <<<")
        time.sleep(1.5)

    else:
        print(f"{'~'*10} Problemas reportados {'~'*10}\n")

        for report in reports:
            print(f"ID do reporte: {report[0]}")
            print(f"ID do autor (customer_id): {report[1]}")
            print(f"Tipo de Problema: {report[2]}")
            print(f"Descrição: {report[3]}")
            print(f"ID da máquina: {report[4]}")
            print(f"Data e Hora: {report[5]}")
            print("-"*50)
        
        input("\nPressione qualquer tecla para voltar.")

    cursor.close()