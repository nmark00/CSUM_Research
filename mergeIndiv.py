import pandas as pd
import numpy as np
import csv, xlrd
from collections import defaultdict, Counter #import dict of sets

# read Individuals file
workbook = xlrd.open_workbook("/Users/nicholasmark/Downloads/2006IPO_Individuals.xlsx","rb")
sheets = workbook.sheet_names() #store file data in sheets

fullNames = defaultdict(lambda: defaultdict(str)) #create a dict of lastNames to dict of firstNames to middle names  
for sheet_name in sheets: #loop through sheets
    sh = workbook.sheet_by_name(sheet_name)
    for rownum in range(sh.nrows): #go down name column and add names to set
        row_val = sh.row_values(rownum)
        # add entries to dictionary
        fullName = row_val[6].split() #split name into components
        middleName = ""
        firstNames = defaultdict(str)
        if len(fullName) > 2: #if middle name exists, add it
        	middleName = fullName[2].upper()
        firstNames[fullName[1].upper()] = middleName #link middle name to first name
        fullNames[fullName[0].upper()].update(firstNames) #link last name to first name

#create different fields found in assignee file
fields = ['uuid', 'patent_id', 'assignee_id', 'rawlocation_id', 'type', 'name_first', 'name_last', 'FirmName', 'sequence']

#read the assignee file
df = pd.read_csv('/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/raw_assignee.csv', skipinitialspace=True, usecols=fields, low_memory=False, encoding='utf-8')

#create output file
row = ['name_first', 'name_last', 'uuid', 'patent_id', 'assignee_id', 'rawlocation_id', 'type', 'FirmName', 'sequence']
with open('/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/outputIndiv.csv', 'w') as csvFile:
	writer = csv.writer(csvFile)
	writer.writerow(row)
csvFile.close()


def isaMatch(fname, lastName): #names are taken from raw assignee data
	#create name components
	firstMiddle = fname.split() #split up first and middle name
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

#loop through assignees' names
for j in range(len(df.name_first)): #check if names exist in set
	if type(df.name_first[j]) is float or type(df.name_last[j]) is float: #if no name -- false 
		continue
	if isaMatch(df.name_first[j].upper(), df.name_last[j].upper()): #check if names match
		row = [df.name_first[j].strip(), df.name_last[j].strip(), df.uuid[j], df.patent_id[j], df.assignee_id[j], df.rawlocation_id[j], df.type[j], df.FirmName[j], df.sequence[j]]
		#open output file, enter a new row with matched patent info
		with open('/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/outputIndiv.csv', 'a') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(row)
		csvFile.close()

# sort the output file
df = pd.read_csv('/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/outputIndiv.csv')			
sortedCSV = df.sort_values('name_last')[['name_first', 'name_last', 'uuid', 'patent_id', 'assignee_id', 'rawlocation_id', 'type', 'FirmName', 'sequence']]
sortedCSV.to_csv('/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/outputIndiv.csv', index=False)

# get number of occurances into an array
column = []
with open('/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/outputIndiv.csv', 'r') as f:
	c = Counter(row[0].strip() + row[1].strip() for row in csv.reader(f))
# create column #ofPatents
with open('/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/outputIndiv.csv', 'r') as f:
	file = csv.reader(f)
	next(file) # skip the header line
	for row in file:
		column.append(c[row[0].strip() + row[1].strip()])

# add new column to the csv output file
df = pd.read_csv('/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/outputIndiv.csv')
new_column = pd.DataFrame({'#ofPatents': column})
df = df.merge(new_column, left_index = True, right_index = True)
df.to_csv('/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/outputIndiv.csv')