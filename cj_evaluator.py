import cj_interpreter as inter
import json
import datetime
from datetime import date 

def evaluate(customerData):
    customer = json.loads(customerData)
    if isActive(customer):
        print(customer["name"], ' => active')
    else:
        print(customer["name"], ' => inactive')

    # --> CONSIDER JOB TYPE <---  For now, base on jobs done within two years

        # DURATION 

        # FREQUENCY 

        # CURRENT PRICE 
    

# DETERMINE IF ACTIVE - Determined based on 2+ years of nothing done
def isActive(customer, effectiveDays = 730):
    jobHistory = customer["jobHistory"]
    dateFormat = '%m/%d/%y'
    today = date.today()
    print(today)

    for job in jobHistory:
        jobDateStr = job["date"]
        jobDate = datetime.datetime.strptime(jobDateStr, dateFormat).date()

        if abs(today-jobDate).days < effectiveDays:
            return True

    return False

customers = inter.load()

evaluate(customers[8])


# OUTPUT:
#  - KeyID => Avg. Duration, From: xx/xx/xxxx to xx/xx/xxxx
#     ** Frequency    - at least once every 2 years, 
#                     - 1x per year
#                     - 2x per year
#                     - 3x per year
#                     - 4x per year
#                     - xx per year


