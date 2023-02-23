## Service Object
class Customer:
    def __init__(self, customer_id):
        self.customer_id          = customer_id
        self.customer_name        = _database.getCustomerName(customer_id)
        self.customer_address     = _database.getCustomerAddress(customer_id)
        self.jobs                 = []   # List of Service object
        self.jobHistory           = defaultdict(list)   # List of considered jobs, according to __justinsStandard()

        ## How the service gets defined
        self.__justinsStandard()
        self.evaluations          = None


    def __str__(self):
        printString = ""

        i = 1
        print("{} - {}:".format(self.customer_id, self.customer_name))

        if len(self.jobs) > 0:
            for service in self.jobs:
                service: TheJob = service

                printString = printString + "\t{}. {} completed {} on {} for ${} and took {}mins.\n".format(
                    i,
                    service.employee,
                    service.title,
                    service.date,
                    service.price,
                    service.duration
                )
                i = i+1

            return printString

        else:
            return "\tNo valuable data :("


    # What service do we do for the customer?
    # How long does it take us to do it?
    # How much are we charging them for it?
    def evaluate(self):
        evaluations = defaultdict(list)

        for job in self.jobs:
            job: TheJob = job # Type casting

            key = str(job.title)
            price = job.price
            duration = job.duration
            frequency = job.frequency

            # Begin grouping by similar jobs
            eval: Evaluation = evaluations[key]
            if not eval: # Initiate if incountering a new service requirement
                eval = Evaluation(job.title, price, frequency)
                eval.addDuration(duration)
                eval.addEmployee(job.employee)
                evaluations[key] = eval
                continue

            else: # Combine to existing service
                priceOnRecord = eval.price

                if price == priceOnRecord:
                    eval.addDuration(duration)
                    eval.addEmployee(job.employee)

                elif price > priceOnRecord:
                    print('[PRICE MISMATCH] {} {} : {} we charge ${} now, we used to charge ${}. Price changed since {}\n'.format(
                        self.customer_name, 
                        self.customer_address,
                        key,
                        eval.price, 
                        price, 
                        job.date))

        vals = evaluations.values()
        self.evaluations = vals if vals else []

        return self.evaluations
