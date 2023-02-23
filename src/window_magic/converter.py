# SECTION PURPOSE
# ==================================================================================
#   This will consolidate services into a Window Magic recognized "Job". No filters 
#   will be applied. Rather a pure database structure to serve command line queries.
# ==================================================================================

from src.customer_factor_importer import assistant as cf_rep
from collections import defaultdict
from src.window_magic.databases import _complete_database as database
from src.window_magic.objects import job

def initWindowMagic_DB():
    wmHistory = []
    ## Get active customers
    allActiveCustomers = cf_rep.getActiveCustomers()
    print('[STATUS] Detected {} active customers'.format(len(allActiveCustomers)))
     ## Iterate through active customers
     # Convert to Window Magic Jobs
    for customer in allActiveCustomers:
        id              = customer[0]
        name            = cf_rep.getCustomerName(id)
        address         = cf_rep.getCustomerAddress(id)
        jobHistory      = jobHistoryBuilder(id)

        for pastJob in jobHistory:
            pastJob: job.Job = pastJob
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
        database.create(wmHistory)
        database.writeCSV()


def jobHistoryBuilder(customer_id):
    jobHistory = []
    entireServiceHistory = gatherServiceHistory(customer_id)
    i = 0

    for service_date, serviceDetails in entireServiceHistory.items():
        # Defines Window Magic's contract, how long it took, and which employees were involved.
        completedJob = job.Job(service_date, serviceDetails)
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
def gatherServiceHistory(customer_id):
    # Get complete customer history in descending order according to date.
    # Latest to oldest (*Only gets history from past jobs. Does NOT consider upcoming jobs)
    serviceHistory = cf_rep.getCustomerHistory(customer_id) 
    
    # Group jobs
    completeService = defaultdict(list)
    for service in serviceHistory:
        service_date = service[1] ## Position of Date saved per The Customer Factor DB
        completeService[service_date].append(service)

    return completeService
