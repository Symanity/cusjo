# Expected post-case:
#   TABLE1: CUSTOMERS
#   Row: Customer id, customer name, company name, customer address, date added, cType

#   TABLE2: Job History
#   Row: Customer Id, jobType, jobPrice, jobDate, employee, duration, invoice 

import cj_interpreter as interpreter
import json
import resources as r

import sqlite3

DATE_FORMAT = '%m/%d/%y'
mCustomerDb = "Customers.db"
mJobDb = "JobHistory.db"

def create(data):
    # Create necessary tables
    __createCustomerTable()
    __createJobTable()

    __generateDB(data)
    printTable("JOB_HISTORY", mJobDb)


def __generateDB(data):
    customers_connection = sqlite3.connect(mCustomerDb)
    customers_cursor = customers_connection.cursor()

    job_connection = sqlite3.connect(mJobDb)
    job_cursor = job_connection.cursor()

    for customerData in data:
        customerJson =  json.loads(customerData)
        customerEvaluator = interpreter.Evaluator(customerJson)

        services = customerEvaluator.services
        
        # Insert Customer Data row into Customers.db
        customers_cursor.execute("INSERT INTO CUSTOMERS VALUES(?,?,?,?,?,?)", (customerJson["id"], customerJson["name"], customerJson["company"], customerJson["dateAdded"], customerJson["cType"], customerJson["address"]))

        for job in customerJson["jobHistory"]:
            duration = interpreter.toMinutes(job["duration"])
            
            job_cursor.execute("INSERT INTO JOB_HISTORY VALUES(?,?,?,?,?,?,?)", (
                customerJson["id"], 
                job["date"], 
                job["type"],
                job["price"],
                job["assigned"],
                duration,
                job["invoice"]))

    job_connection.commit()
    job_connection.close()

    customers_connection.commit()
    customers_connection.close()



#   Row: Customer id, customer name, company name, date added, cType, customer address
def __createCustomerTable():
    connection = sqlite3.connect(mCustomerDb)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS {}".format(r.customerTable))
    
    tableCommand = """ CREATE TABLE {} (
                    customer_id integer PRIMARY KEY,
                    name text NOT NULL,
                    company_name text,
                    date_added text,
                    customer_type text,
                    address text NOT NULL
                )
                """.format(r.customerTable)

    cursor.execute(tableCommand)
    connection.close()

    
#   Row: Customer Id, jobType, jobPrice, jobDate, employee, duration, invoice 
def __createJobTable():
    connection = sqlite3.connect(mJobDb)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS {}".format(r.jobTable))
    
    tableCommand = """ CREATE TABLE {} (
                    customer_id integer NOT NULL,
                    job_date text,
                    job_type text,
                    job_price real,
                    employee text,
                    duration real,
                    invoice integer
                )
                """.format(r.jobTable)

    cursor.execute(tableCommand)
    connection.close()


def printTable(tableName, filename):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()

    data = cursor.execute(f'''SELECT * FROM {tableName}''')
    for row in data:
        print(row)

    connection.close()