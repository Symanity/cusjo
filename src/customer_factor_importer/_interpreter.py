import datetime
from datetime import date
from datetime import datetime as dt
import numpy as np
import copy

DATE_FORMAT = '%Y-%m-%d'

class Evaluator:
    def __init__(self, customer) -> None:
        self.customerID = customer["id"]
        self.customerName = customer["name"]
        self.services = Evaluator.__evals__(customer["jobHistory"])


    # Sorts by jobType
    def __evals__(jobHistory):
        evalDict = {}

        for job in jobHistory:
            jobType = job["type"]

            if not jobType in evalDict:
                evalDict[jobType] = Evaluation(jobType)
            
            evalDict[jobType].jobs.append(job)

        return evalDict


    def __str__(self) -> str:
        return self.customerName


class Evaluation:
    def __init__(self, jobType) -> None:
        self.jobType = jobType
        self.jobs = []


    def __considerDate(targetDate, startDate, endDate):
        if targetDate > startDate and targetDate < endDate:
            return True
        else:
            return False


    # Get frequency of this job type. This takes the average of time between jobs.
    # ** Only considers future jobs... This is dependant on the when the database gets built
    def getFrequency(self):
        count = 1
        total = 0

        if len(self.jobs) >= 3:
            jobs = copy.deepcopy(self.jobs)

            job = jobs.pop()
            while(len(jobs) > 1):
                job2 = jobs.pop()

                if job and job2:
                    delta = self.__getDeltaDays(job2["date"],job["date"])

                    if delta > 0:
                        total = total + delta
                        count = count + 1

                    job = job2 

            average = total/count

            return round(average, 1)
        
        else:
            return None

    def __getDeltaDays(self, date1, date2):
         # Define the start and end dates
        firstDate = dt.strptime(date1, DATE_FORMAT).date()
        secondDate = dt.strptime(date2, DATE_FORMAT).date()

        today = dt.today().date()

        if firstDate > today and secondDate > today:
            difference = secondDate - firstDate
            return difference.days

        else:
            return 0

# Converts into minutes
def toMinutes(timeStr):
    timeDict = {
        "m": None,
        "h": None,
    }

    if timeStr:
        numStr = ''
        for c in timeStr:
            if c >= '0' and c <= '9' or c == '.':
                numStr += c

            # Store numStr as minute
            elif c == 'm' or c == 'M':
                timeDict["m"] = numStr.strip()
                numStr = ''

            elif c == 'h' or c == 'H':
                timeDict["h"] = numStr.strip()
                numStr = ''

    # No time was provided
    else:
        timeDict = None

    timeInMinutes = dictToMins(timeDict, timeStr)

    if timeInMinutes:
        return np.math.ceil(timeInMinutes)
    else:
        return None


def dictToMins(timeDict, ogString):
    mins = 0
    hrs = 0

    if timeDict:
        try:
            if(timeDict["m"]):
                mins = float(timeDict["m"])

            if(timeDict["h"]):
                specialCase = '.'
                if timeDict["h"] == specialCase:
                    timeDict["h"] = 0

                hrs = float(timeDict["h"])

            
            return mins + (hrs*60)
        except:
            print('[ERROR] Error occured converting to decimal. Unrecognized - {}'.format(ogString))
            print(timeDict)
            return None

    return None

def convertTo_iso8601_date(datestring):
    date = dt.strptime(datestring, '%m/%d/%y')  # parse the date string

    # format the date in ISO8601 format
    iso8601_date = date.strftime('%Y-%m-%d')

    return iso8601_date

