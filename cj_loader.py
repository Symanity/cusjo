
import csv
import io
import os
import json
import resources as r

def readOnly(fileName):
    directory = os.path.join(os.getcwd(), "res")
    csv_dict = os.path.join(directory, fileName)
    customerData = io.open(csv_dict, 'r', encoding="utf-8")

    try:
        rawData = csv.DictReader(customerData)
        customers = consolidate(rawData)

        return customers

    finally:
        customerData.close()
        

def consolidate(data):
    customer = None
    customers = []

    for row in data:
        if customer:
            if(customer.id == row[r.id]):
                # consolidate job history
                job = Job(row)
                customer.jobHistory.append(job)
            else: 
                # Save customer and continue to next
                customers.append(customer.toJson())
                customer = Customer(row)
                
        else: # For first pass through
            customer = Customer(row)

    return customers

class Job:
    def __init__(self, data):
        self.date = data[r.jobDate]
        self.type = data[r.jobType]
        self.price = data[r.price]
        self.assiged = data[r.assignedTo]
        self.duration = data[r.duration]
        self.invoice = data[r.invoiceNumber]

    def __str__(self):
        return self.date

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)


class Customer:
    def __init__(self, data):
        self.id  = data[r.id]
        self.name = data[r.name]
        self.company = data[r.companyName]
        self.dateAdded = data[r.dateAdded]
        self.cType = data[r.cType]
        self.address = data[r.address]
        self.jobHistory = []


    def __str__(self):
        return self.name

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)