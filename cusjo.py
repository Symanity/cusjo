##
# THIS IS THE DRIVER OF THE CUSJO PROGRAM.
# There are various commands that can be executed from the terminal.
# Basic Operation:
#   py cusjo.py build       <- Reads and builds from The Customer Factor file located in the res folder
#   py cusjo.py evaluate    <- Evaluates the Customers. Creates the evaluations.txt file.
##

# from datetime import datetime
# import src.window_magic.evaluators.customer_evaluator as WindowMagic
# import customer_evaluators.jc_db_generator as wmDatabase

import sys
from src.customer_factor_importer import assistant
from src.window_magic import converter

# 1. Filter by date range
# 2. filter by employee
# 3. filter by frequency
# 4. search by name

SAMPLE_FILE = "CF_exported.csv"

ACTIVE_JOB_HISTORY = """
        SELECT c.name, j.*
        FROM JOB_HISTORY j
        INNER JOIN CUSTOMERS c ON c.customer_id = j.customer_id
        WHERE c.active_status = 1
        """

EMPLOYEE_JOB_HISTORY = ''' 
    SELECT * 
    FROM CUSTOMERS 
    INNER JOIN JOB_HISTORY ON CUSTOMERS.customer_id = JOB_HISTORY.customer_id 
    WHERE JOB_HISTORY.employee = 'Jose Perez' '''

# def initEvaluationProcess():
#     # Gather only the active customers
#     WM_commerical_jobs = WindowMagic.initEvaluations(assistant.getActiveCustomers())

#     with open('evaluations.txt', 'w') as results:

#         for job in WM_commerical_jobs:
#             job: WindowMagic.ServiceOf = job
#             customerId = job.customer_id
#             customerName = job.customer_name
#             customerAddress = job.customer_address

#             # results.write("{} - {}: {}".format(customerId, customerName, customerAddress))

#             if job.evaluations:
#                 for evaluation in job.evaluations:
#                     outputText = "\n"
#                     jobPoolQty = evaluation.dataCount
#                     evaluation: WindowMagic.Evaluation = evaluation
#                     services = evaluation.serviceTitle
#                     totalPrice = evaluation.price
#                     avgDuration = evaluation.getAvgDuration()
#                     jobFrequency = evaluation.frequency
#                     contributingEmployees = evaluation.employees
#                     rate = evaluation.getRate()

#                     if evaluation.getRate() < 105:

#                         results.write("{} - {}: {}".format(customerId, customerName, customerAddress))

#                         outputText = outputText + "\tAccording to {}\n".format(contributingEmployees)
#                         outputText = outputText + "\t{} on a {} basis for ${} and takes an average of {} minutes\n".format(
#                             services,
#                             jobFrequency.upper() if jobFrequency else "Infrequently",
#                             totalPrice,
#                             avgDuration)

#                         outputText = outputText + "\tThat is ${} per hour - Data Count {}\n\n".format(rate, jobPoolQty)
                        
#                         # else:
#                         #     outputText = "INSUFFICENT DATA :(\n"

#                         results.write(outputText)
#                     else:
#                         print("skipping: {}".format(job.customer_name))

#             else:
#                 results.write(" INSUFFICENT RESULTS :(\n\n")

#     results.close()


# def preivewEvaluationOfCustomer(customerId: int):
#     theService = WindowMagic.ServiceOf(customerId)
#     theService.evaluate()

#     if not theService.customer_name:
#         raise Exception()

#     printToTerminal(theService)

#     print(theService)



# def printToTerminal(theServices: WindowMagic.ServiceOf):
#     customerId = theServices.customer_id
#     customerName = theServices.customer_name
#     customerAddress = theServices.customer_address

#     print("{} - {}: {}".format(customerId, customerName, customerAddress))

#     if theServices.evaluations:
#         for evaluation in theServices.evaluations:
#             outputText = "\n"
#             jobPoolQty = evaluation.dataCount
#             evaluation: WindowMagic.Evaluation = evaluation
#             services = evaluation.serviceTitle
#             totalPrice = evaluation.price
#             avgDuration = evaluation.getAvgDuration()
#             jobFrequency = evaluation.frequency
#             contributingEmployees = evaluation.employees
#             rate = evaluation.getRate()

#             outputText = outputText + "\tAccording to {}\n".format(contributingEmployees)
#             outputText = outputText + "\t{} on a {} basis for ${} and takes an average of {} minutes\n".format(
#                 services,
#                 jobFrequency.upper() if jobFrequency else "Infrequently",
#                 totalPrice,
#                 avgDuration)

#             outputText = outputText + "\tThat is ${} per hour - Data Count {}\n\n".format(rate, jobPoolQty)
            

#             print(outputText)

#     else:
#         print(" INSUFFICENT RESULTS :(\n\n")


def printRes(response = None, query=None):
    if response:
        for r in response:
            print(r)

    else:
        print('[STATUS] ... no response')


# ====================================================================
# DRIVER
# ====================================================================
if len(sys.argv) > 1:
    theCase = sys.argv[1]

    if str(sys.argv[1]) == "build":
        if len(sys.argv) > 2:
            try:
                assistant.build_database(str(sys.argv[2]))
            except:
                print("[FATAL-ERROR] invalid file")

        else:
            assistant.build_database()



    # elif sys.argv[1] == "evaluate":
    #     try:
    #         if len(sys.argv) > 2:
    #             customerId = int(sys.argv[2])
    #             preivewEvaluationOfCustomer(customerId)
    #         else:
    #             # initEvaluationProcess()
    #             pass

    #     except ValueError:
    #         print('[ERROR] Invalid customer id')

    # else:
    #     print('[ERROR] command not recognized')

else:
    converter.initWindowMagic_DB()
    pass
    # query = """SELECT customer_id, customer_name FROM {} WHERE employee = 'Roberto Isais' GROUP BY customer_id HAVING COUNT(DISTINCT employee) = 1""".format(wmDatabase.tbl_consideredJobs)
    # res = wmDatabase.ask(query)
    # printRes(res)
    # initEvaluationProcess()