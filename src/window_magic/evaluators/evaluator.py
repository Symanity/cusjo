# Evaluates the job rate for jobs
# =================================================
from src.window_magic.databasing import assistant

## Returns Evaluation Object
def evaluate_customer(customer_id):
    pass

## Returns a list of Evaluations Objects
def evaluate_all(job_list=None):
    # Execute a query to retrieve all unique customers
    query = f"SELECT DISTINCT customer_name FROM {assistant.job_table}"
    customer_rows = assistant.query(query)

    # Iterate over each customer and retrieve their jobs with price and duration
    for row in customer_rows:
        customer_name = row[0]
        query = f"SELECT * FROM {assistant.job_table} WHERE customer_name= ? AND price > 0 AND duration > 0"
        job_rows = assistant.query(query, (customer_name,))
        
        # Print out the results
        print(f"Jobs for {customer_name}:")
        for job_row in job_rows:
            customer_id, customer_name, customer_address, services, job_date, price, duration, employee = job_row
            print(f"- {services} on {job_date} by {employee} for {price} ({duration} minutes)")
        print()

        pass

class Evaluation:
    def __init__(self, titles, price, frequency) -> None:
        self.serviceTitle = titles
        self.price = price
        self._duration = 0
        self.data_count = 0
        self.frequency = frequency
        self.employees = []

    def addDuration(self, val):
            self.__duration = self.__duration + val
            self.data_count = self.data_count + 1
    
    def addEmployee(self, val):
        if not val in self.employees:
            self.employees.append(val)
        

    def getAvgDuration(self):
        return round(self.__duration/self.data_count)

    def getRate(self):
        return round(self.price/(self.getAvgDuration()/60), 2)

    def __str__(self) -> str:
        string = "\tAccording to: {}\n".format(self.employees)
        string = string + "\t{} {} and takes an avg. {}mins - Data count: {}\n".format(
            self.serviceTitle, 
            self.frequency, 
            self.getAvgDuration(), 
            self.data_count)

        string = string+"\tThat is ${} per hour.".format(self.getRate())
        return string