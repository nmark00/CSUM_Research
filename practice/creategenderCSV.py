import numpy as np
import pandas as pd
import csv
import random

outputFile = '/Users/nicholasmark/Desktop/AJSummer2019/practice/genderCSV.csv'

column1 = ['Natalie', "Ally", "Nicholas", "Amy", "Eric"]


# a = np.asarray([column1])

pd.DataFrame(data={'name':column1}).to_csv(outputFile)