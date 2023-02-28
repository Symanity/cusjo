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
    

    def __str__(self) -> str:
        if self.job_list:
            return f"{self.price} at a rate of ${self.get_rate()} per hour. This takes {self.get_employees()} approximately {round(self.average_duration, 0)} mins"

        else:
            return "INSUFFICIENT DATA"


class Evaluator:
    """
    After adding all necessary
    """
    def __init__(self, all_jobs: job_assistant.Job) -> None:
        """
            The Evaluator Object is responsible for filtering and flaging the job list.\n
                1. Apply filters
                2. Apply flags
                3. Get Evaluations

            Args:
                all_jobs (list): List of type Job
        """
        self.services_performed         = self.__group_jobs_by_service(all_jobs)
        self.services_performed_filtered = copy.deepcopy(self.services_performed)
        self.__filters = []
        self.__post_filters = []
        self.__flags = []

        self.evaluations = {}


    def get_evaluations(self, execute_evaluation = False):
        """
            Applies the filers. Then executes each evaluation per unique job. Finally, returns the list of evaluations.

            Returns: A list of job specs and an accompanying Evaluation object
        """

        if execute_evaluation:
            self.__evaluate()

        return self.evaluations


    def __evaluate(self):
        # Apply filters to each unique job specification
        for job_key in self.services_performed_filtered:
            self.services_performed_filtered[job_key] = self.__execute_filters(self.services_performed_filtered[job_key])
            # self.__execute_flags(self.services_performed_filtered[job_key])

            if self.services_performed_filtered[job_key]:
                self.evaluations[job_key] = Evaluation(self.services_performed_filtered[job_key])

                self.evaluations[job_key]= self.__execute_post_filters(self.evaluations[job_key])
            else:
                self.evaluations[job_key] = None


    def apply_pre_filter(self, func):
         """
         Filter the job list to include the returned list
         """
         self.__filters.append(func)


    def apply_post_filter(self, func):
        self.__post_filters.append(func)

    def add_flag(self, func):
        self.__flags.append(func)


    def reset(self):
        self.services_performed_filtered = copy.deepcopy(self.services_performed)
        self.evaluations = {}


    # def __execute_flags(self, job_list):
    #     for filter in self.__filters:
    #         job_list = filter(job_list)

    #     return job_list

    def __execute_filters(self, job_list):
        for filter in self.__filters:
            job_list = filter(job_list)

        return job_list


    def __execute_post_filters(self, evaluation):
        for filter in self.__post_filters:
            evaluation = filter(evaluation)

        return evaluation

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