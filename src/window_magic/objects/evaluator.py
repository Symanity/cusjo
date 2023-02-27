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
    

    def apply_filter(self, filter_fun):
         pass
    

    def _evaluate():
         pass


class Evaluator:
    def __init__(self, all_jobs) -> None:
        self.job_history = all_jobs


    def get_evaluations():
        pass


    def apply_filter(self, func):
         pass