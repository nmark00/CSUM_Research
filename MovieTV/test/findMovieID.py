from imdb import IMDb
import re,sys

reload(sys) # handling special char
sys.setdefaultencoding('utf8')

ia = IMDb()
title = raw_input('Enter movie/tv title: ')
print '\n'

for i in str(ia.search_movie(title)).split(','):
	i = i.replace('[http] title:_', ' | Title: ')
	i = i.replace('<Movie id:', 'ID: ')
	print re.sub('[^a-zA-Z0-9: ()|]+', '', i).strip()
	
