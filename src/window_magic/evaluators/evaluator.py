# Evaluates the job rate for jobs
# =================================================
from src.window_magic.databasing import assistant as wm_assistant
from src.window_magic.objects.customer import Customer
from src.window_magic.objects.evaluator import Evaluator
from src.window_magic.objects.evaluator import Evaluation
from src.window_magic.objects.job import Job

from collections import defaultdict

from src.window_magic.evaluators import filter_tools as tools

# ====================================================================================
# Window Magic Filter Functions
# ====================================================================================
def __at_most_12_jobs(job_list):
    """
    Gathers first 12 of the remaining job list (most recent to latest)
    """
    return job_list[:12]


def __consider_employees(job_list):
    """
    Filters the job rows to include only rows with an employee in the list.
    Justin, Devony, Roberto, Brandon
    """

    employees = {"Justin Smith", "Jose Perez", "Devony Dettman", "Roberto Isais", "Brandon Foster"}
    return [job for job in job_list if job.employee in employees]


EVALUATE_CUSTOMER = None
def __remove_deliquents(job_list):
    """
    Uses the z-score method derived from a deviation of average values.
    This uses the statistics library from https://scipy.org/
    """
    max_score = 1
    sd_multiplier = 50
    jobs = job_list
    
    if jobs:
        id = jobs[0].customer_id

        if id == EVALUATE_CUSTOMER:
            stdev = tools.calc_standard_deviation(jobs,sd_multiplier)
            average = tools.calc_job_average(jobs)
            z_scores = tools.get_zscore(jobs, sd_multiplier)

            print("======================================================")
            print("z-score\t-- services - date - price - duration - tech")
            print("======================================================")
            i = 0
            for job, score in z_scores.items():
                job: Job = job

                if score > max_score or score < -max_score:
                    print(f"{i+1}. {round(score, 4)}\t-- {job}\t<- REMOVED")
                    jobs.remove(job)
                else:
                    print(f"{i+1}. {round(score, 4)}\t-- {job}")
                i = i+1

            print(f"\n-> Standard deviation: {stdev}")
            print(f"-> average: {average}mins\n")

        else:
            jobs = tools.perform_removal(jobs, max_score, sd_multiplier)

    return jobs




# ====================================================================================
# Applied Filters - Note: Applies in order
# ====================================================================================

# Order sensitive
running_pre_filters = [
    __consider_employees,
    __remove_deliquents,
    __at_most_12_jobs,
]

running_post_filters = [
    
]

# ====================================================================================
# Evaluator functions
# ====================================================================================
def evaluate(customer_id = None):
    if customer_id:
        return __evaluate(customer_id)

    else:
        return __evaluate_all()
    

def __evaluate_all():
    services_evaluations = defaultdict(list)

    # Execute a query to retrieve all unique customers
    customer_list = wm_assistant.list_customers()

    for customer_row in customer_list:
        customer_id = customer_row[0]
        customer = Customer(customer_id)

        services_evaluations[customer] = __generate_evals(customer)

    return services_evaluations


def __evaluate(customer_id):
    services_evaluations = defaultdict(list)
    customer = Customer(customer_id)

    services_evaluations[customer] = __generate_evals(customer)

    return services_evaluations

        

def __generate_evals(customer:Customer):
    evaluator:Evaluator = customer.get_evaluator()
        
    for pre_filter in running_pre_filters:
        evaluator.apply_pre_filter(pre_filter)

    for post_filter in running_post_filters:
        evaluator.apply_post_filter(post_filter)

    services_evals = evaluator.get_evaluations(True)

    return services_evals
