import urllib, csv

def findTitle(tconst):
	url = 'http://www.imdb.com/title/' + tconst
	webpage = urllib.urlopen(url).read()
	title = str(webpage).split('<title>')[1].split('</title>')[0]
	title = title.rsplit(' ',3)[0]
	return title

outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/Part1/tconst-movieOUTPUT.csv'
inputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/miniMovieTV.tsv'

with open(inputFile) as csvfile:
	reader = csv.reader(csvfile, delimiter='\t')
	with open(outputFile, 'w') as csvoutput:
		writer = csv.writer(csvoutput)
		writer.writerows([['tconst', 'movieTitle']])
		for row in reader:
			writer.writerows([[row[0], findTitle(row[0])]])
