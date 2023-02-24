# JUSTIN'S STANDARD
# =======================================
# This script filters the jobs according to Justin's criteria.
#   1. Max job history 12
#   2. Only include employees (Justin, Devony, Jose, Brandon, Roberto)
#   
#   Data Quality Filters
#   1. Price is identified
#   2. Duration is identified



from src.window_magic.objects.job import Job

def filter_jobs(jobs, list_conditions, individual_conditions):
    """
    Applies filter conditions on the jobs(Job object list)
    """
    filtered_jobs = []

    for job in jobs:
        job:Job = job
        # Apply individual conditions to each job
        if all(condition(job) for condition in individual_conditions):
            # Apply list conditions to entire list
            if all(condition(jobs) for condition in list_conditions):
                filtered_jobs.append(job)

    return filtered_jobs
    