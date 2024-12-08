import os, sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from notification import Notification

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from notification_dao import NotificationDAO

def clear_console():
    """
    Console clearing function, (Windows and Unix-based).
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def view_notification(customer_id, db_connection):
    """
    Function to view a customer's notifications.

    Parameters:
    customer_id (str): The ID of the customer whose notifications will be displayed.
    db_connection (sqlite3.Connection): Connection to the database.
    """
    notification_dao = NotificationDAO(db_connection)  # Instanciando a classe de persistência de notificações
    notifications_df = notification_dao.get_notifications_by_user(customer_id)

    clear_console()

    # Verifica se há notificações
    if notifications_df.empty:
        print("\n>>> Você não tem notificações.<<")
    else:
        print("\n~" * 10, "Suas Notificações", "~" * 10, "\n")
        print(notifications_df.to_string(index=False))  # Exibe as notificações em formato tabular
        print("\n~" * 10, "~" * 10)

    # Espera que o usuário pressione Enter para continuar
    input("\n==> Pressione Enter para voltar ao menu.")
