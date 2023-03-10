# Expected post-case:
#   TABLE1: CUSTOMERS
#   Row: Customer id, customer name, company name, customer address, date added, cType

#   TABLE2: Job History
#   Row: Customer Id, jobType, jobPrice, jobDate, employee, duration, invoice 

from src.customer_factor_importer import _interpreter
from src.customer_factor_importer import _loader as customerFactor
from datetime import datetime
import json

import sqlite3
import csv
import os
import src.customer_factor_importer._resources as r

CF_db_name = "CF_complete_history.db"
CF_db = os.path.join(r.database_path,CF_db_name)

tbl_Customers = "CUSTOMERS"
tbl_jobHistory = "JOB_HISTORY"

def create(data, databaseName = CF_db):
    # Create necessary tables
    __createCustomerTable()
    __createJobTable()

    if databaseName == CF_db:
        print("[BUILD] sql tables created")
        print("[BUILD] beginning CustomerFactor raw data processing")
        __generateDB(data)
        print("[BUILD] database built successfully")
         

def __generateDB(data):
    connection = sqlite3.connect(CF_db)
    cursor = connection.cursor()

    for customerData in data:
        customer =  json.loads(customerData)
        customerObj = customerFactor.Customer(json=customer)
        customerEvaluator = _interpreter.Evaluator(customer)

        services = customerEvaluator.services
        
        # Insert Customer Data row into Customers.db
        cursor.execute("INSERT INTO CUSTOMERS VALUES(?,?,?,?,?,?,?)", (
            customer["id"],
            customer["name"],
            customer["company"],
            customer["dateAdded"],
            customer["cType"],
            customer["address"],
            customerObj.isActive()
            ))

        print("processing {}...".format(customer["name"]))
        for job in customer["jobHistory"]:
            duration = _interpreter.toMinutes(job["duration"])
            serviceName = job["type"]

            # print("{} GETS {} DONE EVERY {} DAYS".format(customerJson["name"], job["type"], services[serviceName].getFrequency()))
            cursor.execute("INSERT INTO JOB_HISTORY VALUES(?,?,?,?,?,?,?)", (
                customer["id"], 
                job["date"], 
                job["type"],
                job["price"],
                job["assigned"],
                duration,
                job["invoice"]
                ))
            
        print('\tdone')

    connection.commit()
    connection.close()


#   Row: Customer id, customer name, company name, date added, cType, customer address, customer active status
def __createCustomerTable():
    connection = sqlite3.connect(CF_db)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS {}".format(tbl_Customers))
    
    tableCommand = """ CREATE TABLE {} (
                    customer_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    company_name TEXT,
                    date_added TEXT,
                    customer_type TEXT,
                    address TEXT NOT NULL,
                    active_status INTEGER NOT NULL
                )
                """.format(tbl_Customers)

    cursor.execute(tableCommand)
    connection.close()

    
#   Row: Customer Id, jobType, jobPrice, jobDate, employee, duration, invoice, frequency
def __createJobTable():
    connection = sqlite3.connect(CF_db)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS {}".format(tbl_jobHistory))
    
    tableCommand = """ CREATE TABLE {} (
                    customer_id integer NOT NULL,
                    job_date text,
                    job_type text,
                    job_price real,
                    employee text,
                    duration real,
                    invoice integer
                )
                """.format(tbl_jobHistory)

    cursor.execute(tableCommand)
    connection.close()


# args must be of type Tuble
def ask(sqlite_query, args=None):
    response = []
    conn = sqlite3.connect(CF_db)
    cursor = conn.cursor()

    if args:
        # Execute the query with the parameter
        cursor.execute(sqlite_query, args)
    else:
        # Execute the SQL command
        cursor.execute(sqlite_query)

    # Fetch the results
    results = cursor.fetchall()

    # Print the results
    for row in results:
        response.append(row)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return response


def askOne(sqlite_query, args=None):
    # connect to the database
    conn = sqlite3.connect(CF_db)

    # create a cursor
    cursor = conn.cursor()

    if args:
        # Execute the query with the parameter
        cursor.execute(sqlite_query, args)
    else:
        # Execute the SQL command
        cursor.execute(sqlite_query)

    # fetch the result
    result = cursor.fetchone()

    # close the connection
    conn.close()

    # return the customer name, or None if not found
    return result[0] if result else None


def writeCSV():
    csv_foldername = "csv_complete_history"
    csv_customers = os.path.join(r.database_path, csv_foldername,"customers.csv")
    csv_jobs = os.path.join(r.database_path, csv_foldername,"jobs.csv")

    # Connect to the database file
    conn = sqlite3.connect(CF_db)

    # Create a cursor object
    cursor = conn.cursor()

    # Select all rows from the CUSTOMERS table
    cursor.execute("SELECT * FROM CUSTOMERS")

    # Fetch all rows from the CUSTOMERS table
    customers = cursor.fetchall()

    # Write the rows to a CSV file
    with open(csv_customers, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(customers)

    # Select all rows from the JOB_HISTORY table
    cursor.execute("SELECT * FROM JOB_HISTORY")

    # Fetch all rows from the JOB_HISTORY table
    jobs = cursor.fetchall()

    # Write the rows to a CSV file
    with open(csv_jobs, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(jobs)

    # Close the cursor and connection
    cursor.close()
    conn.close()

    print('[BUILD] csv file created: {}'.format(csv_customers))
    print('[BUILD] csv file created: {}'.format( csv_jobs))