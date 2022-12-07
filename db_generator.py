# Expected post-case:
#   TABLE1: CUSTOMERS
#   Row: Customer id, customer name, company name, customer address, date added, cType

#   TABLE2: Job History
#   Row: Customer Id, jobType, jobPrice, jobDate, employee, duration, invoice 

import cj_interpreter as interpreter
import json

import sqlite3

DATE_FORMAT = '%m/%d/%y'
CustomerDb = "Customers.db"
JobsDb = "JobHistory.db"

CustomerTable = "CUSTOMERS"
JobTable = "JOB_HISTORY"

def create(data):
    # Create necessary tables
    __createCustomerTable()
    __createJobTable()

    print("[STATUS] sql tables created")
    print("[STATUS] beginning CustomerFactor raw data processing")
    __generateDB(data)
    print("[STATUS] successfully processed CustomerFactor data")


def __generateDB(data):
    customers_connection = sqlite3.connect(CustomerDb)
    customers_cursor = customers_connection.cursor()

    job_connection = sqlite3.connect(JobsDb)
    job_cursor = job_connection.cursor()

    for customerData in data:
        customer =  json.loads(customerData)
        customerEvaluator = interpreter.Evaluator(customer)

        services = customerEvaluator.services
        
        # Insert Customer Data row into Customers.db
        customers_cursor.execute("INSERT INTO CUSTOMERS VALUES(?,?,?,?,?,?)", (customer["id"], customer["name"], customer["company"], customer["dateAdded"], customer["cType"], customer["address"]))

        print("processing {}...".format(customer["name"]))
        for job in customer["jobHistory"]:
            duration = interpreter.toMinutes(job["duration"])
            serviceName = job["type"]

            # print("{} GETS {} DONE EVERY {} DAYS".format(customerJson["name"], job["type"], services[serviceName].getFrequency()))
            job_cursor.execute("INSERT INTO JOB_HISTORY VALUES(?,?,?,?,?,?,?,?)", (
                customer["id"], 
                job["date"], 
                job["type"],
                job["price"],
                job["assigned"],
                duration,
                job["invoice"],
                services[serviceName].getFrequency()
                ))
            
        print('\tdone')

    job_connection.commit()
    job_connection.close()

    customers_connection.commit()
    customers_connection.close()



#   Row: Customer id, customer name, company name, date added, cType, customer address
def __createCustomerTable():
    connection = sqlite3.connect(CustomerDb)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS {}".format(CustomerTable))
    
    tableCommand = """ CREATE TABLE {} (
                    customer_id integer PRIMARY KEY,
                    name text NOT NULL,
                    company_name text,
                    date_added text,
                    customer_type text,
                    address text NOT NULL
                )
                """.format(CustomerTable)

    cursor.execute(tableCommand)
    connection.close()

    
#   Row: Customer Id, jobType, jobPrice, jobDate, employee, duration, invoice, frequency
def __createJobTable():
    connection = sqlite3.connect(JobsDb)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS {}".format(JobTable))
    
    tableCommand = """ CREATE TABLE {} (
                    customer_id integer NOT NULL,
                    job_date text,
                    job_type text,
                    job_price real,
                    employee text,
                    duration real,
                    invoice integer,
                    job_frequency real
                )
                """.format(JobTable)

    cursor.execute(tableCommand)
    connection.close()


def printTable(tableName, filename):
    connection = sqlite3.connect(filename)
    cursor = connection.cursor()

    data = cursor.execute(f'''SELECT * FROM {tableName}''')
    for row in data:
        print(row)

    connection.close()