import urllib, csv, sys
from bs4 import BeautifulSoup

reload(sys) # handling special char
sys.setdefaultencoding('utf8')

outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/emmysListOUTPUT.csv'

def getInfo(index):
	page = urllib.urlopen('https://www.imdb.com/search/title/?groups=emmy_nominee&count=250&start='+ index)
	soup = BeautifulSoup(page.read(), features="lxml")
	movie_containers = soup.find_all('div', class_ = 'lister-item mode-advanced')
	
	for i in range(250):
		show = movie_containers[i]
		name = show.h3.a
		dates = name.find_next('span').text
		genre = show.find('span', class_='genre').text
		tconst = str(name).split('/')[2]
		name = name.text
		with open(outputFile, 'a') as csvoutput:
			writer = csv.writer(csvoutput)
			writer.writerows([[tconst, name, dates, genre]])	

with open(outputFile, 'w') as csvoutput:
	writer = csv.writer(csvoutput)
	writer.writerows([['tconst', 'title', 'dates', 'genre']])
for i in range(8):
	index = i*250 + 1
	getInfo(str(index))
