import pandas as pd
import numpy as np
import csv, xlrd, sys, re
from collections import defaultdict, Counter #import dict of sets

count = 0
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
# fields = ['uuid', 'patent_id', 'assignee_id', 'rawlocation_id', 'type', 'name_first', 'name_last', 'organization', 'sequence']
fields = ['uuid', 'patent_id', 'assignee_id', 'rawlocation_id', 'type', 'name_first', 'name_last', 'organization', 'sequence']

#read the assignee file
# df = pd.read_csv('/Users/nicholasmark/Desktop/AJSummer2019/IPO_Patent_Data/raw_assignee.csv', skipinitialspace=True, usecols=fields, low_memory=False, encoding='utf-8')
df = pd.read_csv('/Users/nicholasmark/Downloads/rawassignee.tsv', sep='\t',skipinitialspace=True, usecols=fields, low_memory=False, encoding='utf-8')


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
for j in range(len(df.organization)): #check if names exist in set
	if type(df.organization[j]) is float: #if no name -- false 
		continue
	if isaMatch(df.organization[j]): #check if names match
		count += 1
		

print "count: "+str(count)