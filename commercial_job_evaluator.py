import cj_interpreter as inter
import json
import datetime
from datetime import date 
import cj_evaluator as eval

DATE_FORMAT = '%m/%d/%y'

def assessCommericalJobs(startDate, endDate):
    customers = inter.load()
    evals = []

    results = ""

    date1 = datetime.datetime.strptime(startDate, DATE_FORMAT).date()
    date2 = datetime.datetime.strptime(endDate, DATE_FORMAT).date()

    for customerData in customers:
        customer =  json.loads(customerData)
        customerAnalyzer = eval.Evaluator(customer)

        if eval.Evaluator.isActive(customer, (date2-date1).days):
            results += customer["name"].upper() + ": " + customer["address"] +"\n"
            evals = customerAnalyzer.evaluatations
            
            for evalKey in evals:
                priceObj = evals[evalKey].getPrice()
                durationObj = evals[evalKey].getDuration()

                results += ("\t"+evalKey + "\n")

                if priceObj:
                    results += ("\t Most Recent Price:\t$" + str(priceObj["price"]) + " \t\t=> " + str(priceObj) + "\n")
                else:
                    results += ("\t Most Recent Price:\tNO PRICE AVAILABLE\n")


                if durationObj:
                    results += ("\t Average Duration:\t" + str("{:.2f}".format(durationObj["avg duration in mins"])) + " mins \t=> " + str(durationObj) + "\n")
                else:
                    results += ("\t Average Duration:\tNO DURATION AVAILABLE\n")

                results += ("\n")

            results += ("\n\n")

    printToFile(results)


def printToFile(string):
    with open('cj_eval_results.txt', 'w') as f:
        f.write(string)

assessCommericalJobs("01/01/19", "11/13/22")