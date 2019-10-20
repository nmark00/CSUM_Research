import csv
import gender_guesser.detector as g
d = g.Detector()

all = []
newColumn1 = []
newColumn2 = []
with open('/Users/nicholasmark/Desktop/AJSummer2019/practice/genderCSV.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		gender = d.get_gender(row[1])
		all.append([row[1], gender])
		# all.append(newColumn2)
	with open('/Users/nicholasmark/Desktop/AJSummer2019/practice/output.csv', 'w') as csvoutput:
		writer = csv.writer(csvoutput)
		writer.writerows(all)