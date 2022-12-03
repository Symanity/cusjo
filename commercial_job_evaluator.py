import cj_loader as customerFactor
import sql_converter as interpreter

def assessCommericalJobs(startDate, endDate):
    exportedFileName = "CF_exported.csv"
    data = customerFactor.readOnly(exportedFileName)
    customerData = interpreter.read(data)

    # SQL Queries



assessCommericalJobs("01/01/19", "11/13/22")