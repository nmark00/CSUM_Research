import urllib, csv, sys
from bs4 import BeautifulSoup

reload(sys) # handling special char
sys.setdefaultencoding('utf8')

def getRoles(tconst):
	#return these arrays:
	darr = []
	warr = []
	parr = []

	page = urllib.urlopen('https://www.imdb.com/title/'+tconst+'/fullcredits/')
	soup = BeautifulSoup(page.read(), features="lxml")

	box = soup.find_all('table', class_='simpleTable simpleCreditsTable')
	roles = soup.find_all('td', class_='credit')
	j = 0


	directors = box[0].find_all('a')
	for i in range(len(directors)):
		temp = []
		temp.append( str(directors[i].text) )
		temp.append(str(directors[i]).split('/')[2])
		temp.append(str(roles[j].text))
		darr.append(temp)
		j+=1

	writers = box[1].find_all('a')
	for i in range(len(writers)):
		temp = []
		temp.append(str(writers[i].text))
		temp.append(str(writers[i]).split('/')[2])
		temp.append(str(roles[j].text))
		warr.append(temp)
		j+=1

	producers = box[2].find_all('a')
	for i in range(len(producers)):
		temp = []
		temp.append(str(producers[i].text))
		temp.append(str(producers[i]).split('/')[2])
		temp.append(str(roles[j].text))
		parr.append(temp)
		j+=1

	return [darr, warr, parr]


emmysList = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/emmysListOUTPUT.csv'
outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/Part2/show-peopleOUTPUT.csv'

header = ['title', 'directors', '', 'writers', '', 'producers', '']
with open(outputFile, 'w') as csvoutput: # initialize output file
	writer = csv.writer(csvoutput) # add blank columns for role like 'exec'
	writer.writerows([header])

# order of the professions in array
d = 0
w = 1
p = 2

with open(emmysList) as csvfile:
	reader = csv.reader(csvfile)
	with open(outputFile, 'a') as csvoutput: # write to output
		writer = csv.writer(csvoutput)
		next(reader, None)  # skip the headers
		t = 0
		for row in reader:
			arr = getRoles(str(row[0]))

			for i in range(max( len(arr[d]),len(arr[w]),len(arr[p]) )):
				if i == 0:
					title = row[1]
				else:
					title = ''
				if i < len(arr[d]):
					direc = arr[d][i][0]
					drole = arr[d][i][2]
				else:
					direc = ''
					drole = ''
				if i < len(arr[w]):
					writ = arr[w][i][0]
					wrole = arr[w][i][2]
				else:
					writ = ''
					wrole = ''
				if i < len(arr[p]):
					prod = arr[p][i][0]
					prole = arr[p][i][2]
				else:
					prod = ''
					prole = ''

				writer.writerows([[title, direc, drole, writ, wrole, prod, prole ]])

			if t > 10:
				break
			t+=1









