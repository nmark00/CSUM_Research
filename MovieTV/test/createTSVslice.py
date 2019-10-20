import csv

index = 1049338
numElements = 100

outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/miniMovieTV.tsv'
# inputFile = '/Users/nicholasmark/Downloads/title.ratings.tsv'
inputFile = '/Users/nicholasmark/Downloads/episodes.tsv'
count = 0
with open(inputFile) as csvfile:
	reader = csv.reader(csvfile, delimiter='\t')
	with open(outputFile, 'w') as csvoutput:
		writer = csv.writer(csvoutput, delimiter='\t')
		for row in reader:
			if count > index and count < index+numElements:
				writer.writerows([row])
			count += 1
			if count > index+numElements:
				break
