import json
import cf_loader as customerFactor
import cf_interpreter as inter
import db_generator as database
import resources as r

# SQL Queries () 
#### [** ONLY DO FROM LAST 12 JOBS ***]
#### TODO: Consider Job types being done on the same day
#### TODO: Jobs may have two jobTypes done on the same day. This job structure may have the same duration.

# 1. Filter by date range
# 2. filter by employee
# 3. filter by frequency
# 4. search by name

SAMPLE_FILE = "CF_exported.csv"

def printResponse(query):
    response = database.ask(query)

    for res in response:
        print(res)

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


def searchForCustomers(customersName):
    question = "SELECT * FROM CUSTOMERS WHERE NAME LIKE '{}%'".format(customersName)
    return database.ask(question)


build(SAMPLE_FILE)


    # data = customerFactor.fetchData()
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