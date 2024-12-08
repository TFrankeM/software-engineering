import sys, os

from notification_dao import NotificationDAO

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from notification import Notification

class Subject:
    def __init__(self):
        pass

    def create_table(self):
        pass

    def attach(self, favorite):
        pass

    def detach(self, user_id, favorite_id):
        pass

    def get_observers(self):
        pass

    def notify(self):
        pass

    def send_notification(self, user_id, message):
        pass


class FavoriteProductDAO(Subject):
    """
    Data Access Object (DAO) for managing favorite products in the database.
    """

    def __init__(self, db_connection):
        self.connection = db_connection
        

    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorite_products (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                product_id TEXT NOT NULL
            );
        """)
        self.connection.commit()


    def attach(self, favorite_product):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO favorite_products (id, user_id, product_id)
            VALUES (?, ?, ?)
        """, (str(favorite_product.id), favorite_product.user_id, favorite_product.product_id))
        self.connection.commit()


    def detach(self, user_id, product_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            DELETE FROM favorite_products WHERE user_id = ? AND product_id = ?
        """, (user_id, product_id))
        self.connection.commit()


    def is_favorite_product(self, user_id, product_id):
        """
        Checks if a product is in a user's favorites list.

        Parameters:
            user_id (str): The user ID.
            product_id (str): The product ID.

        Returns:
            bool: Returns True if the product is in the favorites list, otherwise False.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT 1 FROM favorite_products WHERE user_id = ? AND product_id = ? LIMIT 1
        """, (user_id, product_id))
        
        result = cursor.fetchone()

        return result is not None
    

    def get_observers(self, product_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT user_id FROM favorite_products WHERE product_id = ?
        """, (product_id,))
        observers = cursor.fetchall()
        
        return [observer[0] for observer in observers]


    def notify_observers(self, product_id, message):
        observers = self.get_observers(product_id)
        for observer in observers:
            self.send_notification(observer, message)


    def send_notification(self, user_id, message):
        """
        Sends a notification to a user.
        
        Parameters:
            user_id (str): The user ID.
            message (str): The notification message.
        """
        notification = Notification(user_id=user_id, message=message)
        notification_dao = NotificationDAO(self.connection)
        notification_dao.insert_notification(notification)

class FavoriteMachineDAO(Subject):
    """
    Data Access Object (DAO) for managing favorite machines in the database.
    """

    def __init__(self, db_connection):
        self.connection = db_connection


    def create_table(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS favorite_machines (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                machine_id TEXT NOT NULL
            );
        """)
        self.connection.commit()


    def attach(self, favorite_machine):
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO favorite_machines (id, user_id, machine_id)
            VALUES (?, ?, ?)
        """, (str(favorite_machine.id), favorite_machine.user_id, favorite_machine.machine_id))
        self.connection.commit()


    def detach(self, user_id, machine_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            DELETE FROM favorite_machines WHERE user_id = ? AND machine_id = ?
        """, (user_id, machine_id))
        self.connection.commit()


    def is_favorite_machine(self, user_id, machine_id):
        """
        Checks if a vending machine is in a user's favorites list.

        Parameters:
            user_id (str): The user ID.
            machine_id (str): The ID of the vending machine.

        Returns:
            bool: Returns True if the machine is in the favorites, otherwise False.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT 1 FROM favorite_machines WHERE user_id = ? AND machine_id = ? LIMIT 1
        """, (user_id, machine_id))
        
        result = cursor.fetchone()

        return result is not None
    

    def get_observers(self, machine_id):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT user_id FROM favorite_machines WHERE machine_id = ?
        """, (machine_id,))
        observers = cursor.fetchall()
        return [observer[0] for observer in observers]


    def notify_observers(self, machine_id, message):
        """
        Notifies all users who have the machine as a favorite.
        
        Parameters:
            machine_id (str): The machine ID.
            message (str): The notification message to be sent.
        """
        observers = self.get_observers(machine_id)
        for observer in observers:
            self.send_notification(observer, message)


    def send_notification(self, user_id, message):
        """
        Sends a notification to a user.
        
        Parameters:
            user_id (str): The user ID.
            message (str): The notification message.
        """
        notification = Notification(user_id=user_id, message=message)
        notification_dao = NotificationDAO(self.connection)
        notification_dao.insert_notification(notification)

