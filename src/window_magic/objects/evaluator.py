from src.window_magic.objects import job as job_assistant

class Evaluation:
    def __init__(self, jobs) -> None:
        # self.serviceTitle = titles
        # self.price = price
        # self._duration = 0
        # self.data_count = 0
        # self.employees = []
        self.jobs = []

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
    

    def get_rate(self):
         pass
    

    def get_data_point_qty(self):
        pass


    def get_involved_emoployee(self):
         pass
    

    def _evaluate():
         pass


class Evaluator:
    def __init__(self, all_jobs: job_assistant.Job) -> None:
        """Evaluates a list of Job objects

            Args:
                all_jobs (list): List of type Job
        """
        self.job_history = all_jobs
        self.filtered_jobs = all_jobs
        self.__filters = []


    def get_evaluations(self):
        """
            Applies the filers. Then executes each evaluation per unique job. Finally, returns the list of evaluations.
        """
        self.__execute_filters()

        for job in self.job_history:
             print(job)


    def apply_filter(self, func):
         self.__filters.append(func)


    def __execute_filters(self):
         for filter in self.__filters:
              self.filtered_jobs = filter(self.filtered_jobs)