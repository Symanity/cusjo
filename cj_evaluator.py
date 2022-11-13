import json
import datetime
from datetime import date 

DATE_FORMAT = '%m/%d/%y'


class Evaluator:
    def __init__(self, customer) -> None:
        self.customerName = customer["name"]
        self.evaluatations = Evaluator.__evals__(customer["jobHistory"])
        

    def __evals__(jobHistory):
        evalDict = {}

        for job in jobHistory:
            jobType = job["type"]

            if not jobType in evalDict:
                evalDict[jobType] = Evaluation(jobType)
            
            evalDict[jobType].jobs.append(job)

        return evalDict


    # Active status if job completed within x amount of days [defaults to 2 years]
    def isActive(customer, effectiveDays = 730):
        jobHistory = customer["jobHistory"]
        dateFormat = '%m/%d/%y'
        today = date.today()

        for job in jobHistory:
            jobDateStr = job["date"]
            jobDate = datetime.datetime.strptime(jobDateStr, dateFormat).date()

            if abs(today-jobDate).days < effectiveDays:
                return True

        return False

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

    def __getJobsInRange(self, startDate, endDate):
        jobList = []
        for job in self.jobs:
            completedDate = datetime.datetime.strptime(job["date"], DATE_FORMAT).date()
            if Evaluation.__considerDate(completedDate, startDate, endDate):
                jobList.append(job)
            
        return jobList


    # Get avg duration of this job type
    def getAvgDuration(self, startDate = datetime.datetime.strptime("01/01/86", DATE_FORMAT).date(), 
                        endDate = date.today()):
        
        effectiveJobs = self.__getJobsInRange(startDate, endDate)

        avgDuration = 0
        jobWithTimes = 0

        for job in effectiveJobs:
            duration = toMinutes(job["duration"])
            if duration:
                jobWithTimes += 1
                avgDuration += duration

        if jobWithTimes > 0:
            return avgDuration/jobWithTimes
        else:
            return None


    # Get frequency of this job type
    def getFrequency():
        pass


    # Get most recent price
    def getPrice(self):
        today = date.today()
        mostRecent = None
        
        for job in self.jobs:
            jobDate = datetime.datetime.strptime(job["date"], DATE_FORMAT).date()

            if not mostRecent:
                mostRecent = jobDate
            
            


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

    return dictToMins(timeDict)


def dictToMins(timeDict):
    mins = 0
    hrs = 0

    if timeDict:
        try:
            if(timeDict["m"]):
                mins = float(timeDict["m"])

            if(timeDict["h"]):
                hrs = float(timeDict["h"])
            
            return mins + (hrs*60)
        except:
            print('[FATAL] Error occured converting to decimal')
            return None

    return None

# OUTPUT:
#  - Name => Avg. Duration, From: xx/xx/xxxx to xx/xx/xxxx
#     ** Frequency    - at least once every 2 years, 
#                     - 1x per year
#                     - 2x per year
#                     - 3x per year
#                     - 4x per year
#                     - xx per year


