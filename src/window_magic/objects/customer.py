from src.window_magic.databasing import assistant as wm
from src.customer_factor_importer import assistant as cf
from src.window_magic.objects.evaluator import Evaluator
from src.window_magic.objects import job as job_assistant

## Service Object
class Customer:
    def __init__(self, customer_id):
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
        


    # What service do we do for the customer?
    # How long does it take us to do it?
    # How much are we charging them for it?
    # def evaluate(self):
    #     evaluations = defaultdict(list)

    #     for job in self.jobs:
    #         job: TheJob = job # Type casting

    #         key = str(job.title)
    #         price = job.price
    #         duration = job.duration
    #         frequency = job.frequency

    #         # Begin grouping by similar jobs
    #         eval: Evaluation = evaluations[key]
    #         if not eval: # Initiate if incountering a new service requirement
    #             eval = Evaluation(job.title, price, frequency)
    #             eval.addDuration(duration)
    #             eval.addEmployee(job.employee)
    #             evaluations[key] = eval
    #             continue

    #         else: # Combine to existing service
    #             priceOnRecord = eval.price

    #             if price == priceOnRecord:
    #                 eval.addDuration(duration)
    #                 eval.addEmployee(job.employee)

    #             elif price > priceOnRecord:
    #                 print('[PRICE MISMATCH] {} {} : {} we charge ${} now, we used to charge ${}. Price changed since {}\n'.format(
    #                     self.customer_name, 
    #                     self.customer_address,
    #                     key,
    #                     eval.price, 
    #                     price, 
    #                     job.date))

    #     vals = evaluations.values()
    #     self.evaluations = vals if vals else []

    #     return self.evaluations
