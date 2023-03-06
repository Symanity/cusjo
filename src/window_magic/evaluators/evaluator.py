# Evaluates the job rate for jobs
# =================================================
from src.window_magic.databasing import assistant as wm_assistant
from src.window_magic.objects.customer import Customer
from src.window_magic.objects.evaluator import Evaluator
from src.window_magic.objects.evaluator import Evaluation
from src.window_magic.objects.job import Job

from collections import defaultdict


# ====================================================================================
# Window Magic Filters
# ====================================================================================
def __at_most_12_jobs(job_list):
    return job_list[:12]


def __consider_employees(job_list):
    """
    Filters the job rows to include only rows with an employee in the given list.
    """

    employees = {"Justin Smith", "Jose Perez", "Devony Dettman", "Roberto Isais", "Brandon Foster"}
    return [job for job in job_list if job.employee in employees]


def __print_job(job_list):
    for job in job_list:
        print(job)


# ====================================================================================
# Evaluator functions
# ====================================================================================
def evaluate_all():
    services_evaluations = defaultdict(list)

    # Execute a query to retrieve all unique customers
    customer_list = wm_assistant.list_customers()

    for customer_row in customer_list:
        customer = Customer(customer_row[0])

        services_evaluations[customer] = __generate_evals(customer)

    return services_evaluations


## Returns Evaluation Object
def evaluate(customer_id):
    services_evaluations = defaultdict(list)
    customer = Customer(customer_id)

    services_evaluations[customer] = __generate_evals(customer)

    return services_evaluations


def __generate_evals(customer):
    evaluator:Evaluator = customer.get_evaluator()
        
    evaluator.apply_pre_filter(__consider_employees)
    evaluator.apply_pre_filter(__at_most_12_jobs)

    # evaluator.apply_post_filter(__show_only_if_below_min_price)

    services_evals = evaluator.get_evaluations(True)

    return services_evals
