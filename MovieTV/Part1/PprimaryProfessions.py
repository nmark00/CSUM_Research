import csv

categories = set()


with open('/Users/nicholasmark/Downloads/name.basics.tsv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	for row in reader:
		for i in row['primaryProfession'].split(','):
			categories.add(i)


print categories