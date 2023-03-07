from src.window_magic.objects.customer import Customer
from src.window_magic.objects.evaluator import Evaluation
from src.window_magic.objects.job import Job
import src.window_magic._resources as r
import csv
import copy
import math
import os

# ====================================================================================
# Output results as desired
# ====================================================================================

_evals_file = "completed_evaluations.csv"
_jh_file    = "analyzed_data_points.csv"


row_obj = {
    "id"                : None,
    "name"              : None,
    "address"           : None,
    "service"           : None,
    "price"             : None,
    "employees"         : None,
    "duration"          : None,
    "rate"              : None,
    "points"            : None,
    "price_variation"   : None
}

job_history_row = {
    "job_id"            : None,
    "customer_id"       : None,
    "customer_name"     : None,
    "services"          : None,
    "job_date"          : None,
    "price"             : None,
    "duration"          : None,
    "employee"          : None
}


def round_up_to_nearest_5(num):
    # Round up to the nearest integer
    rounded_num = math.ceil(num)
    # Divide by 5 and round up to the nearest integer
    rounded_num = math.ceil(rounded_num / 5.0) * 5
    # Return the rounded number
    return rounded_num

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

    def output_history_to_csv(self):
        with open(os.path.join(r.csv_location, _jh_file), mode='w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(job_history_row.keys())
            for customer in self.customer_and_services:
                printRow = copy.deepcopy(job_history_row)

                for services, eval in self.customer_and_services[customer].items():

                    eval: Evaluation = eval

                    if eval and eval.job_list:
                        for job in eval.job_list:
                            printRow = copy.deepcopy(job_history_row)
                            job: Job = job

                            printRow["job_id"]          = job.get_id()
                            printRow["customer_id"]     = customer.id
                            printRow["customer_name"]   = customer.name
                            printRow["services"]        = services
                            printRow["job_date"]        = job.date
                            printRow["price"]           = job.price
                            printRow["duration"]        = job.duration
                            printRow["employee"]        = job.employee
                            
                            writer.writerow(printRow.values())


    def output_to_csv(self):
        with open(os.path.join(r.csv_location,_evals_file) , mode='w', newline='') as file:
            writer = csv.writer(file)

            writer.writerow(row_obj.keys())
            for customer in self.customer_and_services:
                if self.customer_and_services[customer].values():
                    self.__add_to_csv(customer.id, writer)


    def __add_to_csv(self, customer_id, writer):
        rows = self.__convert_to_row(customer_id)
        
        for row in rows:
            writer.writerow(row.values())


    def __convert_to_row(self, customer_id):
        rows = []

        data = self.__retrieve_info(customer_id)

        customer: Customer = data[0]
        evals = data[1]


        for service_titles, evaluation in evals.items():
            evaluation :Evaluation = evaluation
            row = copy.deepcopy(row_obj)
            row["service"] = service_titles

            row["id"] = customer.id
            row["name"] = customer.name
            row["address"] = customer.address

            if evaluation:
                row["price"]          = evaluation.price
                row["rate"]           = evaluation.get_rate()
                row["duration"]       = round(evaluation.average_duration, 0)
                row["employees"]      = evaluation.get_employees()
                row["points"]         = evaluation.get_data_point_qty()

                if evaluation.flagged:
                    row["flagged"] = evaluation.flagged

            rows.append(row)
                
        return rows


    def __basics_to_console(self, customer_id, include_empties = False):
        print_string = ""
        # Retrieves the Customer and the Evalution to print
        data = self.__retrieve_info(customer_id)
        customer: Customer = data[0]
        services_evals = data[1]

        header_string = f"{customer.id} - {customer.name} ({customer.address}): \n"
        header_string = header_string + f"https://www.thecustomerfactor.com/customers_profile.php?id={customer.id}\n\n"
        
        for service_titles, evaluation in services_evals.items():
            if evaluation:
                price          = evaluation.price
                rate           = evaluation.get_rate()
                duration       = evaluation.average_duration
                employees      = evaluation.get_employees()
                data_points    = evaluation.get_data_point_qty()

                print_string   = print_string + f"\t{service_titles} for ${price}\n"
                print_string   = print_string + f"\t\tAccording to {employees}, this takes an average of {round(duration,0)} mins.\n"
                print_string   = print_string + f"\t\tThat is ${rate}/hr :: {data_points} points\n"
                
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
    