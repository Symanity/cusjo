import json
import cf_loader as customerFactor
import cf_interpreter as inter
import db_generator as database
import resources as r
# import os
import sys


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
    question = """
        SELECT j.*
        FROM CUSTOMERS c
        INNER JOIN JOB_HISTORY j ON c.customer_id = j.customer_id
        WHERE j.employee = ''
        """

    print('[STATUS] asking, {}'.format(question))

    res = database.ask(question)
    printRes(res)



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
        printRes(searchForCustomers(str(sys.argv[2])))

    elif sys.argv[1] == "print":
        if len(sys.argv) > 2:
            if sys.argv[2] == "employees":
                printRes(showEmployees())

            elif sys.argv[2] == "active_customers":
                printRes(getActiveCustomers())

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
    