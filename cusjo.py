import cf_interpreters.cf_loader as customerFactor
import cf_interpreters.db_generator as database
from datetime import datetime
import sys
import customer_evaluators.customer_evaluator as WindowMagic

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

def outputResults():
    WM_commerical_jobs = WindowMagic.initEvaluations(getActiveCustomers())

    with open('evaluations.txt', 'w') as results:

        for job in WM_commerical_jobs:
            job: WindowMagic.ServiceOf = job
            customerId = job.customer_id
            customerName = job.customer_name
            customerAddress = job.customer_address

            results.write("{} - {}: {}".format(customerId, customerName, customerAddress))

            if job.evaluations:
                for evaluation in job.evaluations:
                    outputText = "\n"
                    jobPoolQty = evaluation.dataCount
                    evaluation: WindowMagic.Evaluation = evaluation
                    services = evaluation.serviceTitle
                    totalPrice = evaluation.price
                    avgDuration = evaluation.getAvgDuration()
                    jobFrequency = evaluation.frequency
                    contributingEmployees = evaluation.employees
                    rate = evaluation.getRate()

                    outputText = outputText + "\tAccording to {}\n".format(contributingEmployees)
                    outputText = outputText + "\t{} on a {} basis for ${} and takes an average of {} minutes\n".format(
                        services,
                        jobFrequency.upper() if jobFrequency else "Infrequently",
                        totalPrice,
                        avgDuration)

                    outputText = outputText + "\tThat is ${} per hour - Data Count {}\n\n".format(rate, jobPoolQty)
                    
                    # else:
                    #     outputText = "INSUFFICENT DATA :(\n"

                    results.write(outputText)

            else:
                results.write(" INSUFFICENT RESULTS :(\n\n")

    results.close()


def preivewEvaluationOfCustomer(customerId: int):
    theService = WindowMagic.ServiceOf(customerId)

    if not theService.customer_name:
        raise Exception()

    printToTerminal(theService)



def printToTerminal(theServices: WindowMagic.ServiceOf):
    customerId = theServices.customer_id
    customerName = theServices.customer_name
    customerAddress = theServices.customer_address

    print("{} - {}: {}".format(customerId, customerName, customerAddress))

    if theServices.evaluations:
        for evaluation in theServices.evaluations:
            outputText = "\n"
            jobPoolQty = evaluation.dataCount
            evaluation: WindowMagic.Evaluation = evaluation
            services = evaluation.serviceTitle
            totalPrice = evaluation.price
            avgDuration = evaluation.getAvgDuration()
            jobFrequency = evaluation.frequency
            contributingEmployees = evaluation.employees
            rate = evaluation.getRate()

            outputText = outputText + "\tAccording to {}\n".format(contributingEmployees)
            outputText = outputText + "\t{} on a {} basis for ${} and takes an average of {} minutes\n".format(
                services,
                jobFrequency.upper() if jobFrequency else "Infrequently",
                totalPrice,
                avgDuration)

            outputText = outputText + "\tThat is ${} per hour - Data Count {}\n\n".format(rate, jobPoolQty)
            

            print(outputText)

    else:
        print(" INSUFFICENT RESULTS :(\n\n")


def printRes(response = None, query=None):
    if response:
        for r in response:
            print(r)

    else:
        print('[STATUS] ... no response')


# Returns RAW file data without building the database
def previewFile(fileName):
    fileName = "CF_exported.csv"
    customerFactor.init(fileName)
    return customerFactor.fetchData()
    

# Builds the Customer Factor database
def build(fileName):
    customerFactor.init(fileName)
    data = customerFactor.fetchData()
    database.create(data)
    database.writeCSV()


def showEmployees():
    question = "SELECT DISTINCT employee FROM {}".format(database.tbl_jobHistory)
    return database.ask(question)

def searchForCustomers(customersName):
    question = "SELECT * FROM CUSTOMERS WHERE name LIKE '{}%'".format(customersName)
    return database.ask(question)


def getActiveCustomers():
        question = """
            SELECT *
            FROM CUSTOMERS
            WHERE active_status = 1
            """ 
        return database.ask(question)

if len(sys.argv) > 1:
    theCase = sys.argv[1]

    if str(sys.argv[1]) == "build":
        if len(sys.argv) > 2:
            try:
                build(str(sys.argv[2]))
            except:
                print("[FATAL-ERROR] invalid file")

        else:
            build(SAMPLE_FILE)

    elif sys.argv[1] == "search":
        if len(sys.argv) > 2:
            if(sys.argv[2] == "history"):
                printRes(database.getCustomerHistory(str(sys.argv[3])))

            else:
                print("Searching ....")
                printRes(searchForCustomers(str(sys.argv[2])))

    elif sys.argv[1] == "print":
        if len(sys.argv) > 2:
            if sys.argv[2] == "employees":
                printRes(showEmployees())

            elif sys.argv[2] == "active_customers":
                printRes(getActiveCustomers())

            elif sys.argv[2] == "customers":
                query = """ SELECT * FROM {} """.format(database.tbl_Customers)
                res = database.ask(query)
                printRes(res)

            elif sys.arg[2] == "job_history":
                query = """ SELECT * FROM {} """.format(database.tbl_jobHistory)
                res = database.ask(query)
                printRes(res)


    elif sys.argv[1] == "evaluate":
        try:
            if len(sys.argv) > 2:
                customerId = int(sys.argv[2])
                preivewEvaluationOfCustomer(customerId)
            else:
                outputResults()

        except ValueError:
            print('[ERROR] Invalid customer id')

        except:
            print('[ERROR] Unable to process request. Customer does not exist')

    else:
        print('[ERROR] command not recognized')

else:
    outputResults()


# Usefull snippets
    # Create SQLite database/tables
    # database.create(data)

    # database.printTable(database.tbl_Customers, database.CF_db)

    # customers = customerFactor.getCustomers()
    # for customer in customers:
    #     if customer.isActive():
    #         print("[ACTIVE] {}".format(customer.name))
    #     else:
    #         print("[-] {}".format(customer.name))



# QUESTION HISTORY
    # ** show me the list of Customers where Jose is the employee
    # question = ''' SELECT * FROM CUSTOMERS INNER JOIN JOB_HISTORY ON CUSTOMERS.customer_id = JOB_HISTORY.customer_id WHERE JOB_HISTORY.employee = 'Jose Perez' '''
    