import csv, sys, re, operator
from collections import defaultdict

count = 0
csv.field_size_limit(sys.maxsize)
path = '/Users/nicholasmark/Downloads/'
firmIDs = defaultdict(lambda: defaultdict(list)) #create a set of firms
patentIDs = defaultdict(list)
firmNames = {}
firmDates = {}
capsName = {}

prePatents = defaultdict(list)
postPatents = defaultdict(list)

def stripSuffix(fname):
	fname = fname.upper()
	fname = fname.replace('CORPORATION', '')
	fname = fname.replace('INCORPORATED', '')
	fname = fname.replace('CORP', '')
	fname = fname.replace('INC', '')
	fname = fname.replace('HOLDINGS', '')
	fname = fname.replace('HOLDING', '')
	fname = fname.replace('LTD', '')
	fname = fname.replace('LLC', '')
	fname = fname.replace('AND ASSOCIATES', '')
	fname = fname.replace('ASSOCIATES', '')
	fname = fname.replace('AND ASSOC', '')
	fname = fname.replace('ASSOC', '')
	fname = fname.replace('AND COMPANY', '')
	fname = fname.replace('COMPANY', '')
	fname = fname.replace('AND CO', '')
	fname = fname.replace('& CO', '')
	fname = fname.replace('CO.', '')
	fname = fname.replace('INTL', 'INTERNATIONAL')
	fname = re.sub('[^a-zA-Z0-9]+', '', fname)
	if 'TECHNOLOGY' in fname:
		return fname
	fname = fname.replace('TECH', 'TECHNOLOGY')
	return fname

def isaMatch(fname): #names are taken from raw assignee data
	#create name components
	fname = stripSuffix(fname)

	if fname in firmDates:
		return True
	return False

def getDate(rawDate):
	return int(rawDate.replace('\xe2\x80\x93','-').split('-')[0])

#get IPO dates associated with each firm
with open(path+'IPORoster_9711.csv') as roster:
	reader = csv.reader(roster)
	next(reader, None)  # skip the headers
	for row in reader:
		firmName = row[1].upper()
		firmName = firmName.rsplit(' ', 1)[0] #cuts off suffix
		firmName = firmName.replace('TECH', 'TECHNOLOGY')
		firmName = firmName.replace('INTL', 'INTERNATIONAL')
		firmName = re.sub('[^a-zA-Z0-9]+', '', firmName)
		firmDates[firmName] = row[5]#add the dates
		capsName[firmName] = row[1] #store original names

#creates set of firmNames
with open(path+'raw_assignee.csv', 'rb') as indivFile:
	reader = csv.reader(indivFile)
	for row in reader:
		if not isinstance(row[8], str):
			continue
		if isaMatch( str(row[8]) ):
			count += 1
			assigneeID = re.sub('[^A-Z0-9]+', '', row[3].upper())
			# firmIDs[assigneeID].append(row[2])#links assignee to its patents
			patentIDs[row[2]].append(assigneeID)
			if not assigneeID in firmNames:
				firmNames[assigneeID] = stripSuffix(row[8])

#find the patents
with open(path + 'patent.csv') as patent:
	reader = csv.reader(patent)
	for row in reader:
		patID = re.sub('[^a-zA-Z0-9]+', '', row[0])

		if not patID in patentIDs:
			continue
		patDate = getDate(row[4])


		assigneeIDList = patentIDs[patID]
		for assigneeID in assigneeIDList:
			fname = firmNames[assigneeID]

			if str(patID) == '8370455':
				print fname
				print patDate
				print firmDates[fname]
			
			if int(patDate) >= int(firmDates[fname]):
				postPatents[assigneeID].append(patID)

			else:
				prePatents[assigneeID].append(patID)
				


with open(path+'patentsPrePostIPO.csv', 'a') as output:
	writer = csv.writer(output)
	writer.writerow(['assignee_id','assignee_name','IPO_Date','Pre_IPO_Patents','Post_IPO_Patents'])
	for assigneeID, firmName in firmNames.items():
		tempRow = [assigneeID, capsName[firmName], firmDates[(firmName)],
			len(prePatents[assigneeID]), len(postPatents[assigneeID]) ]
		writer.writerow(tempRow)
