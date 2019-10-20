import csv

all = []
newColumn1 = []
newColumn2 = []
with open('/Users/nicholasmark/Desktop/AJSummer2019/practice/miniCSV.csv') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		# newColumn1.append('aa')
		# newColumn2.append(row[0])
		all.append(['aa', row[0]])
		# all.append(newColumn2)
	with open('/Users/nicholasmark/Desktop/AJSummer2019/practice/output.csv', 'w') as csvoutput:
		writer = csv.writer(csvoutput)
		writer.writerows(all)