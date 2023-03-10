
import csv
import io
import os
import json
import src.customer_factor_importer._resources as r
from src.customer_factor_importer import _interpreter as inter
from datetime import datetime as dt

TARGET_FILE = None

def init(fileName):
    global TARGET_FILE 
    TARGET_FILE = fileName


def read(fileName):
    directory = os.path.join(os.getcwd(), "res")
    csv_dict = os.path.join(directory, fileName)
    customerData = io.open(csv_dict, 'r', encoding="utf-8")

    try:
        rawData = csv.DictReader(customerData)
        customers = __consolidate(rawData)

        return customers

    finally:
        customerData.close()


def fetchData():
    directory = os.path.join(os.getcwd(), "res")
    csv_dict = os.path.join(directory, TARGET_FILE)
    customerData = io.open(csv_dict, 'r', encoding="utf-8")

    try:
        rawData = csv.DictReader(customerData)
        customers = __consolidate(rawData)

        return customers

    finally:
        customerData.close()
        

# Returns a json representation of Customer
def getCustomers():
    rawData = fetchData()
    customers = []

    for customerData in rawData:
        customerJson = json.loads(customerData)
        customer = Customer(json=customerJson)
        customers.append(customer)

    return customers


def __consolidate(data):
    customer = None
    customers = []

    # NOTE: Customer is appended to Customers list if and only if Customer has a job history
    for row in data:
        if customer:
            if(customer.id == row[r.id]):
                # consolidate job history
                job = Service(row)
                customer.jobHistory.append(job)
            else: 
                # Save customer and continue to next
                customers.append(customer.toJson())
                customer = Customer(row)
                
        else: # For first pass through
            customer = Customer(row)

    return customers


class Service:
    def __init__(self, data):
        self.date = inter.convertTo_iso8601_date(data[r.jobDate])
        self.type = data[r.jobType]
        self.price = data[r.price]
        self.assigned = data[r.assignedTo]
        self.duration = data[r.duration]
        self.invoice = data[r.invoiceNumber]

    def __str__(self):
        return self.date

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class Customer:
    def __init__(self, csvRow = None, json = None) -> None:
        self.id         = None
        self.name       = None
        self.company    = None
        self.dateAdded  = None
        self.cType      = None
        self.address    = None
        self.jobHistory = None

        if csvRow is not None:
            self.id  = csvRow[r.id]
            self.name = csvRow[r.name]
            self.company = csvRow[r.companyName]
            self.dateAdded = inter.convertTo_iso8601_date(csvRow[r.dateAdded])
            self.cType = csvRow[r.cType]
            try:
                self.address = csvRow[r.address]
            except KeyError:
                self.address = csvRow[r.street_address]
            except Exception as e:
                print(f"Unexpected error: {e}")
                
            self.jobHistory = []

        elif json:
            self.id         = json["id"]
            self.name       = json["name"]
            self.company    = json["company"]
            self.dateAdded  = json["dateAdded"]
            self.cType      = json["cType"]
            self.address    = json["address"]
            self.jobHistory = json["jobHistory"]


    def __str__(self):
        return self.name


    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    
    # Considered active if Customers have jobs scheduled in the future
    def isActive(self):
        dateFormat = '%Y-%m-%d'
        today = dt.today().date()  # get the current date
        iso_date = today.strftime(dateFormat)

        for job in self.jobHistory:
            jobDateStr = job["date"]
            jobDate = dt.strptime(jobDateStr, dateFormat).date()

            if jobDate > today:
                return True

        return False

