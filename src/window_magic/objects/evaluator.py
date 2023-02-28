from src.window_magic.objects import job as job_assistant
import copy


class Evaluation:
    def __init__(self, job_list) -> None:
        self.job_list = job_list
        self.price = self.__determine_price()
        self.average_duration = self.__determine_avg_duration()


    def __determine_price(self):
        priceOnRecord = None

        for job in self.job_list:
            job: job_assistant.Job = job

            if not priceOnRecord:
                priceOnRecord = job.price

            elif priceOnRecord < job.price:
                print(f'[ERROR] PRICE MISMATCH FOUND')

        return priceOnRecord

    def __determine_avg_duration(self):
        total = 0
        for job in self.job_list:
            job: job_assistant.Job = job
            total = total + job.duration

        return total/len(self.job_list)
        
    
    def get_rate(self):
         return round(self.price/(self.average_duration/60),2)
    

    def get_data_point_qty(self):
        return len(self.job_list)


    def get_employees(self):
        # Create an empty employee list
        employees = []

        # Iterate over the job objects and gather employees
        for job in self.job_list:
            job: job_assistant.Job = job
            employee = job.employee
            if employee not in employees:
                employees.append(employee)

        return employees
    

    def __evaluate():
         pass
    

    def __str__(self) -> str:
        if self.job_list:
            return f"{self.price} at a rate of ${self.get_rate()} per hour. This takes {self.get_employees()} approximately {round(self.average_duration, 0)} mins"

        else:
            return "INSUFFICIENT DATA"


class Evaluator:
    def __init__(self, all_jobs: job_assistant.Job) -> None:
        """Evaluates a list of Job objects

            Args:
                all_jobs (list): List of type Job
        """
        self.services_performed         = self.__group_jobs_by_service(all_jobs)
        self.services_performed_filtered = copy.deepcopy(self.services_performed)
        self.__filters = []

        self.evaluations = {}


    def get_evaluations(self):
        """
            Applies the filers. Then executes each evaluation per unique job. Finally, returns the list of evaluations.
        """

        # Apply filters to each unique job specification
        for job_key in self.services_performed_filtered:
            self.services_performed_filtered[job_key] = self.__execute_filters(self.services_performed_filtered[job_key])

            if self.services_performed_filtered[job_key]:
                self.evaluations[job_key] = Evaluation(self.services_performed_filtered[job_key])
            else:
                self.evaluations[job_key] = None

        return self.evaluations


    def apply_filter(self, func):
         self.__filters.append(func)


    def __execute_filters(self, job_list):
        for filter in self.__filters:
            job_list = filter(job_list)

        return job_list


    def __group_jobs_by_service(self, job_list):
        """
        Groups the job objects in job_list according to the services they provide.

        Args:
            job_list (list): A list of Job objects.

        Returns:
            dict: A dictionary with service names as keys and lists of Job objects as values.
        """
        # Create an empty dictionary to store the job objects
        jobs_by_service = {}

        # Iterate over the job objects and group them by service
        for job in job_list:
            job: job_assistant.Job = job
            service = job.services
            if service in jobs_by_service:
                jobs_by_service[service].append(job)
            else:
                jobs_by_service[service] = [job]

        return jobs_by_service