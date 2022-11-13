import cj_interpreter as inter
import json
import datetime
from datetime import date 
import cj_evaluator as eval

DATE_FORMAT = '%m/%d/%y'

customers = inter.load()
evals = []

startDate, endDate = datetime.datetime.strptime("01/01/16", DATE_FORMAT).date(), date.today()

evaluation = eval.Evaluator(json.loads(customers[3]))
print('LOOKING AT ', evaluation.customerName)
# evals.append(evaluation)

evals = evaluation.evaluatations
for evalKey in evals:
    duration = evals[evalKey].getAvgDuration(startDate, endDate)
    # print(evalKey, "took an avg of", str(duration), 'mins')
    print(evals[evalKey].getPrice())

# print(evaluation.evaluatations)