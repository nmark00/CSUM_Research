import urllib, csv, sys
path = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV'
sys.path.insert(1, path)

from people import Person
import people as ppl
from movie2 import Movie
import movie2 as movie
import getDates as dt
from collections import defaultdict
import os, glob

emmysList = path + '/emmysListOUTPUT.csv'
outputFile = path +'/Part4/AwardsOUTPUT.csv'
awardCountFile = path + '/Part4/AwardsCountOUTPUT.csv'
header = ['tconst', 'year', 'nconst', 'emmy']
# header = ['year','tconst','title','dates','genre','nominations','emmys', 
# 'nconst','name','director','writer','producer','gender','emmys']

# os.remove(outputFile) # deletes current outputFile

# pset = {} #dict of people for each show
# # make global variable, so you don't have to keep copying it

# def extractPerson(nconst, year):
# 	name = pset[nconst].name
# 	gender = pset[nconst].gender
# 	director = '' #person is no prof_dates by default
# 	writer = ''
# 	producer = ''
# 	# check which professions that person is
# 	for i in pset[nconst].year_prof[year]:
# 		if i == 'd':
# 			director = pset[nconst].prof_dates[i]
# 		if i == 'w':
# 			writer = pset[nconst].prof_dates[i]
# 		if i =='p':
# 			producer = pset[nconst].prof_dates[i]
	
# 	return [nconst, name, director, writer, producer,gender]

def getAwards(pAwards, year):
	awards = []
	for award in pAwards:
		if award.rsplit(' ',1)[-1] == str(year):
			awards.append(award)
	return awards



with open(emmysList) as csvfile:
	reader = csv.reader(csvfile)
	with open(outputFile, 'a') as csvoutput: # initialize output file
		csvWriter = csv.writer(csvoutput) 
		# csvWriter.writerows([header])
		next(reader, None)  # skip the headers
		row = list(reader)
		
		# t = 0 # timer, don't run entire emmysList
		#row = [tconst, title, dates, genre]
		# for row in reader: #each row is a different show
		for i in range(1815, 20000):
			# pset = ppl.personArray(str(row[0])) #creates set of people for a show
			mv = movie.movieAwards(row[i]) #instantiate movie:
			while mv == False:
				mv = movie.movieAwards(row[i])
			for year in mv.arrDates:
				newRow = [mv.tconst, year]
				for nconst in mv.pAwards:
				# titleRow = [year, mv.tconst, mv.name, mv.dates, mv.genre,mv.noms,mv.wins]
				# for nconst in pset:# getting info from the people set
				# 	if year in pset[nconst].year_prof:
				# 		newRow = titleRow + extractPerson(nconst, year)
					newRow.append(nconst)
					for award in getAwards(mv.pAwards[nconst],year):
						newRow.append(award)
						csvWriter.writerows([newRow])
						newRow.remove(award)
					newRow.remove(nconst)
			# t+=1
			# if t == 10:
			# 	break





