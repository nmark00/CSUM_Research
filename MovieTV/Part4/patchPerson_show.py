import urllib, csv, sys, re
path1 = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV'
sys.path.insert(1, path1)
import glob, os
from people import Person
import people as ppl
from movie2 import Movie
import movie2 as movie
# import main2 as m2
import getDates as dt
from collections import defaultdict

emmysList = path1 + '/emmysListOUTPUT.csv'
path = path1+ '/Part3Outputs/*.csv'
output = path1+ '/Part4/person_showOutputTESTER.csv'


pset = {} #dict of people for each show
# make global variable, so you don't have to keep copying it

def newOutputFile(name):
	name = name.replace('/', '-')
	outputFile = path1 + '/Part4/'+str(name)+'.csv'
	# with open(outputFile, 'w') as csvoutput: # initialize output file
	# 	csvWriter = csv.writer(csvoutput) # add blank columns for role like 'exec'
	# 	csvWriter.writerows([header])
	return outputFile

def extractPerson(nconst, year):
	name = pset[nconst].name
	gender = pset[nconst].gender
	director = '' #person is no prof_dates by default
	writer = ''
	producer = ''
	# check which professions that person is
	for i in pset[nconst].year_prof[year]:
		if i == 'd':
			director = pset[nconst].prof_dates[i]
		if i == 'w':
			writer = pset[nconst].prof_dates[i]
		if i =='p':
			producer = pset[nconst].prof_dates[i]
	
	return [nconst, name, director, writer, producer,gender]

def getAwards(pAwards, year):
	awards = []
	for award in pAwards:
		if award.rsplit(' ',1)[-1] == str(year):
			awards.append(award)
	return awards



matches = set()
with open(output, 'a') as csvoutput:
	writer = csv.writer(csvoutput)
	with open(emmysList) as csvfile:# open emmysList
		reader = csv.reader(csvfile)
		row = list(reader)
		index = -1
		count = 0
		otherCount = 0
		
		for file in glob.glob(path): # get all csv files in the directory
			index += 1
			if os.path.isfile(file) and os.stat(file).st_size > 0:
				continue

			filename = file.rsplit('/')[-1].replace('.csv', '') 
			for i in range(0, len(row)): 
				if re.sub('[^A-Za-z0-9]', '', row[i][1])  == re.sub('[^A-Za-z0-9]', '',filename):
					matches.add(tuple(row[i]))
					print row[i][0]
			count += 1

			# with open(file) as csvfile:
			# 	reader = csv.reader(x.replace('\0', '') for x in csvfile)

			# 	for row in reader:
			# 		writer.writerows([[row[1],row[7]]])





with open(emmysList) as csvfile:
	reader = csv.reader(csvfile)
	row = list(reader)
	
	#row = [tconst, title, dates, genre]
	for row in matches: #each row is a different show
		pset = ppl.personArray(str(row[0])) #creates set of people for a show
		mv = movie.movieAwards(row) #instantiate movie:
		
		while mv == False: #error catching, keep requesting url until success
			mv = movie.movieAwards(row)
		while pset == False:
			pset = ppl.personArray(str(row[0]))


		with open(newOutputFile(row[1]), 'a') as csvoutput: # initialize output file
			csvWriter = csv.writer(csvoutput) # add blank columns for role like 'exec'

			for year in mv.arrDates:
				titleRow = [year, mv.tconst, mv.name, mv.dates, mv.genre,mv.noms,mv.wins]
				for nconst in pset:# getting info from the people set
					if year in pset[nconst].year_prof:
						newRow = titleRow + extractPerson(nconst, year)
						newRow.append(getAwards(mv.pAwards[nconst],year))
						csvWriter.writerows([newRow])






