# Helper in creating and loading from The Customer Factor
# ========================================================
from customer_factor_importer import loader as customerFactor
from customer_factor_importer import database

DEFAULT_FILE_NAME = "CF_exported.csv"


#=================================================================================
#   DEFAULT FUNCTIONS
#=================================================================================

def build(customer_factor_exported_file = DEFAULT_FILE_NAME):
    """
    Build a database from a customer file and create a readable CSV file.

    Args:
        customer_factor_exported_file (str): The name of the file of exported customers from The Customer Factor. 
        Defaults to "CF_exported.csv".

    Returns:
        None
    """
        
    # Specify which Customer File is to be used.
    customerFactor.init(customer_factor_exported_file)
    
    # Reads the data from the customer factor
    data = customerFactor.fetchData()

    # creates the database from the data
    database.create(data)

    # Creates a readable csv file.
    database.writeCSV()


def query(question, args = None):
    """
    Query The Customer Factor database using SQLite queries.

    Args:
        question (str): The SQLite query.
        args (array): A list of arguments to include in the query.

    Returns:
        the response from The Customer Factor database.
    """
    return database.ask(question, args)


def print_query(question, args = None):
    """
    Query The Customer Factor database using SQLite queries and print directly to console.

    Args:
        question (str): The SQLite query.
        args (array): A list of arguments to include in the query.

    Returns:
        the response from The Customer Factor database.
    """
    response =  database.ask(question, args)
    if response:
        for r in response:
            print(r)

    return response


#=================================================================================
#   COMMON FUNCTIONS USED BY THE REST OF THE PROGRAM
#=================================================================================