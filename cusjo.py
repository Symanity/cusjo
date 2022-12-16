import cf_loader as customerFactor
import db_generator as database
from datetime import datetime
import sys
import services_attributor as WindowMagic

# # Import the required modules
# import sqlite3

# # Connect to the database
# conn = sqlite3.connect('my_database.db')

# # Define a dictionary to store the data
# data = defaultdict(list)

# # Query the CUSTOMERS table
# query = "SELECT * FROM CUSTOMERS"
# customers = conn.execute(query).fetchall()

# # Loop over the customers
# for customer in customers:
#     # Check if the customer is active
#     if customer[6]:
#         # Query the JOB_HISTORY table
#         query = "SELECT * FROM JOB_HISTORY WHERE customer_id = ?"
#         jobs = conn.execute(query, (customer[0],)).fetchall()

#         # Group the jobs by job_date
#         jobs_by_date = defaultdict(list)
#         for job in jobs:
#             jobs_by_date[job[1]].append(job)

#         # Add the data to the dictionary
#         data[customer[1]] = jobs_by_date

# # Print the dictionary
# print(data)

# # Close the connection
# conn.close()



# SQL Queries () 
#### [** ONLY DO FROM LAST 12 JOBS ***]
#### TODO: Consider Job types being done on the same day
#### TODO: Jobs may have two jobTypes done on the same day. This job structure may have the same duration.

# 1. Filter by date range
# 2. filter by employee
# 3. filter by frequency
# 4. search by name

SAMPLE_FILE = "CF_exported.csv"

ACTIVE_JOB_HISTORY = """
        SELECT c.name, j.*
        FROM JOB_HISTORY j
        INNER JOIN CUSTOMERS c ON c.customer_id = j.customer_id
        WHERE c.active_status = 1
        """

EMPLOYEE_JOB_HISTORY = ''' 
    SELECT * 
    FROM CUSTOMERS 
    INNER JOIN JOB_HISTORY ON CUSTOMERS.customer_id = JOB_HISTORY.customer_id 
    WHERE JOB_HISTORY.employee = 'Jose Perez' '''

def playground():
    # activeJobHistory = database.ask(ACTIVE_JOB_HISTORY)
    # employees = ['Jose Perez', 'Justin Smith', 'Devony Dettman']

    # filteredList = []

    # for line in activeJobHistory:
    #     if any(employee in line for employee in employees):
    #         filteredList.append(line)

    # iePacific = serv.OurServiceOf(731)

    # serv.evaluate(iePacific)
    # serv.evaluate(traderJoes)
    activeCustomers = getActiveCustomers()
    for customer in activeCustomers:
        id = customer[0]
        customerName = customer[1]
        theService = WindowMagic.ServiceOf(id)

        print(theService)

        # print("\n")

        # print(theJob)


def printRes(response = None, query=None):
    if response:
        for r in response:
            print(r)

    else:
        print('[STATUS] ... no response')


# Returns RAW file data without building the database
def previewFile(fileName):
    fileName = "CF_exported.csv"
    customerFactor.init(fileName)
    return customerFactor.fetchData()
    

# Builds the CF_sql database
def build(fileName):
    customerFactor.init(fileName)
    data = customerFactor.fetchData()
    database.create(data)


def showEmployees():
    question = "SELECT DISTINCT employee FROM {}".format(database.tbl_jobHistory)
    return database.ask(question)

def searchForCustomers(customersName):
    question = "SELECT * FROM CUSTOMERS WHERE name LIKE '{}%'".format(customersName)
    return database.ask(question)


def getActiveCustomers():
        question = """
            SELECT *
            FROM CUSTOMERS
            WHERE active_status = 1
            """ 
        return database.ask(question)

if len(sys.argv) > 1:
    theCase = sys.argv[1]

    if str(sys.argv[1]) == "build":
        if len(sys.argv) > 2:
            try:
                build(str(sys.argv[2]))
            except:
                print("[FATAL-ERROR] invalid file")

        else:
            build(SAMPLE_FILE)

    elif sys.argv[1] == "search":
        if len(sys.argv) > 2:
            if(sys.argv[2] == "history"):
                printRes(database.getCustomerHistory(str(sys.argv[3])))

            else:
                print("Searching ....")
                printRes(searchForCustomers(str(sys.argv[2])))

    elif sys.argv[1] == "print":
        if len(sys.argv) > 2:
            if sys.argv[2] == "employees":
                printRes(showEmployees())

            elif sys.argv[2] == "active_customers":
                printRes(getActiveCustomers())

            elif sys.argv[2] == "customers":
                query = """ SELECT * FROM {} """.format(database.tbl_Customers)
                res = database.ask(query)
                printRes(res)

            elif sys.arg[2] == "job_history":
                query = """ SELECT * FROM {} """.format(database.tbl_jobHistory)
                res = database.ask(query)
                printRes(res)
    else:
        print('[ERROR] command not recognized')

else:
    playground()


# Usefull snippets
    # Create SQLite database/tables
    # database.create(data)

    # database.printTable(database.tbl_Customers, database.CF_db)

    # customers = customerFactor.getCustomers()
    # for customer in customers:
    #     if customer.isActive():
    #         print("[ACTIVE] {}".format(customer.name))
    #     else:
    #         print("[-] {}".format(customer.name))



# QUESTION HISTORY
    # ** show me the list of Customers where Jose is the employee
    # question = ''' SELECT * FROM CUSTOMERS INNER JOIN JOB_HISTORY ON CUSTOMERS.customer_id = JOB_HISTORY.customer_id WHERE JOB_HISTORY.employee = 'Jose Perez' '''
    