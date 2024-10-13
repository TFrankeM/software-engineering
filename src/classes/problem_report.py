from datetime import datetime
import uuid


class ProblemReport:
    """
    Class to represent a reported problem in the system or with a specific machine.
    """

    # Tipos de problema pré-definidos
    # Novas opções podem ser adicionados futuramente a medida que a complexidade da implementação cresce.
    SYSTEM_PROBLEM_TYPES = [
        "Erro de login",
        "Página lenta",
        "Erro de carregamento",
        "Outro"
    ]
    
    MACHINE_PROBLEM_TYPES = [
        "Produto esgotado",
        "Máquina fora de serviço",
        "Erro no pagamento",
        "Outro"
    ]

    def __init__(self, author_id, problem_type, comment=None, machine_id=None):
        """
        Initialize the problem report with details about the problem.

        Parameters:
            author_id (int): ID of the user reporting the problem.
            problem_type (str): Type of the problem, chosen from predefined options.
            comment (str, optional): Optional comment providing more details about the problem if the type is "Outro".
            machine_id (int, optional): ID of the machine (if the problem is related to a specific machine). None if it's a system problem.

        Raises:
            ValueError: If the problem_type is invalid or if "Outro" is selected but no comment is provided.
        """
        self.id = uuid.uuid4()              # Unique ID for the report
        self.author_id = author_id
        self.machine_id = machine_id
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if machine_id is None:
            self._validate_system_problem_type(problem_type)
        else:
            self._validate_machine_problem_type(problem_type)

        self.problem_type = problem_type
        self.comment = self._validate_comment(comment, problem_type)
    

    def _validate_system_problem_type(self, problem_type):
        """
        Validate the system problem type.

        Raises:
            ValueError: If the problem_type is not in the predefined system problem types.
        """
        if problem_type not in self.SYSTEM_PROBLEM_TYPES:
            raise ValueError(f"Invalid system problem type: {problem_type}. Choose from: {self.SYSTEM_PROBLEM_TYPES}")


    def _validate_machine_problem_type(self, problem_type):
        """
        Validate the machine problem type.

        Raises:
            ValueError: If the problem_type is not in the predefined machine problem types.
        """
        if problem_type not in self.MACHINE_PROBLEM_TYPES:
            raise ValueError(f"Invalid machine problem type: {problem_type}. Choose from: {self.MACHINE_PROBLEM_TYPES}")


    def _validate_comment(self, comment, problem_type):
        """
        Validate the comment. A comment is required if "Outro" is chosen as the problem type.
        
        Raises:
            ValueError: If the problem type is "Outro" and no comment is provided.
        """
        if problem_type == "Outro" and (not comment or comment.strip() == ""):
            raise ValueError("A comment is required when 'Outro' is selected as the problem type.")
        
        # Return the comment or None if no comment is needed
        return comment if problem_type == "Outro" else None


    def __str__(self):
        """
        Return a string representation of the problem report.
        """
        if self.machine_id:
            return f"Report by User {self.author_id} for Machine {self.machine_id}: {self.problem_type} - {self.comment or 'No comment'}"
        else:
            return f"Report by User {self.author_id} for System: {self.problem_type} - {self.comment or 'No comment'}"

