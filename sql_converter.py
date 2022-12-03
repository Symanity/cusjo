import cj_json as cJson
import json
import datetime

DATE_FORMAT = '%m/%d/%y'

def read(data):
    services = []

    for customerData in data:
        customerJson =  json.loads(customerData)
        customer = cJson.Evaluator(customerJson)
        services = customer.services

        for serviceKey in services:
            service = services[serviceKey]
            print(service.getPrice()) #<- returning Json of {'job': {JOB OBJECT}, 'price': PRICE_VALUE}
