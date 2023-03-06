# Evaluates the job rate for jobs
# =================================================
from src.window_magic.databasing import assistant as wm_assistant
from src.window_magic.objects.customer import Customer
from src.window_magic.objects.evaluator import Evaluator
from src.window_magic.objects.evaluator import Evaluation
from src.window_magic.objects.job import Job

from collections import defaultdict
import statistics
from scipy.stats import zscore

# ====================================================================================
# Window Magic Filter Functions
# ====================================================================================
def __at_most_12_jobs(job_list):
    return job_list[:20]


def __consider_employees(job_list):
    """
    Filters the job rows to include only rows with an employee in the given list.
    """

    employees = {"Justin Smith", "Jose Perez", "Devony Dettman", "Roberto Isais", "Brandon Foster"}
    return [job for job in job_list if job.employee in employees]


def __remove_deliquents(job_list):
    if job_list:
        id = job_list[0].customer_id

        if id == 246: ## Viewing Mohnacky
            stdev = __calc_deviation(job_list)
            average = __calc_avg(job_list)
            z_scores = zscore(__get_durations(job_list))

            i = 0
            for job in job_list:
                job: Job = job
                z_score = __calc_z_score(job.duration, average, stdev)


                print(f"{i+1}. {round(z_scores[i], 4)}\t-- {job}")
                i = i+1

            print(f"\n-> Standard deviation: {stdev}")
            print(f"-> average: {average}\n")

    return job_list


def __calc_deviation(job_list):
    return statistics.stdev(__get_durations(job_list))


def __calc_avg(job_list):
    durations = __get_durations(job_list)

    center = round(len(durations)/2,None)

    return durations[center]

    # total = 0

    # for duration in durations:
    #     total = total + duration

    # return total / len(durations)


def __calc_z_score(duration, avg, sdev):
    return (duration-avg)/sdev


def __get_durations(job_list):
    durations = []

    for job in job_list:
            job: Job = job
            durations.append(job.duration)
    
    durations.sort
    return durations
    

# ====================================================================================
# Applied Filters - Note: Applies in order
# ====================================================================================

# Order sensitive
running_pre_filters = [
    __consider_employees,
    __at_most_12_jobs,
    __remove_deliquents,
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
