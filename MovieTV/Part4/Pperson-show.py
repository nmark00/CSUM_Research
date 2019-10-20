import csv
import glob, os

path = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/Part3Outputs/*.csv'
output = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/Part4/person_showOutput.csv'
with open(output, 'a') as csvoutput:
	writer = csv.writer(csvoutput)
	writer.writerows([['tconst','nconst']])
	
	for file in glob.glob(path): # get all csv files in the directory
		if os.path.isfile(file) and os.stat(file).st_size > 0:

			with open(file) as csvfile:
				reader = csv.reader(x.replace('\0', '') for x in csvfile)

				for row in reader:
					writer.writerows([[row[1],row[7]]])
