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

	if tempStart.isdigit():
		startDate = int(tempStart)
	else:
		startDate = endDate

	dates = []
	for i in range(endDate-startDate + 1):
		dates.append(startDate+i)
	return dates

set1 = getDates('associate producer (24 episodes, 2016-2019)')
set2 = getDates('(2010- )')
set3 = getDates('(2013-2019)')
set4 = getDates(' -2019')
set5 = getDates('2015 TV movie')

for i in set1:
	print i
print ''
for i in set2:
	print i
print ''
for i in set3:
	print i
print ''
for i in set4:
	print i
print ''
for i in set5:
	print i