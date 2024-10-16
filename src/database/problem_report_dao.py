import sqlite3
import sys, os
from datetime import datetime
import uuid

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../classes")))
from problem_report import ProblemReport


class ProblemReportDAO:
    """
    Data Access Object (DAO) for managing problem reports in the database.
    """

    def __init__(self, db_connection):
        """
        Initialize the ProblemReportDAO with a database connection.

        Parameters:
            db_connection (sqlite3.Connection): A connection object to the SQLite database.
        """
        self.connection = db_connection

    def create_table(self):
        """
        Create the problem_reports table in the database if it doesn't already exist.
        """
        cursor = self.connection.cursor()

        # Create the problem_reports table with foreign keys for author and machine (if applicable)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS problem_reports (
                id TEXT PRIMARY KEY,
                author_id TEXT NOT NULL,
                problem_type TEXT NOT NULL,
                comment TEXT,
                machine_id TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (author_id) REFERENCES usuarios(id) ON DELETE CASCADE,
                FOREIGN KEY (machine_id) REFERENCES vending_machines(id) ON DELETE CASCADE
            );
        ''')

        self.connection.commit()

    def insert_problem_report(self, problem_report):
        """
        Insert a problem report into the database.

        Parameters:
            problem_report (ProblemReport): A ProblemReport object to be inserted into the database.
        """
        cursor = self.connection.cursor()

        # Insert problem report details
        cursor.execute('''
            INSERT INTO problem_reports (id, author_id, problem_type, comment, machine_id, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (str(problem_report.id), problem_report.author_id, problem_report.problem_type,
              problem_report.comment, problem_report.machine_id, problem_report.timestamp))

        self.connection.commit()

    def get_problem_report_by_id(self, report_id):
        """
        Retrieve a problem report from the database by its ID.

        Parameters:
            report_id (str): The ID of the problem report to retrieve.

        Returns:
            ProblemReport: A ProblemReport object with its associated details.
        """
        cursor = self.connection.cursor()

        # Fetch the problem report details
        cursor.execute('''
            SELECT * FROM problem_reports WHERE id = ?
        ''', (report_id,))
        report_data = cursor.fetchone()

        if report_data is None:
            return None

        # Create and return the ProblemReport object
        problem_report = ProblemReport(
            author_id=report_data[1],
            problem_type=report_data[2],
            comment=report_data[3],
            machine_id=report_data[4]
        )
        problem_report.id = report_data[0]
        problem_report.timestamp = report_data[5]
        return problem_report

    def get_reports_by_author_id(self, author_id):
        """
        Retrieve all problem reports created by a specific author from the database.

        Parameters:
            author_id (str): The ID of the author whose reports are to be retrieved.

        Returns:
            list: A list of ProblemReport objects associated with the author.
        """
        cursor = self.connection.cursor()

        # Fetch the problem reports where the author_id matches
        cursor.execute('''
            SELECT * FROM problem_reports WHERE author_id = ?
        ''', (author_id,))
        rows = cursor.fetchall()

        reports = []

        # Create ProblemReport objects for each row
        for row in rows:
            problem_report = ProblemReport(
                author_id=row[1],
                problem_type=row[2],
                comment=row[3],
                machine_id=row[4]
            )
            problem_report.id = row[0]
            problem_report.timestamp = row[5]
            reports.append(problem_report)

        return reports

    def delete_problem_report(self, report_id):
        """
        Delete a problem report from the database by its ID.

        Parameters:
            report_id (str): The ID of the problem report to delete.
        """
        cursor = self.connection.cursor()

        # Delete the problem report
        cursor.execute('DELETE FROM problem_reports WHERE id = ?', (report_id,))

        self.connection.commit()
