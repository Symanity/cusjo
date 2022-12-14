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


## Service Object
class OurService:
    def __init__(self, customer_id):
        self.customer_id          = customer_id
        self.employeesInvolved    = []
        self.prices               = []
        self.durations            = []
        self.serviceNames         = []
        self.services             = []

        print('Verifying {} ...'.format(customer_id))
        self.__justinsStandard()
        try:
            self.__validateSelf()
            print('clean')
        except:
            print('error has occured during evaluation of {}'.format(customer_id))


    def __justinsStandard(self, maxHistory = 12, ommitEmployees = None):
        entireServiceHistory = serviceHistory(self.customer_id)
        i = 0
        for service_date, services in entireServiceHistory.items():
            employee = self.__extractEmployees(services)
            totalPrice = self.__extractPrice(services)
            totalDuration = self.__extractDuration(services)
            serviceNames = self.__extractServices(services)

            # Iterate through service history from latest to oldest, as far back as maxHistory
            # Only consider if totalDuration and totalPrice has been identified
            if i < maxHistory:
                if totalDuration and totalPrice:
                    i = i+1
                    # Record services performed
                    self.services.append(services)

                    # Capture employee if needed
                    if employee not in self.employeesInvolved:
                        self.employeesInvolved.append(employee)    
                    
                    # Store totalPrice
                    if totalPrice not in self.prices:
                        self.prices.append(totalPrice)
                    
                    # Store duration
                    self.durations.append(totalDuration)

                    # Strore Service Names
                    if serviceNames not in self.serviceNames:
                        self.serviceNames.append(serviceNames)

            else:
                break

    
    def getPrice(self):
        if len(self.prices) == 1:
            return self.prices[0]
        else:
            print('[!] Multiple prices detected for {}... returning latest price'.format(self.customer_Id))
            return self.prices[0]

    def getAvgDuration(self):
        total = 0
        for duration in self.durations:
            total = total + duration

        return total/len(self.durations)

    def getHourlyRate(self):
        timeMins = self.getAvgDuration()
        price = self.getPrice()
        timeHr = timeMins/60

        return price/timeHr

    def __validateSelf(self):
        if not len(self.durations) == len(self.services):
            raise Exception("Unable to validate. Job unsyncronized.")

        if len(self.prices) > 1:
            raise Exception("Multiple prices detected.")

    ## Get the employee(s) that were assigned to be on site.
    def __extractEmployees(self, servicesPerformed):
        employee = None
        for service in servicesPerformed:
            sus = service[Employee]

            if not employee:
                employee = sus

            elif employee != sus:
                print("[ERROR] check employee params for service on {} for {}".format(service[Service_Date], service[Customer_Id]))
                return None

        return employee


    def __extractPrice(self, servicesPerformed):
        totalPrice = 0
        for service in servicesPerformed:
            servicePrice = service[Service_Price]

            if servicePrice:
                totalPrice += servicePrice
            else:
                print("[ERROR] check price params for service on {} for {}".format(service[Service_Date], service[Customer_Id]))
                return None

        return totalPrice

    # Duration gets applied equally to all services performed at the same time.
    # For example, if three services were performed for a total of 1hr. CF applies 1hr to all three services. 
    def __extractDuration(self, servicesPerformed):
        totalDuration = None
        for service in servicesPerformed:
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


    def __extractServices(self, servicesPerformed):
        serviceNames = []
        for service in servicesPerformed:
            name = service[Service_Type]

            if service not in serviceNames:
                serviceNames.append(name)

        return serviceNames


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



# Combines Services which were done at the same time for the same customer.
# Example: Interior/Exterior and partitions.
# Returns key/value pair. {service_date:[list of services_performed]}
def serviceHistory(customer_id):
    # Get complete customer history in descending order according to date.
    # Latest to oldest
    serviceHistory = database.getCustomerHistory(customer_id) 
    
    # Group jobs
    completeService = defaultdict(list)
    for service in serviceHistory:
        service_date = service[Service_Date]
        completeService[service_date].append(service)


    return completeService
