# Evaluates the job rate for jobs
# =================================================
from src.window_magic.databasing import assistant as wm_assistant
from src.window_magic.objects.customer import Customer
from src.window_magic.objects.evaluator import Evaluator
from src.window_magic.objects.evaluator import Evaluation
from src.window_magic.objects.job import Job
from collections import defaultdict
import math


# ====================================================================================
# Window Magic Filters
# ====================================================================================
ideal_employee_rate = 105

def __at_most_12_jobs(job_list):
    return job_list[:12]


def __consider_employees(job_list):
    """
    Filters the job rows to include only rows with an employee in the given list.
    """

    employees = {"Justin Smith", "Jose Perez", "Devony Dettman, Roberto Isais, Brandon Foster"}
    return [job for job in job_list if job.employee in employees]


# Post Filter
def __show_only_if_below_min_price(evaluation: Evaluation):
    if evaluation.get_rate() < 105:
        return evaluation

    else:
        return None

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

    evaluator.apply_post_filter(__show_only_if_below_min_price)

    services_evals = evaluator.get_evaluations(True)

    return services_evals

    
def round_up_to_nearest_5(num):
    # Round up to the nearest integer
    rounded_num = math.ceil(num)
    # Divide by 5 and round up to the nearest integer
    rounded_num = math.ceil(rounded_num / 5.0) * 5
    # Return the rounded number
    return rounded_num

# ====================================================================================
# Output results as desired
# ====================================================================================
class Outputer:
    def __init__(self, evaluations) -> None:
        self.customer_and_services = evaluations


    def output_to_console(self, customer_id = None, include_empties = False):
        """
        Purpose: Print customer information to the console

        Input:
            - customer_id (optional): The ID of the customer to print information for. Default is None.
            - include_empties (optional): Whether to include empty values in the output. Default is False.

        """
        a_string = ""
        if customer_id:
            return self.__basics_to_console(customer_id, include_empties)
        else:
            for customer in self.customer_and_services:
                if self.customer_and_services[customer].values():
                    output = self.__basics_to_console(customer.id, include_empties)
                    if output:
                        a_string = a_string + output + "\n"

            return a_string



    def output_to_csv(self, customer_id = None):
        pass


    def __basics_to_console(self, customer_id, include_empties = False):
        print_string = ""
        # Retrieves the Customer and the Evalution to print
        data = self.__retrieve_info(customer_id)
        customer: Customer = data[0]
        services_evals = data[1]

        header_string = f"{customer.id} - {customer.name} ({customer.address}): \n"
        header_string = header_string + f"https://www.thecustomerfactor.com/customers_profile.php?id={customer.id}\n"
        
        for service_titles, evaluation in services_evals.items():
            if evaluation:
                price          = evaluation.price
                rate           = evaluation.get_rate()
                duration       = evaluation.average_duration
                employees      = evaluation.get_employees()
                data_points    = evaluation.get_data_point_qty()
                correct_price  = evaluation.calculate_new_price(ideal_employee_rate)

                print_string   = print_string + f"\t{service_titles} for ${price}\n"
                print_string   = print_string + f"\t\tAccording to {employees}, this takes an average of {round(duration,0)} mins.\n"
                print_string   = print_string + f"\t\tThat is ${rate}/hr :: {data_points} points\n"

                print_string   = print_string + f"\t\tFOR A RATE OF ${ideal_employee_rate}/hr, PRICE JOB @ ${round_up_to_nearest_5(correct_price)}"
                
                print_string   = print_string + "\n"

            elif include_empties:
                print_string = print_string + f"\t{service_titles} - HAS INSUFFICIENT DATA\n"


        if print_string:
            return header_string+print_string
        

    def __retrieve_info(self, customer_id):
        for customer, services_evals in self.customer_and_services.items():
            if customer.id == customer_id:
                return [customer, services_evals]
            
        return None
    