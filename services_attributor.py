from collections import defaultdict
from datetime import datetime
import db_generator as database


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


class Service:
    def __init__(self, serviceDate, completedJob):
        self.job        = completedJob

        self.title      = self.__extractServiceTitles(completedJob)
        self.price      = self.__extractPrice(completedJob)
        self.duration   = self.__extractDuration(completedJob)
        self.employee   = self.__extractEmployees(completedJob)
        self.date       = serviceDate
        self.frequency  = self.__determineFrequency()



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
                    print("[ERROR] check duration params for {} service on {} for {}".format(
                        service[Service_Type], 
                        service[Service_Date], 
                        service[Customer_Id]))
                    return None
            
        return totalDuration


    def __extractServiceTitles(self, job):
        serviceNames = []
        for service in job:
            name = service[Service_Type]

            if service not in serviceNames:
                serviceNames.append(name)

        return serviceNames


    def __determineFrequency(self):
        return None
    

    


## Service Object
class ServiceOf:
    def __init__(self, customer_id):
        self.customer_id          = customer_id
        self.customer_name        = database.getCustomerName(customer_id)
        self.services             = []   # List of CompleteService object
        self.serviceHistory       = defaultdict(list)   # List of considered jobs, according to __justinsStandard()

        ## How the service gets defined
        self.__justinsStandard()

    considerEmp = [
        'Devony Dettman',
        'Justin Smith',
        # 'Roberto Isais',
        'Jose Perez',
        # 'Isais'
    ]

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



    def __justinsStandard(self, maxHistoryQty = 12, considerEmployees = considerEmp, considerFrequency = considerFreq):
        entireServiceHistory = serviceHistory(self.customer_id)
        i = 0

        # Iterate through service history from latest to oldest, as far back as maxHistory
        # "servicesDetails" are grouped by services performed on the same day, 
            # For example, Windows and partions were performed on 1-1-2020.  
        # Only retrieves jobs from the past.
        for service_date, serviceDetails in entireServiceHistory.items():

            # Defines Window Magic's contract, how long it took, and which employees were involved.
            completedService = Service(service_date, serviceDetails)

            # [FILTER] Employee is a considered employee.
            # [FILTER] Get a max of maxHistoryQty jobs. Continue gathering data until maxHistoryQty or history runs out.
            employee = completedService.employee
            if employee in considerEmployees and employee != 'None':
                if i < maxHistoryQty:
                    totalPrice = completedService.price
                    totalDuration = completedService.duration

                    # [DATA QUALITY FILTER] Only consider if totalDuration and totalPrice have been identified
                    if totalDuration and totalPrice:
                        i = i+1

                        # Archive service details performed on given date
                        self.serviceHistory[service_date] = serviceDetails

                        # Save Service for evaluation
                        self.services.append(completedService)

                else:
                    return
    

    def __str__(self):
        printString = ""

        i = 1
        print("For {} - {}:".format(self.customer_id, self.customer_name))

        if len(self.services) > 0:
            for service in self.services:
                service: Service = service

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

        for service in self.services:
            service: Service = service # Type casting

            key = str(service.title)
            price = service.price
            duration = service.duration

            # Begin grouping by similar jobs
            if not evaluations[key]: # (price, duration, service_count)
                evaluations[key]= (price, duration, 1)
                continue

            # Combine to existing
            else:
                # Add new info to services
                pdq = evaluations[key]

                if price == pdq[0]:
                    nDuration = pdq[1] + duration
                    serviceCount =  pdq[2] + 1

                    evaluations[key] = (pdq[0], nDuration, serviceCount)
                else:
                    print('[!]Price mismatch: {} - ${}, incoming -> ${}'.format(key, pdq[0], price))

        print("{} gets the following done: ".format(self.customer_name))
        for title, job in evaluations.items():
            price = job[0]
            allDuration = job[1]
            jobCount = job[2]

            avgDuration = allDuration/jobCount
            rate = price/(avgDuration/60)

            print("{} for ${} and takes an avg. {}mins - Data count: {}".format(title, price, round(avgDuration), jobCount))
            print("That is ${} per hour".format(round(rate, 2)))


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
