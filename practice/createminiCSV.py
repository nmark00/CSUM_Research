import numpy as np
import pandas as pd
import csv
import random

outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/practice/miniCSV.csv'

column1 = []
column2 = []
column3 = []
for i in range(10):
	column1.append(i)
	column2.append(random.randint(1,100))
	column3.append(14)

a = np.asarray([column1, column2, column3])
np.savetxt(outputFile, a, fmt='%d', delimiter=',')