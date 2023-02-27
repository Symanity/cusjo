# Evaluates the job rate for jobs
# =================================================
from src.window_magic.databasing import assistant
from src.window_magic.objects.customer import Customer
from src.window_magic.objects.evaluator import Evaluator
from collections import defaultdict


# ===========================================
#   Retrieve Evaluations for all customers
#   pre: A list of the customer to evaluate
#   post: A list of evaluations for each customer
# ===========================================
# def evaluate_all():
#     """

#     """
#     focused_data = defaultdict(list)

#     # Execute a query to retrieve all unique customers
#     customer_list = assistant.list_customers()

#     # Iterate over each customer and retrieve their jobs with price and duration
#     for customer in customer_list:
#         customer_id = customer[0]
#         job_rows = assistant.get_completed_jobs(customer_id)

#         employees = ["Justin Smith", "Jose Perez", "Devony Dettman"]
#         job_rows = filter_jobs_by_employee(job_rows, employees)
        
#         # Print out the results
#         print_results(customer_id, job_rows, customer[1])
        

def evaluate_all():
    evaluations = defaultdict(list)

    # Execute a query to retrieve all unique customers
    customer_list = assistant.list_customers()

    for customer_row in customer_list:
        customer = Customer(customer_row[0])

        evaluator:Evaluator = customer.get_evaluator()

        evaluator.apply_filter(__consider_employees)
        evaluator.apply_filter(__at_most_12_jobs)

        
        evaluations[customer] = evaluator.get_evaluations()


def __at_most_12_jobs(job, job_list):
    if len(job_list) < 12:
        return job

def print_results(customer_name, job_rows, id):
    if len(job_rows) > 0:
        print(f"Jobs for {customer_name}: {id}")

        for job_row in job_rows:
            customer_id, customer_name, customer_address, services, job_date, price, duration, employee = job_row
            print(f"- {services} on {job_date} by {employee} for {price} ({duration} minutes)")
        print()


def __consider_employees(job, job_list):
    """
    Filters the job rows to include only rows with an employee in the given list.
    """

    employees = ["Justin Smith", "Jose Perez", "Devony Dettman"]
    pass
    # return [job for _job in job_list if job_list[-1] in employees]


## Returns Evaluation Object
def evaluate_customer(customer_id):
    pass