import pandas as pd
import numpy as np
import csv, xlrd, sys, re
from collections import defaultdict, Counter #import dict of sets

# read iduals file
workbook = xlrd.open_workbook("/Users/nicholasmark/Downloads/IPORoster_9711.xlsx","rb")
sheets = workbook.sheet_names() #store file data in sheets

firmNames = set() #create a dict of lastNames to dict of firstNames to middle names  
for sheet_name in sheets: #loop through sheets
    sh = workbook.sheet_by_name(sheet_name)
    for rownum in range(sh.nrows): #go down name column and add names to set
        row_val = sh.row_values(rownum)
        # add entries to dictionary
        firmName = row_val[1].upper()
        firmName = firmName.rsplit(' ', 1)[0] #cuts off suffix
        firmName = firmName.replace('TECH', 'TECHNOLOGY')
		firmName = firmName.replace('INTL', 'INTERNATIONAL')
        firmNames.add(re.sub('[^a-zA-Z0-9]+', '', firmName)) #keeps only letters

#create different fields found in assignee file
fields = ['uuid', 'patent_id', 'assignee_id', 'rawlocation_id', 'type', 'name_first', 'name_last', 'FirmName', 'sequence']

#read the assignee file
df = pd.read_csv('/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/raw_assignee.csv', skipinitialspace=True, usecols=fields, low_memory=False, encoding='utf-8')

#create output file
row = ['FirmName', 'uuid', 'patent_id', 'assignee_id', 'rawlocation_id', 'type', 'name_first', 'name_last', 'sequence']
outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/outputFirm1.csv'
with open(outputFile, 'w') as csvFile:
	writer = csv.writer(csvFile)
	writer.writerow(row)
csvFile.close()

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

#loop through assignees' names
for j in range(len(df.FirmName)): #check if names exist in set
	if type(df.FirmName[j]) is float: #if no name -- false 
		continue
	if isaMatch(df.FirmName[j]): #check if names match
		row = [re.sub(r'[^\x00-\x7F]+',' ', df.FirmName[j]), df.uuid[j], df.patent_id[j], df.assignee_id[j], df.rawlocation_id[j], df.type[j], df.name_first[j], df.name_last[j], df.sequence[j]]
		#open output file, enter a new row with matched patent info
		with open(outputFile, 'a') as csvFile:
			writer = csv.writer(csvFile)
			writer.writerow(row)
		csvFile.close()

# sort the csv file
df = pd.read_csv(outputFile)
sortedCSV = df.iloc[df.FirmName.str.upper().str.replace(' ', '').argsort()]
sortedCSV.to_csv(outputFile, index=False)

# number of occurances column:
column = []
with open(outputFile, 'r') as f:
	c = Counter(stripSuffix(row[0]) for row in csv.reader(f))
# create column #ofPatents
with open(outputFile, 'r') as f:
	file = csv.reader(f)
	next(file) # skip the header line
	for row in file:
		column.append(c[stripSuffix(row[0])])

# add new column to the csv output file
df = pd.read_csv(outputFile)
new_column = pd.DataFrame({'#ofPatents': column})
df = df.merge(new_column, left_index = True, right_index = True)
df.to_csv(outputFile)