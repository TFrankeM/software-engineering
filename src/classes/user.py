import uuid
import bcrypt

class User:
    def __init__(self, name, email, password, address=None, anonymous_profile=True, coins = 0):
        """Initialize a new User instance with the given attributes.

        Args:
            name (str): The user's name. This is a protected attribute.
            email (str): The user's email address. This is a protected attribute.
            password (str): The user's password, which will be hashed.
            address (str, optional): The user's address. Defaults to None.
        """
        self.__user_id = uuid.uuid4()  # Unique user ID generated using UUID
        self._name = name                # Protected name attribute
        self._email = email              # Protected email attribute
        self.__password = self._hash_password(password)  # Private hashed password
        self.__address = address          # Private address attribute
        self.__profile_picture_path = "../imgs/default.png"  # Default profile picture path
        self.anonymous_profile = anonymous_profile  # Public anonymous profile attribute
        self.coins = coins #number of coins

    @property
    def user_id(self):
        """Read-only property for the user's unique ID."""
        return self.__user_id
    
    @property
    def name(self):
        """Property for the user's name (protected)."""
        return self._name
    
    @property
    def email(self):
        """Property for the user's email (protected)."""
        return self._email
    
    @property
    def address(self):
        """Property for the user's address (private)."""
        return self.__address
    
    @property
    def profile_picture_path(self):
        """Property for the user's profile picture path (private)."""
        return self.__profile_picture_path
    
    def _hash_password(self, password):
        """
        Hash the password using bcrypt.

        Args:
            password (str or bytes): The password to be hashed.

        Returns:
            str: The hashed password.
        """
        if isinstance(password, str):
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return password
    
    def verify_password(self, password):
        """Verify the password using bcrypt.

        Args:
            password (str): The password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bcrypt.checkpw(password.encode('utf-8'), self.__password)  # Use self.__password to check
    
    @property
    def change_name(self):
        """Setter for changing the user's name (protected)."""
        return self._name

    @change_name.setter
    def change_name(self, new_name):
        """Change the user's name.

        Args:
            new_name (str): The new name for the user.
        """
        self._name = new_name
        
    @property
    def change_email(self):
        """Setter for changing the user's email (protected)."""
        return self._email
    
    @change_email.setter
    def change_email(self, new_email):
        """Change the user's email.

        Args:
            new_email (str): The new email for the user.
        """
        self._email = new_email
    
    @property
    def change_address(self):
        """Setter for changing the user's address (private)."""
        return self.__address

    @change_address.setter
    def change_address(self, new_address):
        """Change the user's address.

        Args:
            new_address (str): The new address for the user.
        """
        self.__address = new_address

    @property
    def change_password(self):
        """Setter for changing the user's password (private)."""
        return self.__password

    @change_password.setter
    def change_password(self, new_password):
        """Change the user's password.

        Args:
            new_password (str): The new password for the user.
        """
        self.__password = self._hash_password(new_password)

    @property
    def change_profile_picture_path(self):
        """Setter for changing the user's profile picture path (private)."""
        return self.__profile_picture_path

    @change_profile_picture_path.setter
    def change_profile_picture_path(self, new_path):
        """Change the user's profile picture path.

        Args:
            new_path (str): The new path for the user's profile picture.
        """
        self.__profile_picture_path = new_path



class UserFactory:
    @staticmethod
    def create_user(user_type, name, email, password, address=None, anonymous_profile=True, coins=0):
        """
        Factory method to create users based on the given type.

        Args:
            user_type (str): The type of user to create ('Administrator', 'Customer', 'Seller').
            name (str): The name of the user.
            email (str): The email of the user.
            password (str): The password of the user.
            address (str, optional): The address of the user. Defaults to None.
            anonymous_profile (bool, optional): If the user's profile is anonymous. Defaults to True.

        Returns:
            User: An instance of the requested user type.

        Raises:
            ValueError: If the user type is invalid.
        """
        if user_type == "Administrator":
            from administrator import Administrator
            return Administrator(name, email, password, address, anonymous_profile)
        elif user_type == "Customer":
            from customer import Customer
            return Customer(name, email, password, address, anonymous_profile, coins)
        elif user_type == "Seller":
            from seller import Seller
            return Seller(name, email, password, address, anonymous_profile, coins)
        else:
            raise ValueError(f"Invalid user type: {user_type}")
