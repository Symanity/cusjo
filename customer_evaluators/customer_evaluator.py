from collections import defaultdict
from datetime import datetime, timedelta
import cf_interpreters.db_generator as database
import cf_interpreters.cf_converter as inter
import customer_evaluators.jc_db_generator as jc_database


## REFERENCE Job object as returned from SQL queries
    # customer_id = job[0]
    # jobDate = job[1]
    # jobType = job[2]
    # jobPrice = job[3]
    # employee = job[4]
    # jobDuration = job[5]
    # jobFrequency = job[7]

Customer_Id = 0
Service_Date = 1
Service_Type = 2
Service_Price = 3
Employee = 4
Service_Duration = 5
# Invoice = 6
Service_Frequency = 7

_daily          = 'daily'
_weekly         = 'weekly'
_2weeks         = '2 weeks'
_3weeks         = '3 weeks'
_monthly        = 'monthly'
_6weeks         = '6 weeks'
_2months        = '2 months'
_quarterly      = 'quarterly'
_semi_annually  = 'semi-annually'
_yearly         = 'yearly'
_2years         = '2 years'


considerEmp = [
    # "Justin Smith",
    # "Devony Dettman",
    "Roberto Isais",
    "Isais",
    # "Jose Perez",
    # "Nolan Barraza",
    # "Dallas Wright",
    # "Skyler Gibbs",
    # "Adam Ruiz",
    # "Brandon Foster",
    # "Evans Richie",
    # "Danny Steinweg",
    # "Oliver Munroe",
    # "Tim Grant"
]

maxHistoryQTY = 12

## Service Object
class ServiceOf:
    def __init__(self, customer_id):
        self.customer_id          = customer_id
        self.customer_name        = database.getCustomerName(customer_id)
        self.customer_address     = database.getCustomerAddress(customer_id)
        self.jobs             = []   # List of Service object
        self.jobHistory       = defaultdict(list)   # List of considered jobs, according to __justinsStandard()

        ## How the service gets defined
        self.__justinsStandard()
        self.evaluations          = None

    
    considerFreq = [
        _daily, 
        _weekly,
        _2weeks, 
        _3weeks,
        _monthly,
        _6weeks,
        _2months,
        _quarterly,
        _semi_annually,
        _yearly,
        _2years
    ]


    def __justinsStandard(self, maxHistoryQty = maxHistoryQTY, considerEmployees = considerEmp, considerFrequency = considerFreq):
        entireServiceHistory = serviceHistory(self.customer_id)
        i = 0

        # Iterate through service history from latest to oldest, as far back as maxHistory
        # "servicesDetails" are grouped by services performed on the same day, 
            # For example, Windows and partions were performed on 1-1-2020.  
        # Only retrieves jobs from the past.

        for service_date, serviceDetails in entireServiceHistory.items():
            # Defines Window Magic's contract, how long it took, and which employees were involved.
            completedJob = TheJob(service_date, serviceDetails)

            # [FILTER] Employee is a considered employee.
            # [FILTER] Get a max of maxHistoryQty jobs. Continue gathering data until maxHistoryQty or history runs out.
            employee = completedJob.employee
            if employee in considerEmployees and employee != 'None':
                if i < maxHistoryQty:
                    totalPrice = completedJob.price
                    totalDuration = completedJob.duration

                    # [DATA QUALITY FILTER] Only consider if totalDuration and totalPrice have been identified
                    if totalDuration and totalPrice:
                        i = i+1

                        # Archive service details performed on given date
                        self.jobHistory[service_date] = serviceDetails

                        # Save Service for evaluation
                        self.jobs.append(completedJob)

                else:
                    break

    def __str__(self):
        printString = ""

        i = 1
        print("{} - {}:".format(self.customer_id, self.customer_name))

        if len(self.jobs) > 0:
            for service in self.jobs:
                service: TheJob = service

                printString = printString + "\t{}. {} completed {} on {} for ${} and took {}mins.\n".format(
                    i,
                    service.employee,
                    service.title,
                    service.date,
                    service.price,
                    service.duration
                )
                i = i+1

            return printString

        else:
            return "\tNo valuable data :("


    # What service do we do for the customer?
    # How long does it take us to do it?
    # How much are we charging them for it?
    def evaluate(self):
        evaluations = defaultdict(list)

        for job in self.jobs:
            job: TheJob = job # Type casting

            key = str(job.title)
            price = job.price
            duration = job.duration
            frequency = job.frequency

            # Begin grouping by similar jobs
            eval: Evaluation = evaluations[key]
            if not eval: # Initiate if incountering a new service requirement
                eval = Evaluation(job.title, price, frequency)
                eval.addDuration(duration)
                eval.addEmployee(job.employee)
                evaluations[key] = eval
                continue

            else: # Combine to existing service
                priceOnRecord = eval.price

                if price == priceOnRecord:
                    eval.addDuration(duration)
                    eval.addEmployee(job.employee)

                elif price > priceOnRecord:
                    print('[PRICE MISMATCH] {} {} : {} we charge ${} now, we used to charge ${}. Price changed since {}\n'.format(
                        self.customer_name, 
                        self.customer_address,
                        key,
                        eval.price, 
                        price, 
                        job.date))

        vals = evaluations.values()
        self.evaluations = vals if vals else []

        return self.evaluations

