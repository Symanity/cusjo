from src.window_magic.databasing import assistant as wm
from src.customer_factor_importer import assistant as cf
from src.window_magic.objects.evaluator import Evaluator
from src.window_magic.objects import job as job_assistant

## Service Object
class Customer:
    def __init__(self, customer_id):
        """
            Constructs the Customer object, only requiring the Customer Id. All other information
            is gathered directly from the database.
        """
        self.id             = customer_id
        self.name           = cf.getCustomerName(customer_id)
        self.address        = cf.getCustomerAddress(customer_id)
        self.phone_number   = None
        self.email          = None
        self.customer_since = None
        self.all_jobs       = job_assistant.translate_rows_from_db(wm.get_completed_jobs(customer_id))
        self.evaluator      = Evaluator(self.all_jobs)


    def get_evaluator(self):
        """
        Returns an evaluator object, which will evaluate the Customer
        """
        return self.evaluator

        
    # def __str__(self):
    #     printString = ""

    #     i = 1
    #     print("{} - {}:".format(self.customer_id, self.customer_name))

    #     if len(self.jobs) > 0:
    #         for service in self.jobs:
    #             service: TheJob = service

    #             printString = printString + "\t{}. {} completed {} on {} for ${} and took {}mins.\n".format(
    #                 i,
    #                 service.employee,
    #                 service.title,
    #                 service.date,
    #                 service.price,
    #                 service.duration
    #             )
    #             i = i+1

    #         return printString

    #     else:
    #         return "\tNo valuable data :("
        