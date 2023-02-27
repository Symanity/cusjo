from datetime import datetime
from src.window_magic.databasing import _complete_database_struct as database
from src.window_magic.objects.job import Job

job_table = database.JOB_HISTORY_TABLE
#=================================================================================
#   DEFAULT FUNCTIONS
#=================================================================================
def build_database(job_list):
    """
    Build a database from a list of jobs

    Args:
        job_list (list): The job list as compiled from the converter.

    Returns:
        None
    """

    # creates the database from the data
    database.create(job_list)

    # Creates a readable csv file.
    database.writeCSV()


def query(question, args = None):
    """
    Query The Window Magic database using SQLite queries.

    Args:
        question (str): The SQLite query.
        args (tuble): A list of arguments to include in the query.

    Returns:
        the response from The Window Magic database.
    """
    return database.ask(question, args)


def print_query(question, args = None):
    """
    Query The Window Magic database using SQLite queries and print directly to console.

    Args:
        question (str): The SQLite query.
        args (array): A list of arguments to include in the query.

    Returns:
        the response from The Window Magic database.
    """
    response =  database.ask(question, args)
    if response:
        for r in response:
            print(r)

    return response


#=================================================================================
#   COMMON FUNCTIONS USED BY THE REST OF THE PROGRAM
#=================================================================================
def listEmployees():
    question = "SELECT DISTINCT employee FROM {}".format(database.JOB_HISTORY_TABLE)
    return database.ask(question)


def get_customer_address(customer_id: int):
    return database.askOne("SELECT address FROM ? customer_id = ?", (database.JOB_HISTORY_TABLE, customer_id,))


def list_customers():
    """
    Execute a query to retrieve all unique customers
    """
    queryString = f"SELECT DISTINCT customer_id, customer_name FROM {job_table}"
    return query(queryString)


def get_completed_jobs(customer_id):
    queryString = f"SELECT * FROM {job_table} WHERE customer_id = ? AND price > 0 AND duration > 0"
    return query(queryString, (customer_id,))