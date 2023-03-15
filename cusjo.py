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
from src.window_magic.outputter import Outputer

def printRes(response = None):
    if response:
        for r in response:
            print(r)

    else:
        print('[STATUS] ... no response')


def outCSV(evaluations = None):
    outputer = Outputer(evaluations)
    outputer.output_to_csv()
    outputer.output_history_to_csv()

def printEvaluations(evaluations, customer_id = None):
    outputer = Outputer(evaluations)
    outputer.output_to_console(customer_id)


# ====================================================================
# DRIVER
# ====================================================================
if len(sys.argv) > 1:
    theCase = sys.argv[1]

    if theCase == "help" or theCase == "-h":
        print("1. Import file into res folder")
        print("2. Build CF database with 'build' keyword")
        print("3. Convert the CF database with 'convert' keyword")
        print("4. Create evaluations with 'evalutate' keyword")

    if str(sys.argv[1]) == "build":                             # BUILD THE CUSTOMER FACTOR DATABASE
        if len(sys.argv) > 2:
            try:
                assistant.build_database(str(sys.argv[2]))
            except:
                print("[FATAL-ERROR] invalid file")

        else:
            assistant.build_database()

    elif str(sys.argv[1]) == "convert":                           # CONVERT THE CUSTOMER FACTOR DATABASE TO WINDOW MAGIC DATABASE
        try:
            converter.initWindowMagic_DB()
        except:
            print("[FATAL-ERROR] invalid file")


    elif str(sys.argv[1]) == "list":                           # CONVERT THE CUSTOMER FACTOR DATABASE TO WINDOW MAGIC DATABASE
        if len(sys.argv) > 2:
            if sys.argv[2] == "employees":
                try:
                    res = assistant.listEmployees()
                    printRes(res)
                except:
                    print("[FATAL-ERROR] could not retrieve employees")


    elif sys.argv[1] == "evaluate":
        try:
            if len(sys.argv) > 2:
                customerId = int(sys.argv[2])
                evaluator.EVALUATE_CUSTOMER = customerId
                customer_evaluations = evaluator.evaluate(customerId)
                
            else:
                customer_evaluations = evaluator.evaluate()
                outputer = Outputer(customer_evaluations)
                outputer.output_to_csv()
                outputer.output_history_to_csv()

        except ValueError:
            print('[ERROR] Invalid customer id')

    # else:
    #     print('[ERROR] command not recognized')

else:
    # customer_evaluations = evaluator.evaluate(9992)
    evaluator.EVALUATE_CUSTOMER = 246
    customer_evaluations = evaluator.evaluate()
    

    outputer = Outputer(customer_evaluations)
    outputer.output_to_csv()
    outputer.output_history_to_csv()
