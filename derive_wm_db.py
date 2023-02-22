# SECTION PURPOSE
# ==================================================================================
#   This will consolidate services into a Window Magic recognized "Job". No filters 
#   will be applied. Rather a pure database structure to serve command line queries.
# ==================================================================================

from customer_factor_importer import database
import customer_evaluators.customer_evaluator as evaluator
from collections import defaultdict
import customer_evaluators.jc_db_generator as wm_db_generator


# def initWindowMagic_DB():
#     for ser

def initWindowMagic_DB():
    wmHistory = []
    ## Get active customers
    allActiveCustomers = retrieveActiveCustomers()
    print('[STATUS] Detected {} active customers'.format(len(allActiveCustomers)))
     ## Iterate through active customers
     # Convert to Window Magic Jobs
    for customer in allActiveCustomers:
        id           = customer[0]
        name        = database.getCustomerName(id)
        address     = database.getCustomerAddress(id)
        jobHistory = jobHistoryBuilder(id)

        for pastJob in jobHistory:
            pastJob: evaluator.TheJob = pastJob
            considerJob = (
                    id, 
                    name, 
                    address, 
                    str(pastJob.title), 
                    pastJob.date,
                    pastJob.price,
                    pastJob.duration,
                    pastJob.employee
                )
            wmHistory.append(considerJob)

    print('[STATUS] finished gathering {} jobs'.format(len(wmHistory)))

    ## Save job list into db
    if wmHistory:
        wm_db_generator.create(wmHistory)
        wm_db_generator.writeCSV()


def jobHistoryBuilder(customer_id):
    jobHistory = []
    entireServiceHistory = retrieveServiceHistory(customer_id)
    i = 0

    for service_date, serviceDetails in entireServiceHistory.items():
        # Defines Window Magic's contract, how long it took, and which employees were involved.
        completedJob = evaluator.TheJob(service_date, serviceDetails)
        totalPrice = completedJob.price
        totalDuration = completedJob.duration

        # [DATA QUALITY FILTER] Only consider if totalPrice have been identified
        if totalPrice:
            i = i+1

            # Archive service details performed on given date
            jobHistory.append(completedJob)

        else:
             print('[ERROR] Failed to recognize price for {}'.format(customer_id))

    return jobHistory



# Combines Services which were done at the same time for the same customer.
# Example: On 12/7/20, Interior/Exterior Windows AND partition
# Returns key/value pair. {service_date:[list of services_performed]}
def retrieveServiceHistory(customer_id):
    # Get complete customer history in descending order according to date.
    # Latest to oldest (*Only gets history from past jobs. Does NOT consider upcoming jobs)
    serviceHistory = database.getCustomerHistory(customer_id) 
    
    # Group jobs
    completeService = defaultdict(list)
    for service in serviceHistory:
        service_date = service[1] ## Position of Date saved per The Customer Factor DB
        completeService[service_date].append(service)

    return completeService


# Query The Customer Factor database and retrieve only the active customers
def retrieveActiveCustomers():
        question = """
            SELECT *
            FROM CUSTOMERS
            WHERE active_status = 1
            """ 
        return database.ask(question)

initWindowMagic_DB()