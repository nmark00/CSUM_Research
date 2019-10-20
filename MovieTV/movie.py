import urllib, csv, sys
from collections import defaultdict
from bs4 import BeautifulSoup

reload(sys) # handling special char
sys.setdefaultencoding('utf8')

class Movie():
	"""contains: title, tconst, years, award for each year, genre"""
	def __init__(self, tconst):
		self.tconst = tconst
		self.name = str
		self.dates = str
		self.genre = str
		self.winner = []
		self.nominee = []
		self.pAwards = defaultdict(list)
	def __eq__(self, other): #used to compare movies
		if isinstance(other, Movie):
			return (self.tconst == other.tconst)

categories = {'Outstanding Comedy Series','Outstanding Drama Series',
'Outstanding Limited Series','Outstanding Competition Program',
'Outstanding Television Movie','Outstanding Variety Sketch Series',
'Outstanding Variety Talk Series'}

def movieAwards(tconst):
	page = urllib.urlopen('https://www.imdb.com/title/'+tconst+'/awards')
	soup = BeautifulSoup(page.read(), features="lxml")
	
	m1 = Movie(tconst) #create new movie

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
				
				if award in categories: #if the show won an emmy
					if nom: #add the name of award and year to array
						# print 'nom: ' +addThis
						m1.nominee.append(addThis)
					else:
						# print 'won: ' +addThis
						m1.winner.append(addThis)

				else: #the award went to a specific person:
					if nom:
						addThis = 'Nom. '+ addThis
					for a in td.find_all('a'):# some awards have multiple names
						if '/name/' in str(a).split('="')[1]: #make sure it is really a name
							m1.pAwards[str(a).split('/')[2].split('"')[0]].append(addThis)

	return m1	

