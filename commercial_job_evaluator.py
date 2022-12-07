import json
import cj_loader as customerFactor
import cj_interpreter as inter
import db_generator as db

def assessCommericalJobs(startDate, endDate):
    exportedFileName = "CF_exported.csv"
    data = customerFactor.readOnly(exportedFileName)
    
    for cData in data:
        customerJson = json.loads(cData)
        evals = inter.Evaluator(customerJson)

        print(evals)
        for key in evals.services:
            frequency = evals.services[key].getFrequency()
            print("\t{} every {} days".format(key, frequency))
            
        # target = customerJson["name"]
        # if target == "Watchlight Corporation":
        #     for key in evals.services:
        #         evals.services[key].getFrequency()


    # Create SQLite database/tables
    # db.create(data)
    
    # SQL Queries
    # 1. Filter by date range
    # 2. filter by employee
    # 3. filter by frequency
    # 4. search by name



assessCommericalJobs("01/01/19", "11/13/22")