import urllib, csv, sys
from collections import defaultdict
from bs4 import BeautifulSoup
import getDates as dt
from socket import error as SocketError
import errno

reload(sys) # handling special char
sys.setdefaultencoding('utf8')

class Movie():
	"""contains: title, tconst, years, award for each year, genre"""
	def __init__(self, tconst, name, dates, genre,arrDates):
		self.tconst = tconst
		self.name = name
		self.dates = dates
		self.genre = genre
		self.arrDates = arrDates
		self.wins = 0
		self.noms = 0
		self.pAwards = defaultdict(list)
	def __eq__(self, other): #used to compare movies
		if isinstance(other, Movie):
			return (self.tconst == other.tconst)

def movieAwards(row):# row = [tconst, title, dates, genre]
	try: # error catching, sometimes doesn't load page
		page = urllib.urlopen('https://www.imdb.com/title/'+row[0]+'/awards')
		soup = BeautifulSoup(page.read(), features="lxml")
	except SocketError as e:
		if e.errno != errno.ECONNRESET:
			raise
		print "error with "+row[1]
		return False

	m1 = Movie(row[0],row[1],row[2],row[3], dt.getDates(row[2]))#create new movie

	for h3 in soup.find_all('h3'): #array of emmy nom/win years
		if 'Primetime Emmy Award' in h3.text:
			# contains all the awards for a given year:
			for td in h3.find_next('table',class_='awards').find_all('td'):
				if 'Winner' in td.text:# if winner/nominee box- skip
					nom = False# winner/nom have the same tag
					continue
				if 'Nominee' in td.text:
					nom = True
					continue
				year = str(h3.a.text).strip()

				#array of nom awards/awards for some year
				award = str(td.text).strip().split('\n')[0]#clear extra char from award name
				addThis = award+' '+year
				if nom:
					m1.noms += 1 #count number of nominations
					addThis = 'Nom. '+ addThis
				else:
					m1.wins += 1 #number of wins

				for a in td.find_all('a'):# some awards have multiple names
					if '/name/nm' in str(a): #make sure it is really a name
						m1.pAwards[str(a).split('/')[2].split('"')[0]].append(addThis)

	return m1	

