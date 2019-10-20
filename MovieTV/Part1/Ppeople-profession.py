# ** Compatible with pypy **

import csv

# create duplicate file of ratings
nameFile = '/Users/nicholasmark/Downloads/name.basics.tsv'
outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/Part1/people-professionOUTPUT.csv'

primaryProfessionArray = ['director','actor','producer','writer','actress','editor','manager','production_manager','casting_director','talent_agent','executive','editorial_department','cinematographer','script_department','assistant_director','casting_department']

all = []
all.append(['primaryName', 'primaryProfession'])
# open names file
with open(nameFile) as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	for row in reader:

		for i in row['primaryProfession'].split(','): #check if person is a key profession
			for j in primaryProfessionArray:
				if i == j:
					all.append([row['primaryName'], row['primaryProfession']])
					break #quit out of primaryProfessionArray
			else:
				continue
			break
	with open(outputFile, 'w') as csvoutput:
		writer = csv.writer(csvoutput)
		writer.writerows(all)				