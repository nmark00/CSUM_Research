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
doutputFile = path +'/Part4/directors.csv'
woutputFile = path +'/Part4/writers.csv'
poutputFile = path +'/Part4/producers.csv'

# header = ['year','tconst','title','dates','genre','nominations','emmys', 
# 'nconst','name','director','writer','producer','gender','emmys']

# os.remove(outputFile) # deletes current outputFile

pset = {} #dict of people for each show
# make global variable, so you don't have to keep copying it

def extractPerson(nconst):
	name = pset[nconst].name
	gender = pset[nconst].gender
	director = '' #person is no prof_dates by default
	writer = ''
	producer = ''
	# check which professions that person is
	for year in pset[nconst].year_prof:
		for i in year:
			if i == 'd':
				director = pset[nconst].prof_dates[i]
			if i == 'w':
				writer = pset[nconst].prof_dates[i]
			if i =='p':
				producer = pset[nconst].prof_dates[i]
	
	return [nconst, name, director, writer, producer,gender]


with open(emmysList) as csvfile:
	reader = csv.reader(csvfile)
	with open(doutputFile, 'a') as csvoutput: # initialize output file
		dcsvWriter = csv.writer(csvoutput) 
		dcsvWriter.writerows([['tconst', 'directors', 'years']])

		with open(woutputFile, 'a') as csvoutput:
			wcsvWriter = csv.writer(csvoutput)
			wcsvWriter.writerows([['tconst','writers', 'years']])

			with open(poutputFile, 'a') as csvoutput:
				pcsvWriter = csv.writer(csvoutput)
				pcsvWriter.writerows([['tconst','producers', 'years']])

				# next(reader, None)  # skip the headers
				row = list(reader)
				
				t = 0;
				for i in range(1, 1000):
					pset = ppl.personArray(str(row[i][0])) #creates set of people for a show
					while pset == False:
						print 'uh oh --'+ str(row[i][1])
						pset = ppl.personArray(str(row[i][0])) 


					newRow = [row[i][0] ]
					dprevRow = []
					wprevRow = []
					pprevRow = []
					for nconst in pset:# getting info from the people set
						for p in pset[nconst].prof_dates:
							if p == 'd':
								drow = newRow + [nconst, pset[nconst].prof_dates[p]]
								if dprevRow != drow:
									dcsvWriter.writerows([drow])
								dprevRow = drow
							if p == 'w':
								wrow = newRow + [nconst, pset[nconst].prof_dates[p]]
								if wprevRow != wrow:
									wcsvWriter.writerows([wrow])
								wprevRow = wrow
							if p =='p':
								prow = newRow + [nconst, pset[nconst].prof_dates[p]]
								if pprevRow != prow:
									pcsvWriter.writerows([prow])
								pprevRow = prow

					# t+=1
					# if t == 10:
					# 	break





