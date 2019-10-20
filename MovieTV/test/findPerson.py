import csv,re,urllib,sys

csv.field_size_limit(sys.maxsize)

def hasNumbers(inputString):
	return any(char.isdigit() for char in inputString)

def transformString(inputString):
	inputString = re.sub('[^a-zA-Z]+', '', inputString)
	return inputString.upper()


value = raw_input('Enter a person: ')
if hasNumbers(value):
	col = 0
	value = re.sub('\D', '', value)
	value = 'nm'+ value
else:
	col = 1
	value = transformString(value)

tv = '/Users/nicholasmark/Downloads/name.basics.tsv'
seeRest = False
print '\n'

with open(tv) as csvfile:
	reader = csv.reader(csvfile, delimiter='\t')
	for index, row in enumerate(reader):
		if col == 1 :
			name = transformString(row[col])
		else:
			name = row[col]
		if value in name:
			print 'Index: '+ str(index)
			print 'name: '+ row[1]
			print 'nconst: '+ row[0]
			print 'Found in: ' + tv
			print '\n'
			if not seeRest:
				y = raw_input("\nWant to see the rest? y or n\n")
				if y.lower() == 'y':
					seeRest = True
				else:
					quit()
