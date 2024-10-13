from datetime import datetime
import unittest
import sys, os

# Corrigir caminhos
# adding src to the system path
"""
    os.path.dirname(__file__): diretório do arquivo atual (A)
    os.path.join(A, '../../src/classes'): combina o diretório atual com o caminho relativo '../../src/classes' (B)
    os.path.abspath(B): converte o caminho relativo '../../src/classes' em um caminho absoluto (C)
    sys.path.insert(0, C): insere o caminho absoluto da pasta src no início da lista sys.path (uma lista de diretórios que o Python procura quando importa um módulo) 
"""
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src/classes")))
from problem_report import ProblemReport  # Importe a classe do arquivo onde está a classe original


class TestProblemReport(unittest.TestCase):
    def setUp(self):
        """
            Set up a basic environment for each test. Create a sample problem report.
        """
        self.author_id = 101
        self.system_problem_type = "Erro de login"
        self.machine_problem_type = "Produto esgotado"
        self.comment = "Detalhes adicionais sobre o problema"
        self.machine_id = 202


    def test_system_report_creation(self):
        """
        Test the creation of a problem report for a system issue (no machine_id).
        """
        report = ProblemReport(author_id=self.author_id, problem_type=self.system_problem_type)
        
        self.assertIsNotNone(report.id)                                     # UUID should be automatically created
        self.assertEqual(report.author_id, self.author_id)
        self.assertEqual(report.problem_type, self.system_problem_type)
        self.assertIsNone(report.machine_id)                                # No machine ID should be set for system issues
        self.assertIsNone(report.comment)                                   # Comment should be None if not provided


    def test_machine_report_creation(self):
        """
        Test the creation of a problem report for a machine-related issue (with machine_id).
        """
        report = ProblemReport(author_id=self.author_id, problem_type=self.machine_problem_type, machine_id=self.machine_id)
        
        self.assertIsNotNone(report.id)                                     # UUID should be automatically created
        self.assertEqual(report.author_id, self.author_id)
        self.assertEqual(report.problem_type, self.machine_problem_type)
        self.assertEqual(report.machine_id, self.machine_id)                # machine_id should be set
        self.assertIsNone(report.comment)                                   # Comment should be None if not provided


    def test_report_with_comment(self):
        """
        Test the creation of a problem report with an optional comment.
        """
        report = ProblemReport(author_id=self.author_id, problem_type=self.system_problem_type, comment=self.comment)
        
        # Assert that the comment is correctly set
        self.assertEqual(report.comment, self.comment)


    def test_str_method_for_system(self):
        """
        Test the __str__ method for a system problem report.
        """
        report = ProblemReport(author_id=self.author_id, problem_type=self.system_problem_type, comment=self.comment)
        expected_str = f"Report by User {self.author_id} for System: {self.system_problem_type} - {self.comment}"
        self.assertEqual(str(report), expected_str)


    def test_str_method_for_machine(self):
        """
        Test the __str__ method for a machine-related problem report.
        """
        report = ProblemReport(author_id=self.author_id, problem_type=self.machine_problem_type, comment=self.comment, machine_id=self.machine_id)
        expected_str = f"Report by User {self.author_id} for Machine {self.machine_id}: {self.machine_problem_type} - {self.comment}"
        self.assertEqual(str(report), expected_str)


    def test_timestamp_is_generated(self):
        """
        Test that the timestamp is correctly generated when a report is created.
        """
        report = ProblemReport(author_id=self.author_id, problem_type=self.system_problem_type)
        self.assertIsNotNone(report.timestamp)  # The timestamp should not be None
        
        # Ensure the timestamp is close to the current time (within the same minute)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertEqual(report.timestamp[:16], current_time[:16])  # Comparing up to minutes to avoid precision issues


# Run the tests
if __name__ == "__main__":
    unittest.main()
