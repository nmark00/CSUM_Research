import pandas as pd
import csv, numpy
# import gender_guesser.detector as gender
# d = gender.Detector()

# create duplicate file of ratings
ratingsFile = '/Users/nicholasmark/Downloads/title.ratings.tsv'
outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/MovieTV/Part1/rating-peopleOutput.csv'
df = pd.read_csv(ratingsFile, sep='\t')
numRows = len(df['tconst'])
# add new column
# new_column = [None] * len(df['numVotes'])
# # new_column = df['numVotes'] + 1
# df['names'] = new_column
# df.to_csv(outputFile)

# search algorithms: 
def binarySearch (arr, l, r, x): 
  
    # Check base case 
    if r >= l: 
  
        mid = l + (r - l)/2
  
        # If element is present at the middle itself 
        if arr[mid] == x: 
            return mid 
          
        # If element is smaller than mid, then it can only 
        # be present in left subarray 
        elif arr[mid] > x: 
            return binarySearch(arr, l, mid-1, x) 
  
        # Else the element can only be present in right subarray 
        else: 
            return binarySearch(arr, mid+1, r, x) 
  
    else: 
        # Element is not present in the array 
        return -1



# create empty name column to be appended later
name_Column = [''] * numRows 

# open names file
with open('/Users/nicholasmark/Downloads/name.basics.tsv') as csvfile:
	reader = csv.DictReader(csvfile, delimiter='\t')
	for row in reader:
		for i in row['knownForTitles'].split(','):
			index = binarySearch(df['tconst'].to_numpy(), 0, numRows-1, i)
			if index != -1:
				if name_Column[index] == '':
					name_Column[index] = row['primaryName']
				else:
					name_Column[index] += ', ' + row['primaryName']

df['names'] = name_Column
df.to_csv(outputFile)
