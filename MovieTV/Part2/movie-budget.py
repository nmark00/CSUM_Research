import urllib, csv, sys
from bs4 import BeautifulSoup

reload(sys) # handling special char
sys.setdefaultencoding('utf8')

def webInfo(tconst):
	page = urllib.urlopen('http://www.imdb.com/title/'+ tconst)
	soup = BeautifulSoup(page.read(), features="lxml")
	title = soup.title.string.rsplit(' ',3)[0] + ')'#get the title without imdb tag
	budget = ''
	for h4 in soup.find_all('h4'): #looks for h4 tag
	    if "Budget:" in h4:
	        budget = h4.next_sibling.strip()
	
	return [title, budget]

# movie and tv have different columns
i = raw_input("Enter 't' for TV, 'm' for movie.\n") 
t = 0 #movie by default
if i.lower() == 't':
	t = 1

outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/Part2/movie-budgetOUTPUT.csv'
inputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/miniMovieTV.tsv'

with open(inputFile) as csvfile:
	reader = csv.reader(csvfile, delimiter='\t') #reads input tsv file
	with open(outputFile, 'w') as csvoutput: #open up output file
		writer = csv.writer(csvoutput)
		writer.writerows([['tconst', 'movieTitle', 'budget']]) #write header of output file
		prev = None #get rid of duplicates
		for row in reader:
			if prev == row[t]:
				continue
			prev = row[t]
			webInfoList = webInfo(row[t])
			
			# if webInfoList[1] == '': #only keep ones with a budget
			# 	continue
			writer.writerows([[row[t], webInfoList[0], webInfoList[1] ]])


