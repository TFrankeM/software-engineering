import uuid

class FavoriteMachine:
    """
    Class representing a favorite vending machine of a user.
    """
    def __init__(self, user_id, machine_id):
        """
        Initialize a new favorite machine instance.

        Parameters:
            user_id (str): The ID of the user who favorited the vending machine.
            machine_id (str): The ID of the vending machine that was favorited.
        """
        self.id = uuid.uuid4()  # Unique ID for the favorite record
        self.user_id = user_id
        self.machine_id = machine_id

    def __repr__(self):
        return f"<FavoriteMachine(id={self.id}, user_id={self.user_id}, machine_id={self.machine_id})>"
