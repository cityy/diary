#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3RD PARTY MODULES
from yattag import Doc
from yattag import indent
import csv
import os
import locale
encoding = locale.getpreferredencoding(True)
#import math+

imageFormats = ['jpg', 'gif']
bookList = []
tagList = []
authorList = []
keywordList = []
datesList = []

file = open('./output/stats.html', 'wb')

doc, tag, text = Doc().tagtext()

#todo
# switch from keywords to authors/books
# think about displaying tags
# show just entry counts on y
# highlight identical elements on hover
# add link to the catalogue
# make horizontal scrolling work
# day/month/year

for letter in os.listdir("./data/"):
	for word in os.listdir("./data/" + letter):
		for citation in os.listdir("./data/" + letter + "/" + word):
			if( str("./data/" + letter + "/" + word + '/' + citation).endswith('.csv') ):
				with open("./data/" + letter + "/" + word + '/' + citation, "rt") as citation_csv:
					keywordList.append(word)
					thisCitation = dict()
					thisCitationBook = ''
					thisCitationAuthor = ''
					thisCitationTags = ''
					thisCitationDate = ''
					thisCitationTime = ''
					for key,value in csv.reader(citation_csv, delimiter='|'):
						thisCitation[key] = value
						#if('dateAdded' not in thisCitation):
							#print(word, citation)
						if(key == 'author'):
							thisCitationAuthor += value.split(',')[0].lower()
						elif(key == 'in'):
							if(value == ''):
								thisCitationBook = '-'
							else:
								thisCitationBook += value.split(',')[0].lower()
							bookList.append(thisCitationBook)
						elif(key == 'tag'):
							tagString = ''.join(value.split('+'));
							tagString = tagString.replace(' ','').lower()
							thisCitationTags += tagString
							tagList.append(thisCitationTags);
						elif(key == 'dateAdded'):
							thisCitationDate = value.split('_')[0].replace('2018', '18')
							thisCitationTime = value.split('_')[1]
							datesList.append(thisCitationDate);

datesListUnique = sorted(list(set(datesList)));

dateKeywords = dict()
for date in datesListUnique:
	dateKeywords[date]=[]

dateBooks = dict()
for date in datesListUnique:
	dateBooks[date]=[]

for index,date in enumerate(datesList):
	dateBooks[date].append(bookList[index])


for index,date in enumerate(datesList):
	dateKeywords[date].append(keywordList[index])


doc.asis('<!DOCTYPE html>')
with tag('html', lang='en'):
	with tag('head'):
		doc.stag('meta', charset='utf-8')
		doc.stag('meta', name='CATALOGUE OF CITATIONS STATS', content='')
		doc.stag('meta', author='Ferdinand List', content='')
		with tag('title'):
			text('CATALOGUE OF CITATIONS STATS')
		doc.stag('meta', name='viewport', content='width=device-width, initial-scale=1')
		doc.stag('link', rel='stylesheet', href='./assets/lib/bootstrap-4.0.0/bootstrap-grid.min.css')
		doc.stag('link', rel='stylesheet', href='./assets/css/stats.css')
		doc.line('script', '', type='text/javascript', src='./assets/js/interaction_stats.js')

	with tag('body'):
		#with tag('div', klass='container-fluid'):
			with tag('div', klass='chart'):
				for date in datesListUnique:
					with tag('div', klass='column'):
						with tag('div', klass='container-fluid'):
							for keyword in dateBooks[date]:
								with tag('div', klass='row'):
									with tag('span', klass='valueSpan'):
										text( keyword )
							with tag('div', klass='row'):
								with tag('span', klass='dateSpan'):
									text(date)
			with tag('div', id='options'):
				text('options')

#print(dateKeywords)

file.write(indent(doc.getvalue(), newline = '\r\n').encode() )
#file.write(doc.getvalue())
file.close()