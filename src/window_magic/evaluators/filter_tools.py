from datetime import datetime
from datetime import timedelta
import statistics
from scipy.stats import zscore
from src.window_magic.objects.job import Job


def get_frequency(job_list):
    # get dates for post covid
    dates = __filter_for_post_covid(job_list)
    dates.reverse()

    # calculate differences between adjacent dates
    if len(dates) > 1:
        differences = [dates[i+1] - dates[i] for i in range(len(dates)-1)]
        days = [diff.days for diff in differences]

        z_score = zscore(days)

        i = 0
        for i in range(len(differences)-1):
            if z_score[i] > 1 or z_score[i] < -1:
                differences.remove(differences[i])


        # calculate total number of differences and sum up differences in days
        total_diffs = len(differences)
        total_days = sum(diff.days for diff in differences)

        # calculate average days between dates
        average_days = total_days / total_diffs

        return round(average_days, 1)


def get_zscore(job_list, freedom = 0):
    z_scores = zscore(__get_durations__(job_list),0, -freedom)

    scores = {}
    i = 0
    for job in job_list:
         scores[job] = z_scores[i]
         i = i+1

    return scores

def calc_standard_deviation(job_list, multiplier = 100):
    try:
        return statistics.stdev(__get_durations__(job_list))
    except:
        print('[INFO] Not enough data points to determine deviation')
        return 0


def perform_removal(jobs, max_score = 1, sd_value = 50):

    z_scores = get_zscore(jobs, sd_value)

    for job, score in z_scores.items():
        job: Job = job

        if score >  max_score or score < -max_score:
            jobs.remove(job)

    return jobs


def calc_job_average(job_list):
    durations = __get_durations__(job_list)

    total = 0

    for duration in durations:
        total = total + duration

    return total / len(durations)
    # return __get_mean__(job_list)


def __get_mean__(job_list):
    durations = __get_durations__(job_list)
    center = round(len(durations)/2,None)

    return durations[center]



def __get_durations__(job_list):
    durations = []

    for job in job_list:
        job: Job = job
        durations.append(job.duration)
    
    return durations


def __get_dates__(job_list):
    dates = []

    for job in job_list:
        job: Job = job
        dates.append(job.date)
    
    dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
    return dates


def __filter_for_post_covid(job_list):
    covid_end = "2021-06-01"

    limit_date = datetime.strptime(covid_end, '%Y-%m-%d')
    dates = []

    for job in job_list:
        job: Job = job
        date = datetime.strptime(job.date, '%Y-%m-%d')

        if date >= limit_date:
            dates.append(date)

    return dates