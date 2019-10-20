# goes to each imdb page for the tv shows on emmyList
# gathers information puts each show in its own csv table

from people import Person
import people as ppl
from movie2 import Movie
import movie2 as movie
import getDates as dt
import urllib, csv, sys
from collections import defaultdict
import os, glob

#deletes everything in the output directory
# files = glob.glob('/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/Part3Outputs/*.csv')
# for f in files:
# 	os.remove(f)


emmysList = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/emmysListOUTPUT.csv'
header = ['year','tconst','title','dates','genre','nominations','emmys', 
'nconst','name','director','writer','producer','gender','emmys']

pset = {} #dict of people for each show
# make global variable, so you don't have to keep copying it

def newOutputFile(name):
	name = name.replace('/', '-')
	outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/Part3Outputs/'+str(name)+'.csv'
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



with open(emmysList) as csvfile:
	reader = csv.reader(csvfile)
	next(reader, None)  # skip the headers
	row = list(reader)
	
	#row = [tconst, title, dates, genre]
	for t in range(1284,1500): #each row is a different show
		pset = ppl.personArray(str(row[t][0])) #creates set of people for a show
		mv = movie.movieAwards(row[t]) #instantiate movie:
		
		while mv == False: #error catching, keep requesting url until success
			mv = movie.movieAwards(row[t])
		while pset == False:
			pset = ppl.personArray(str(row[t][0]))


		with open(newOutputFile(row[t][1]), 'a') as csvoutput: # initialize output file
			csvWriter = csv.writer(csvoutput) # add blank columns for role like 'exec'

			for year in mv.arrDates:
				titleRow = [year, mv.tconst, mv.name, mv.dates, mv.genre,mv.noms,mv.wins]
				for nconst in pset:# getting info from the people set
					if year in pset[nconst].year_prof:
						newRow = titleRow + extractPerson(nconst, year)
						newRow.append(getAwards(mv.pAwards[nconst],year))
						csvWriter.writerows([newRow])






