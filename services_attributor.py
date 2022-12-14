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
class OurServiceOf:
    def __init__(self, customer_id):
        self.customer_id          = customer_id
        self.employeesInvolved    = []
        self.prices               = defaultdict(list)
        self.durations            = defaultdict(list)
        self.serviceNames         = defaultdict(list)
        self.services             = defaultdict(list)

        ## How the service gets defined
        self.__justinsStandard()


    def __justinsStandard(self, maxHistory = 12, ommitEmployees = []):
        entireServiceHistory = serviceHistory(self.customer_id)
        i = 0

        # Iterate through service history from latest to oldest, as far back as maxHistory
        # "services" are grouped by services performed on the same day
        for service_date, services in entireServiceHistory.items():
            employee = self.__extractEmployees(services)

            # Only consider if totalDuration and totalPrice have been identified
            if employee not in ommitEmployees:
                if i < maxHistory:
                    totalPrice = self.__extractPrice(services)
                    totalDuration = self.__extractDuration(services)
                    serviceNames = self.__extractServices(services)

                    if totalDuration and totalPrice:
                        i = i+1
                        # Record services performed
                        self.services[service_date].append(services)

                        # Capture employee if needed
                        if employee not in self.employeesInvolved:
                            self.employeesInvolved.append(employee)
                        
                        # Store totalPrice
                        self.prices[service_date].append(totalPrice)
                        
                        # Store duration
                        self.durations[service_date].append(totalDuration)

                        # Store Service Names
                        self.serviceNames[service_date].append(serviceNames)

                else:
                    return
    

    ## Get the employee(s) that were assigned to be on site.
    def __extractEmployees(self, servicesPerformed):
        employee = None
        for service in servicesPerformed:
            sus = service[Employee]

            if not employee and sus:
                employee = sus
                break

        if employee:
            return employee

        else:
            return "Unknown"

    def __extractPrice(self, servicesPerformed):
        totalPrice = 0
        for service in servicesPerformed:
            servicePrice = service[Service_Price]

            if servicePrice:
                totalPrice += servicePrice

        if totalPrice > 0:
            return totalPrice
        
        return None

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
