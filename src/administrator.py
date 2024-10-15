from user import User

class Administrator(User):
    """
    A class representing an administrator in the system.
    """
    def __init__(self, name, email, address, password, profile_picture_path=None, anonymous_profile=True):
        """
        Initialize a new administrator.

        Parameters:
            name (str): The name of the administrator.
            email (str): The email address of the administrator.
            address (str): The address of the administrator.
            password (str): The password of the administrator.
            profile_picture_path (str): The path to the administrator's profile picture.
            anonymous_profile (bool): Whether the administrator's profile is anonymous (default is True).
        """
        super().__init__(name, email, address, password, profile_picture_path, anonymous_profile)
        self.vending_machines = [] # List of vending machines managed by the administrator.
        
    
            

