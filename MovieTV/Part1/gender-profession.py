import pandas as pd
import csv, numpy, re
from sets import Set
import gender_guesser.detector as g
d = g.Detector()

# create duplicate file of ratings
nameFile = '/Users/nicholasmark/Downloads/name.basics.tsv'
outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/Part1/gender-professionOUTPUT.csv'

primaryProfessionArray = Set(['producer','manager','production_manager','casting_director','writer','talent_agent','editor','executive','editorial_department','director','cinematographer','script_department','assistant_director','casting_department'])

all = []
all.append(['primaryName', 'gender', 'primaryProfession'])
# open names file
with open(nameFile) as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	for row in reader:
		for i in row['primaryProfession'].split(','): #check if person is a key profession
			#unambiguous gender cases:
			found = False
			if i == 'actor':
				name = row['primaryName']
				gender = 'male' 
				all.append([name, gender, row['primaryProfession']])
				found = True
				break
			elif i == 'actress':
				name = row['primaryName']
				gender = 'female'
				all.append([name, gender, row['primaryProfession']])
				found = True
				break

		# not an actor or actress:
		if not found:
			for i in row['primaryProfession'].split(','):
				if i in primaryProfessionArray:
					name = row['primaryName']
					gender = d.get_gender(name.split()[0])
					all.append([name, gender, row['primaryProfession']])
					break #quit out of primaryProfessionArray
			

	all[1:] = sorted(all[1:], key=lambda name: re.sub('[^a-zA-Z]+', '', name[0].split()[-1].upper()) )
	with open(outputFile, 'w') as csvoutput:
		writer = csv.writer(csvoutput)
		writer.writerows(all)