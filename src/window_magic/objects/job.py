def translate_from_db(job_row):
    """
        Translates the row returned from the job table into a Job object
    """
    job = Job()

    customer_id, customer_name, customer_address, services, job_date, price, duration, employee = job_row

    job.services = services
    job.date = job_date
    job.price = price
    job.duration = duration
    job.employee = employee

    return job

def translate_rows_from_db(rows):
    job_row = []
    for row in rows:
        job_row.append(translate_from_db(row))

    return job_row

class Job:

    def __init__(self) -> None:
        self.services = None
        self.date = None
        self.price = None
        self.duration = None
        self.employee = None

    def __str__(self) -> str:
        return f"{self.services} - {self.date} - {self.price} - {self.duration} - {self.employee}"