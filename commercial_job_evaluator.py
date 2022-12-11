import json
import cf_loader as customerFactor
import cf_interpreter as inter
import db_generator as database
import resources as r

import sqlite3

def assessCommericalJobs(startDate, endDate):
    exportedFileName = "CF_exported.csv"
    customerFactor.init(exportedFileName)
    data = customerFactor.fetchData()
    
    # Create SQLite database/tables
    # database.create(data)

    # database.printTable(database.tbl_jobHistory, database.CF_db)

    customers = customerFactor.getCustomers()
    for customer in customers:
        customerJSON = customer.toJson()
        

    
    # SQL Queries () 
    #### [** ONLY DO FROM LAST 12 JOBS ***]
    #### Consider Job types being done on the same day
    #### Jobs may have two jobTypes done on the same day. This job structure may have the same duration.

    # 1. Filter by date range
    # 2. filter by employee
    # 3. filter by frequency
    # 4. search by name


assessCommericalJobs("01/01/19", "11/13/22")