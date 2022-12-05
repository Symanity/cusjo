# Expected post-case:
#   TABLE1: CUSTOMERS
#   Row: Customer id, customer name, job

import cj_json as cJson
import json
import datetime

DATE_FORMAT = '%m/%d/%y'

def read(data):
    services = []

    for customerData in data:
        customerJson =  json.loads(customerData)
        customerEvals = cJson.Evaluator(customerJson)
        services = customerEvals.services
        
        if(customerJson["id"] == "69"):
            print(customerJson["name"])
            print(customerEvals.services)

        # print(customerEvals)

        # for key in customerEvals:
        #     print(customerEvals[key])
            # service = services[serviceKey]
            # print(service.getPrice()) #<- returning Json of {'job': {JOB OBJECT}, 'price': PRICE_VALUE}

        


