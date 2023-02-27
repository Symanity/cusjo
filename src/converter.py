# SECTION PURPOSE
# ==================================================================================
#   This will consolidate services into a Window Magic recognized "Job". No filters 
#   will be applied. Rather a pure database structure to serve command line queries.
# ==================================================================================
# Points of Note:
#   1. This only converts active customers

## TODO: Revise error detection when service durations do not match
## TODO: Find a way to determine job frequency

from src.customer_factor_importer import assistant as cf_rep
from collections import defaultdict
from src.window_magic.databasing import assistant

from src.window_magic import _resources as service_position


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
            pastJob: _Job = pastJob
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
        assistant.build_database(wmHistory)


def jobHistoryBuilder(customer_id):
    jobHistory = []
    entireServiceHistory = gatherServiceHistory(customer_id)
    i = 0

    for service_date, serviceDetails in entireServiceHistory.items():
        # Defines Window Magic's contract, how long it took, and which employees were involved.
        completedJob = _Job(service_date, serviceDetails)
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


# id, name, services, job_date, price, duration, employee
class _Job:
    def __init__(self, jobDate, servicesList):
        self.job        = servicesList

        self.title      = self.__extractServiceTitles(servicesList)
        self.price      = self.__extractPrice(servicesList)
        self.duration   = self.__extractDuration(servicesList)
        self.employee   = self.__extractEmployees(servicesList)
        self.date       = jobDate
        # self.frequency  = convertFrequency(self.__determineFrequency())



  ## ** For the Following function -> Extraction of data takes in servicesPerformed on a single day **
    # Get the employee(s) that were assigned to be on site.
    def __extractEmployees(self, job):
        employee = None
        for service in job:
            sus = service[service_position.Employee]

            if not employee and sus:
                employee = sus
                break

        if employee:
            return employee

        else:
            return "Unknown"

    def __extractPrice(self, job):
        totalPrice = 0
        for service in job:
            servicePrice = service[service_position.Service_Price]

            if servicePrice:
                totalPrice += servicePrice

        if totalPrice > 0:
            return totalPrice
        
        return None

    # Duration gets applied equally to all services performed at the same time.
    # For example, if three services were performed for a total of 1hr. CF applies 1hr to all three services. 
    def __extractDuration(self, job):
        totalDuration = None
        for service in job:
            duration = service[service_position.Service_Duration]

            if duration:
                if not totalDuration:
                    totalDuration = duration

                if totalDuration != duration: ## TODO: REVISE THIS Error Checker
                    # customerName = _database.getCustomerName(service[service_position.Customer_Id])
                    # address = _database.getCustomerAddress(service[service_position.Customer_Id])
                    # # print("[!] {} vs. {} -- check duration for {} service on {} for {}:{}".format(
                    #     totalDuration,
                    #     duration,
                    #     service[Service_Type], 
                    #     service[Service_Date], 
                    #     customerName,
                    #     address))
                    # print('\t[RECOVERY METHOD] Adding the durations together: {} mins\n'.format(totalDuration))
                    totalDuration = totalDuration + duration
            
        return totalDuration


    def __extractServiceTitles(self, job):
        serviceNames = []
        for service in job:
            name = service[service_position.Service_Type]

            if service not in serviceNames:
                serviceNames.append(name)

        return serviceNames


    # def __determineFrequency(self):
    #     customer_id = self.job[0][service_position.Customer_Id]
    #     deltas = []

    #     futureServices = _database.ask(''' SELECT * FROM JOB_HISTORY WHERE customer_id = ? AND job_date > CURRENT_DATE ''', (customer_id,))

    #     # Group jobs
    #     jobs = defaultdict(list)
    #     for job in futureServices:
    #         service_date = job[service_position.Service_Date]
    #         jobs[service_date].append(job)

    #     futureJobs = []
    #     for job in jobs.values():
    #         futureJobs.append(job[0])


    #     # Iterate over the jobs
    #     for i in range(1, len(futureJobs)):
    #         # Parse the job dates as datetime objects
    #         job_date1 = datetime.fromisoformat(futureJobs[i][1])
    #         job_date2 = datetime.fromisoformat(futureJobs[i-1][1])
    #         # Calculate the delta between the current job and the previous job
    #         delta = job_date1 - job_date2
    #         deltas.append(delta)

    #     # Calculate the average delta
    #     if len(deltas) > 0:
    #         total_seconds = sum(delta.total_seconds() for delta in deltas)
    #         average_delta = timedelta(seconds=total_seconds / len(deltas)).days
    #     else:
    #         average_delta = None

    #     return average_delta