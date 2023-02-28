##
# THIS IS THE DRIVER OF THE CUSJO PROGRAM.
# There are various commands that can be executed from the terminal.
# Basic Operation:
#   py cusjo.py build       <- Reads and builds from The Customer Factor file located in the res folder
#   py cusjo.py convert     <- Converts The Customer Factor Database into the Window Magic Database.
##

import sys
from src.customer_factor_importer import assistant
from src.window_magic.evaluators import evaluator
from src import converter

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

    if str(sys.argv[1]) == "build":                             # BUILD THE CUSTOMER FACTOR DATABASE
        if len(sys.argv) > 2:
            try:
                assistant.build_database(str(sys.argv[2]))
            except:
                print("[FATAL-ERROR] invalid file")

        else:
            assistant.build_database()

    if str(sys.argv[1]) == "convert":                           # CONVERT THE CUSTOMER FACTOR DATABASE TO WINDOW MAGIC DATABASE
        try:
            converter.initWindowMagic_DB()
        except:
            print("[FATAL-ERROR] invalid file")



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
    # customer_evaluations = evaluator.evaluate(9992)
    customer_evaluations = evaluator.evaluate_all()

    outputer = evaluator.Outputer(customer_evaluations)
    outputer.output_to_console()

    # for customer in customer_evaluations:
    #     print(f"{customer.id} - {customer.name} ({customer.address}) gets:")
    #     for service_key, evaluation in customer_evaluations[customer].items():
    #         print(f"{service_key} @ {evaluation}")