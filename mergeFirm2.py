import csv, sys, re, operator
from collections import defaultdict, Counter

count = 0
csv.field_size_limit(sys.maxsize)

firmNames = set() #create a set of firms

with open('/Users/nicholasmark/Downloads/IPORoster_9711.csv', 'rb') as indivFile:
	reader = csv.reader(indivFile)
	for row in reader:
		firmName = row[1].upper()
		firmName = firmName.rsplit(' ', 1)[0] #cuts off suffix
		firmName = firmName.replace('TECH', 'TECHNOLOGY')
		firmName = firmName.replace('INTL', 'INTERNATIONAL')
		firmNames.add(re.sub('[^a-zA-Z0-9]+', '', firmName)) #keeps only letters

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
	fname = fname.replace('TECH', 'TECHNOLOGY')
	return re.sub('[^a-zA-Z0-9]+', '', fname)

def isaMatch(fname): #names are taken from raw assignee data
	#create name components
	fname = stripSuffix(fname)

	if fname in firmNames:
		return True
	return False
#['uuid', 'patent_id', 'assignee_id', 'rawlocation_id', 'type', 'name_first', 'name_last', 'organization', 'sequence']
firmCol = 7
largeFile = '/Users/nicholasmark/Downloads/rawassignee.tsv'
# largeFile = '/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/raw_assignee.csv'
outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/outputFirm.csv'

with open(largeFile) as firmFile:
	reader = csv.reader(firmFile, delimiter='\t',quotechar=None)
	# reader = csv.reader(firmFile)

	with open(outputFile, 'w') as ouput: #initialize output file
		writer = csv.writer(ouput)
	
	for row in reader:
		if not isinstance(row[firmCol], str):
			continue
		if isaMatch( str(row[firmCol]) ):
			count += 1
			#['uuid', 'patent_id', 'assignee_id', 'rawlocation_id', 'type', 'name_first', 'name_last', 'organization', 'sequence']
			tempRow = [re.sub(r'[^\x00-\x7F]+',' ', row[firmCol]), row[0], row[1],row[2]]
			with open(outputFile, 'a') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow(tempRow)
			csvFile.close()


#create header
fields = ['organization','uuid', 'patent_id', 'assignee_id','#patents']
all = []
all.append(fields)

# sort the array
data = csv.reader(open(outputFile))
# to add more specific sorting order ...firm: (firm[0].upper(), firm[i])
sortedlist = sorted(data, key=lambda firm: firm[0].upper() )# sort column 1, ignore case

# count number of occurences
with open(outputFile, 'r') as f: #count without spaces/periods,and middle initial
	c = Counter(stripSuffix(row[0]) for row in csv.reader(f))
# append occurences to array
for row in sortedlist:
	all.append([row[0],row[1],row[2],row[3], c[stripSuffix(row[0])] ])

# replace file with array
with open(outputFile, 'wb') as f:
	fileWriter = csv.writer(f)
	fileWriter.writerows(all)

# print total number of entries
print "count: " + str(count)
