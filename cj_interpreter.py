
import csv
import io
import os
import json

FILE_BASE = os.path.join(os.getcwd(), "res")
CUSTOMER_DATA = os.path.join(FILE_BASE, "CF_exported.csv")

CUSTOMER_ID = 'Id'
CUSTOMER_NAME = 'Customer Name'
COMPANY_NAME = 'Company Name'
DATE_ADDED = 'Date Added'
CUSTOMER_TYPE = 'Customer Type'

# JOB 
JOB_DATE = 'Job Date'
JOB_TYPE = 'Job Type'
PRICE = 'Price'
ASSIGNED_TO = 'Assigned To'
DURATION = 'Duration'
INVOICE_NUMBER = 'Invoice Number'

# Return dictionay
def consolidate(data):
    customer = None
    customers = []

    for row in data:
        if customer:
            if(customer.id == row[CUSTOMER_ID]):
                # consolidate job history
                job = Job(row)
                customer.jobHistory.append(job)
            else: 
                # Save customer and continue to next
                customers.append(customer)
                customer = Customer(row)
                
        else: # For first pass through
            customer = Customer(row)

    return customers

class Job:
    def __init__(self, data):
        self.date = data[JOB_DATE]
        self.type = data[JOB_TYPE]
        self.price = data[PRICE]
        self.assiged = data[ASSIGNED_TO]
        self.duration = data[DURATION]
        self.invoice = data[INVOICE_NUMBER]

    def __str__(self):
        return self.date


class Customer:
    def __init__(self, data):
        self.id  = data[CUSTOMER_ID]
        self.name = data[CUSTOMER_NAME]
        self.company = data[COMPANY_NAME]
        self.dateAdded = data[DATE_ADDED]
        self.cType = data[CUSTOMER_TYPE]
        self.jobHistory = []


    def __str__(self):
        return self.name


# --------------------MAIN--------------------
customerData = io.open(CUSTOMER_DATA, 'r', encoding="utf-8")

try:
    rawData = csv.DictReader(customerData)
    consolidate(rawData)

finally:
    print('end')



    #Goal == get data into a json file 
    # CUSTOMER_DB = {
    #     customerKey: {
    #         customerName: '',
    #         'etc'
    #     }
    # }