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


class CompleteService:
    def __init__(self, serviceDate, completedJob) -> None:
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
        self.employeesInvolved    = []
        # For the below dictionaries, Service_date serves as the key
        self.prices               = defaultdict(list)
        self.durations            = defaultdict(list)
        self.serviceNames         = defaultdict(list)
        self.services             = defaultdict(list)

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



    def __justinsStandard(self, maxHistory = 12, considerEmployees = considerEmp, considerFrequency = considerFreq):
        entireServiceHistory = serviceHistory(self.customer_id)
        i = 0

        # Iterate through service history from latest to oldest, as far back as maxHistory
        # "services" are grouped by services performed on the same day
        for service_date, services in entireServiceHistory.items():
            completeService = CompleteService(service_date, services)
            employee = completeService.employee
            # serviceFq = self.__extractFrequency(services)

            # Only consider if totalDuration and totalPrice have been identified
            if employee in considerEmployees and employee != 'None':
            # if employee in considerEmployees and employee != 'None' and serviceFq in considerFrequency:
                if i < maxHistory:
                    totalPrice = completeService.price
                    totalDuration = completeService.duration
                    serviceNames = completeService.title

                    print("considering job on {}".format(service_date))

                    if totalDuration and totalPrice:
                        i = i+1
                        # Record services performed
                        self.services[service_date] = services

                        # Capture employee if needed
                        if employee not in self.employeesInvolved:
                            self.employeesInvolved.append(employee)
                        
                        # Store totalPrice
                        self.prices[service_date] = totalPrice
                        
                        # Store duration
                        self.durations[service_date] = totalDuration

                        # Store Service Names
                        self.serviceNames[service_date] = serviceNames

                else:
                    return
    

    def __str__(self):
        price = self.getPrice()
        avgDuration = self.getAvgDuration()
        printString = "{} pays {} and takes \n{} \nan average of \n{} mins to complete\n{}.\nThat is a rate of ${} per hour".format(
            self.customer_id,
            price,
            self.employeesInvolved,
            round(avgDuration),
            self.serviceNames,
            round(self.getHourlyRate(), 2))

        return printString


# What service do we do for the customer?
# How long does it take us to do it?
# How much are we charging them for it?
def evaluate(OurService, customerName=""):
    toService = defaultdict(list)
    for date, services in OurService.serviceNames.items():
        key = str(services)
        price = OurService.prices[date]
        duration = OurService.durations[date]

        # Set the different jobs specifications if not set yet
        val = toService[key]
        if not val: # (price, duration, service_count)
            toService[key]= (price, duration, 1)
            # print("added {} -> {}".format(key, toService[key]))
            continue

        else:
            # Add new info to services
            pdq = toService[key]

            if price == pdq[0]:
                nDuration = pdq[1] + duration
                serviceCount =  pdq[2] + 1

                toService[key] = (pdq[0], nDuration, serviceCount)
            else:
                print('[!]Price mismatch: {} - ${}, incoming -> ${}'.format(key, pdq[0], price))

    print("{} gets the following done: ".format(customerName))
    for title, job in toService.items():
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
