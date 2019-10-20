import urllib, csv, sys
from bs4 import BeautifulSoup
import getDates as dt
from collections import defaultdict
import gender_guesser.detector as gender
g = gender.Detector()
from socket import error as SocketError
import errno

reload(sys) # handling special char
sys.setdefaultencoding('utf8')

class Person:
	"""docstring for person"""
	def __init__(self, name, nconst, gender):
		self.name = name
		self.nconst = nconst
		self.prof_dates = {}
		self.year_prof = defaultdict(list)
		self.awards = []
		self.gender = gender
	def __eq__(self, other):
		if isinstance(other, Person):
			return (self.nconst == other.nconst)
	def __hash__(self):
		return hash(self.nconst)

def createPerson(nconst, name, rawDate, profession, pset):
	if nconst not in pset:
		gender = g.get_gender(name.split()[0])
		pset[nconst] = Person(name, nconst, gender) #create new person

	pset[nconst].prof_dates[profession]=rawDate
	for year in dt.getDates(rawDate): #add the professions for each year
		pset[nconst].year_prof[year].append(profession) 
	
	return pset
	

def personArray(tconst):
	#return set of people:
	pset = {}
	try: # error catching, sometimes doesn't load page
		page = urllib.urlopen('https://www.imdb.com/title/'+tconst+'/fullcredits/')
		soup = BeautifulSoup(page.read(), features="lxml")
	except SocketError as e:
		if e.errno != errno.ECONNRESET:
			raise
		print "error with "+tconst
		return False
	

	box = soup.find_all('table', class_='simpleTable simpleCreditsTable')
	roles = soup.find_all('td', class_='credit')
	j = 0

	for k in range(3):
		prof = box[k].find_all('a') #finds everyone in d/w/p box
		for i in range(len(prof)):
			if k == 0:
				profession = 'd'
			elif k == 1:
				profession = 'w'
			else:
				profession = 'p'
			nconst = str(prof[i]).split('/')[2]
			name = str(prof[i].text).strip()
			rawDate = str(roles[j].text).strip()
			pset = createPerson(nconst, name, rawDate, profession, pset)
			j+=1

	return pset