# id, name, services, job_date, price, duration, employee
class TheJob:
    def __init__(self, serviceDate, completedJob):
        self.job        = completedJob

        self.title      = self.__extractServiceTitles(completedJob)
        self.price      = self.__extractPrice(completedJob)
        self.duration   = self.__extractDuration(completedJob)
        self.employee   = self.__extractEmployees(completedJob)
        self.date       = serviceDate
        self.frequency  = convertFrequency(self.__determineFrequency())



  ## ** For the Following function -> Extraction of data takes in servicesPerformed on a single day **
    # Get the employee(s) that were assigned to be on site.
    def __extractEmployees(self, job):
        employee = None
        for service in job:
            sus = service[Employee]

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
            servicePrice = service[Service_Price]

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
            duration = service[Service_Duration]

            if duration:
                if not totalDuration:
                    totalDuration = duration

                if totalDuration != duration:
                    customerName = database.getCustomerName(service[Customer_Id])
                    address = database.getCustomerAddress(service[Customer_Id])
                    # print("[!] {} vs. {} -- check duration for {} service on {} for {}:{}".format(
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
            name = service[Service_Type]

            if service not in serviceNames:
                serviceNames.append(name)

        return serviceNames


    def __determineFrequency(self):
        customer_id = self.job[0][Customer_Id]
        deltas = []

        futureServices = database.ask(''' SELECT * FROM JOB_HISTORY WHERE customer_id = ? AND job_date > CURRENT_DATE ''', (customer_id,))

        # Group jobs
        jobs = defaultdict(list)
        for job in futureServices:
            service_date = job[Service_Date]
            jobs[service_date].append(job)

        futureJobs = []
        for job in jobs.values():
            futureJobs.append(job[0])


        # Iterate over the jobs
        for i in range(1, len(futureJobs)):
            # Parse the job dates as datetime objects
            job_date1 = datetime.fromisoformat(futureJobs[i][1])
            job_date2 = datetime.fromisoformat(futureJobs[i-1][1])
            # Calculate the delta between the current job and the previous job
            delta = job_date1 - job_date2
            deltas.append(delta)

        # Calculate the average delta
        if len(deltas) > 0:
            total_seconds = sum(delta.total_seconds() for delta in deltas)
            average_delta = timedelta(seconds=total_seconds / len(deltas)).days
        else:
            average_delta = None

        return average_delta


