from datetime import datetime
import uuid


class ProblemReport:
    """
    Class to represent a reported problem in the system.
    """

    def __init__(self, author_id, problem_type, comment=None, machine_id=None):
        """
        Initialize the problem report with details about the problem.

        Parameters:
            author_id (int): ID of the user reporting the problem.
            problem_type (str): Type of the problem (e.g., "System", "Machine").
            comment (str, optional): Optional comment providing more details about the problem.
            machine_id (int, optional): ID of the machine (if the problem is related to a specific machine). None if it's a system problem.
        """
        self.id = uuid.uuid4()                  # Unique ID for the report
        self.author_id = author_id
        self.machine_id = machine_id            # Can be None if it's a system problem
        self.problem_type = problem_type
        self.comment = comment
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        """
        Return a string representation of the problem report.
        """
        if self.machine_id:
            return f"Report by User {self.author_id} for Machine {self.machine_id}: {self.problem_type} - {self.comment}"
        else:
            return f"Report by User {self.author_id} for System: {self.problem_type} - {self.comment}"

