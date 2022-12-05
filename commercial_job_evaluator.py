import cj_loader as customerFactor
import sql_converter as interpreter

def assessCommericalJobs(startDate, endDate):
    exportedFileName = "CF_exported.csv"
    data = customerFactor.readOnly(exportedFileName)
    customerData = interpreter.read(data)

    # SQL Queries
    # 1. Filter by date range
    # 2. filter by employee
    # 3. filter by frequency
    # 4. search by name



assessCommericalJobs("01/01/19", "11/13/22")