class Evaluation:
    def __init__(self, title, price, frequency) -> None:
        self.serviceTitle = title
        self.price = price           
        self.__duration = 0          
        self.dataCount = 0
        self.frequency = frequency
        self.employees = [] 

    def addDuration(self, val):
        self.__duration = self.__duration + val
        self.dataCount = self.dataCount + 1
    
    def addEmployee(self, val):
        if not val in self.employees:
            self.employees.append(val)
        

    def getAvgDuration(self):
        return round(self.__duration/self.dataCount)

    def getRate(self):
        return round(self.price/(self.getAvgDuration()/60), 2)

    def __str__(self) -> str:
        string = "\tAccording to: {}\n".format(self.employees)
        string = string + "\t{} {} and takes an avg. {}mins - Data count: {}\n".format(
            self.serviceTitle, 
            self.frequency, 
            self.getAvgDuration(), 
            self.dataCount)

        string = string+"\tThat is ${} per hour.".format(self.getRate())
        return string


# Combines Services which were done at the same time for the same customer.
# Example: Interior/Exterior and partitions.
# Returns key/value pair. {service_date:[list of services_performed]}
def serviceHistory(customer_id):
    # Get complete customer history in descending order according to date.
    # Latest to oldest (*Only gets history from past jobs. Does NOT consider upcoming jobs)
    serviceHistory = database.getCustomerHistory(customer_id) 
    
    # Group jobs
    completeService = defaultdict(list)
    for service in serviceHistory:
        service_date = service[Service_Date]
        completeService[service_date].append(service)


    return completeService


def convertFrequency(frequencyNum):
    if not frequencyNum:
        return None
    else:
        # Daily
        if frequencyNum > 0 and frequencyNum < 3:
            return 'daily'
        # weekly
        elif frequencyNum >= 3 and frequencyNum < 10:
            return 'weekly'
        # two weeks
        elif frequencyNum >= 10 and frequencyNum < 18:
            return '2 weeks'
        # three weeks
        elif frequencyNum >= 18 and frequencyNum < 25:
            return '3 weeks'
        # monthly
        elif frequencyNum >= 25 and frequencyNum < 40:
            return 'monthly'
        # 6 weeks
        elif frequencyNum >= 40 and frequencyNum < 48:
            return '6 weeks'
        # bi-monthly
        elif frequencyNum >= 48 and frequencyNum < 75:
            return '2 months'
        # quarterly
        elif frequencyNum >= 75 and frequencyNum < 130:
            return 'quarterly'
        # semi-yearly
        elif frequencyNum >= 130 and frequencyNum < 250:
            return 'semi-annually'
        # Yearly
        elif frequencyNum >= 250 and frequencyNum < 500:
            return 'yearly'

        # bi-yearly
        elif frequencyNum >= 500 and frequencyNum < 800:
            return '2 years'

def initEvaluations(customerList):
    WM_commerical_jobs = []
    activeCustomers = customerList
    print('[Running] Gathering Jobs...')
    for customer in activeCustomers:
        id = customer[0]
        theService = ServiceOf(id)
        WM_commerical_jobs.append(theService)
    print('[STATUS] finished gathering {} jobs'.format(len(WM_commerical_jobs)))

    # Create table
    # id, name, address, services, job_date, price, duration, employee
    considerJobs = []
    for job in WM_commerical_jobs:
        job: ServiceOf = job
        id = job.customer_id
        name = job.customer_name
        address = job.customer_address
        for pastJob in job.jobs:
            pastJob: TheJob = pastJob
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
            considerJobs.append(considerJob)

    if considerJobs:
        jc_database.create(considerJobs)
        jc_database.writeCSV()
        

    print("[Running] Beginning Evalulations...")
    for job in WM_commerical_jobs:
        job: ServiceOf = job

        job.evaluate()

    print('\tdone.')
    return WM_commerical_jobs


print('[Running] Filters check...')
print('[Filter] Considering employees {}'.format(considerEmp))
print('[Filter] Gather at most {} past jobs'.format(maxHistoryQTY))
print('[Filter] Skip jobs with NO DURATION and/or NO PRICE'.format())