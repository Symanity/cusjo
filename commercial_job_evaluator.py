import cj_loader as customerFactor
import db_generator as db

def assessCommericalJobs(startDate, endDate):
    exportedFileName = "CF_exported.csv"
    data = customerFactor.readOnly(exportedFileName)
    customerData = db.create(data)
    

    # SQL Queries
    # 1. Filter by date range
    # 2. filter by employee
    # 3. filter by frequency
    # 4. search by name



assessCommericalJobs("01/01/19", "11/13/22")