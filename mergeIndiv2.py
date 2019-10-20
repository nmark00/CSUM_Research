import csv, sys, re, operator
from collections import defaultdict, Counter

count = 0
csv.field_size_limit(sys.maxsize)

# initialize hashtable
fullNames = defaultdict(lambda: defaultdict(str))

# read Individuals file
with open('/Users/nicholasmark/Downloads/2006IPO_Individuals.csv', 'rb') as indivFile:
	reader = csv.reader(indivFile)
	for row in reader:
		fullName = row[6].split() #split name into components
		middleName = ""
		firstNames = defaultdict(str)
		if len(fullName) > 2: #if middle name exists, add it
			middleName = fullName[2].upper()
		firstNames[fullName[1].upper()] = middleName #link middle name to first name
		fullNames[fullName[0].upper()].update(firstNames) #link last name to first name


def isaMatch(fname, lastName): #names are taken from raw assignee data
	#create name components
	firstMiddle = fname.split() #split up first and middle name
	
	if len(firstMiddle) == 0: #blank name
		return False

	firstName = firstMiddle[0]

	if lastName in fullNames: #last name matches
		if firstName in fullNames[lastName]: #first name matches last name
			if len(firstMiddle) == 1:
				return True #no middle name -- ambiguous
			elif firstMiddle[1] == fullNames[lastName][firstName]: #middle names match
				return True
			elif len(firstMiddle[1]) == 2 and fullNames[lastName][firstName]: #checks if middle name exists
				if firstMiddle[1][1] == "." and firstMiddle[1][0] == fullNames[lastName][firstName][0]: #middle initial matches
					return True
	return False

# make all names uppercase, no spaces, or quotes
def makeValidName(name):
	validName = str(name).upper().strip().strip('"') #all uppercase, no spaces before/after
	return validName

# columns that contain first/last name in rawinventor:
fnCol = 4
lnCol = 5

largeFile = '/Users/nicholasmark/Downloads/rawinventor.csv'
outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/outputIndiv.csv'
with open(largeFile) as inventorFile:
	reader = csv.reader(inventorFile, quotechar=None)
	
	with open(outputFile, 'w') as ouput: #initialize output file
		writer = csv.writer(ouput)
	
	for row in reader:
		if not isinstance(row[fnCol], str) and not isinstance(row[lnCol], str):
			continue

		if isaMatch( makeValidName(row[fnCol]), makeValidName(row[lnCol]) ):
			count += 1
			tempRow = [row[fnCol].strip(), row[lnCol].strip(), row[0],row[1],row[2]]
			with open(outputFile, 'a') as csvFile:
				writer = csv.writer(csvFile)
				writer.writerow(tempRow)
			csvFile.close()
# create array
all = []
fields = ['name_first', 'name_last', 'uuid', 'patent_id', 'inventor_id', '#patents']
all.append(fields)

# sort the array
data = csv.reader(open(outputFile))
sortedlist = sorted(data, key=operator.itemgetter(1, 0))# sort column 1

# count number of occurences
with open(outputFile, 'r') as f: #count without spaces/periods,and middle initial
	c = Counter(re.sub('[^a-zA-Z0-9]+', '', row[0].split()[0] + row[1]) for row in csv.reader(f))
# append occurences to array
for row in sortedlist:
	all.append([row[0],row[1],row[2],row[3],row[4], c[re.sub('[^a-zA-Z0-9]+', '', row[0].split()[0] + row[1])] ])

# replace file with array
with open(outputFile, 'wb') as f:
	fileWriter = csv.writer(f)
	fileWriter.writerows(all)

# print total number of entries
print "count: " + str(count)




