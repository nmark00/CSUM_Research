import datetime, re
now = datetime.datetime.now()

def getDates(dateString):
	# associate producer (24 episodes, 2016-2019)
	rawDates = dateString.rsplit(',',1)[-1].strip().replace(')','').replace('\xe2\x80\x93','-')
	#rawDates: 2016-2019
	tempStart = re.sub('[^0-9]','',rawDates.split('-')[0])#keep only num
	tempEnd = re.sub('[^0-9]','',rawDates.split('-')[-1])
	if not tempEnd.isdigit(): # if date is (2016-)
		endDate = now.year #set endDate to current year
	else:
		endDate = int(tempEnd) #otherwise set it to last number

	if tempStart.isdigit(): #if the start date exists
		startDate = int(tempStart)
	else: # if there is no start date, make it the end date
		startDate = endDate

	dates = []
	for i in range(endDate-startDate + 1):
		dates.append(startDate+i)
	return dates