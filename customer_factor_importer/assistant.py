# Helper in creating and loading from The Customer Factor
# ========================================================
from customer_factor_importer import _loader as customerFactor
from customer_factor_importer import _database

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
    _database.create(data)

    # Creates a readable csv file.
    _database.writeCSV()


def query(question, args = None):
    """
    Query The Customer Factor database using SQLite queries.

    Args:
        question (str): The SQLite query.
        args (array): A list of arguments to include in the query.

    Returns:
        the response from The Customer Factor database.
    """
    return _database.ask(question, args)


def print_query(question, args = None):
    """
    Query The Customer Factor database using SQLite queries and print directly to console.

    Args:
        question (str): The SQLite query.
        args (array): A list of arguments to include in the query.

    Returns:
        the response from The Customer Factor database.
    """
    response =  _database.ask(question, args)
    if response:
        for r in response:
            print(r)

    return response


#=================================================================================
#   COMMON FUNCTIONS USED BY THE REST OF THE PROGRAM
#=================================================================================
def previewFile(fileName = DEFAULT_FILE_NAME):
    """
    Retrieves the RAW file data without building the database

    """
    customerFactor.init(fileName)
    return customerFactor.fetchData()


def listEmployees():
    question = "SELECT DISTINCT employee FROM {}".format(_database.tbl_jobHistory)
    return _database.ask(question)


def searchForCustomers(customersName):
    question = "SELECT * FROM CUSTOMERS WHERE name LIKE '{}%'".format(customersName)
    return _database.ask(question)

    
def getActiveCustomers():
        question = """
            SELECT *
            FROM CUSTOMERS
            WHERE active_status = 1
            """ 
        return _database.ask(question)