import json
import cf_loader as customerFactor
import cf_interpreter as inter
import db_generator as database
import resources as r
from datetime import datetime
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
    # activeJobHistory = database.ask(ACTIVE_JOB_HISTORY)
    # employees = ['Jose Perez', 'Justin Smith', 'Devony Dettman']

    # filteredList = []

    # for line in activeJobHistory:
    #     if any(employee in line for employee in employees):
    #         filteredList.append(line)

    activeCustomers = getActiveCustomers()

    for customer in activeCustomers:
        customer_id = customer[0]
        customerName = customer[1]
        jobHistory = getCustomerHistory(customer_id)

        for job in jobHistory:
            print("{} -> {}".format(customerName, job))
        

    # printRes(filteredList)

def getCustomerHistory(customer_id):
    today = datetime.today().date()
    formatted_date = today.strftime('%m/%d/%y')

    currentDate = datetime.today().date()
    print(currentDate)
    # retrieve rows from the JOB_HISTORY table for the given customer_id
    return database.ask('SELECT * FROM JOB_HISTORY WHERE customer_id = ? AND job_date < ? LIMIT 12', (customer_id, formatted_date))

# Frequency is a integer represeninting the amount of days we do a job
# Only filters out active jobs
def filterByFrequency(frequency = None):
    if not frequency:
        query = """
            SELECT c.name, j.*
            FROM JOB_HISTORY j
            INNER JOIN CUSTOMERS c ON c.customer_id = j.customer_id AND c.active_status = 1
            """
        return database.ask(query)
    
    else:
        # Daily
        if frequency > 0 and frequency < 3:
            params = (0,3)
        # weekly
        elif frequency >= 3 and frequency < 10:
            params = (3, 10)
        # two weeks
        elif frequency >= 10 and frequency < 18:
            params = (10, 18)
        # three weeks
        elif frequency >= 18 and frequency < 25:
            params = (18, 25)
        # monthly
        elif frequency >= 25 and frequency < 40:
            params = (25, 40)
        # 6 weeks
        elif frequency >= 40 and frequency < 48:
            params = (40, 48)
        # bi-monthly
        elif frequency >= 48 and frequency < 75:
            params = (48, 75)
        # quarterly
        elif frequency >= 80 and frequency < 130:
            params = (80, 130)
        # bi-yearly
        elif frequency >= 130 and frequency < 250:
            params = (130, 250)
        # Yearly
        elif frequency >= 250 and frequency < 500:
            params = (250, 500)

        # bi-yearly
        elif frequency >= 500 and frequency < 800:
            params = (500, 800)

        # Select the jobs with a job frequency in the specified range
        query = """
        SELECT c.name, j.*
        FROM CUSTOMERS c
        INNER JOIN JOB_HISTORY j ON c.customer_id = j.customer_id
        WHERE j.job_frequency >= ? AND j.job_frequency <= ? AND c.active_status = 1
        """

        return database.ask(query, args=params)


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
    