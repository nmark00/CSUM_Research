import csv,re,urllib,sys

csv.field_size_limit(sys.maxsize)

value = raw_input('Enter a movieID: ')
value = re.sub('\D', '', value)
value = 'tt'+ value

tv = '/Users/nicholasmark/Downloads/episodes.tsv'

seeRest = False

with open(tv) as csvfile:
	reader = csv.reader(csvfile, delimiter='\t')
	for index, row in enumerate(reader):
		for i in row:
			if value == i:
				print 'Index: '+ str(index)
				print 'tconst: '+ row[0]
				print 'Found in: ' + tv
				if not seeRest:
					y = raw_input("\nWant to see the rest? y or n\n")
					if y.lower() == 'y':
						seeRest = True
					else:
						quit()
				break

bit = '/Users/nicholasmark/Downloads/title.'
movieArray = [bit+'akas.tsv',bit+'crew.tsv',bit+'ratings.tsv', bit+'basics.tsv']

for i in movieArray:
	with open(i) as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')
		for index, row in enumerate(reader):
			if value == row[0]:
				print 'Index: '+ str(index)
				print 'Found in: ' + i
				quit()
