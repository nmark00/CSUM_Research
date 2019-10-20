from people import Person
import people as ppl
from movie2 import Movie
import movie2 as movie
import getDates as dt
import urllib, csv, sys
from collections import defaultdict
import os, glob

emmysList = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/emmysListOUTPUT.csv'
outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/OUTPUT.csv'
header = ['year','tconst','title','dates','genre','nominations','emmys', 
'nconst','name','director','writer','producer','gender','emmys']

os.remove(outputFile) # deletes current outputFile

pset = {} #dict of people for each show
# make global variable, so you don't have to keep copying it

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
	with open(outputFile, 'a') as csvoutput: # initialize output file
		csvWriter = csv.writer(csvoutput) # add blank columns for role like 'exec'
		csvWriter.writerows([header])
		next(reader, None)  # skip the headers
		
		t = 0 # timer, don't run entire emmysList
		#row = [tconst, title, dates, genre]
		for row in reader: #each row is a different show
			pset = ppl.personArray(str(row[0])) #creates set of people for a show
			mv = movie.movieAwards(row) #instantiate movie:
			for year in mv.arrDates:
				titleRow = [year, mv.tconst, mv.name, mv.dates, mv.genre,mv.noms,mv.wins]
				for nconst in pset:# getting info from the people set
					if year in pset[nconst].year_prof:
						newRow = titleRow + extractPerson(nconst, year)
						newRow.append(getAwards(mv.pAwards[nconst],year))
						csvWriter.writerows([newRow])
			t+=1
			if t == 100:
				break





