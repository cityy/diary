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

import importlib.util

# custom script to generate stats
spec = importlib.util.spec_from_file_location("generateSTATS", "./gen_HTML_stats.py")
gen_STATS = importlib.util.module_from_spec(spec)

imageFormats = ['jpg', 'gif']
bookList = []
tagList = []
authorList = []


# add print backup support (generate pdfs ? make it a book?)

file = open('./output/index.html', 'wb')

doc, tag, text = Doc().tagtext()

doc.asis('<!DOCTYPE html>')
with tag('html', lang='en'):
	with tag('head'):
		doc.stag('meta', charset='utf-8')
		doc.stag('meta', name='CATALOGUE OF CITATIONS', content='')
		doc.stag('meta', author='Ferdinand List', content='')
		with tag('title'):
			text('CATALOGUE OF CITATIONS')
		doc.stag('meta', name='viewport', content='width=device-width, initial-scale=1')
		doc.stag('link', rel='stylesheet', href='../assets/lib/bootstrap-4.0.0/bootstrap-grid.min.css')
		doc.stag('link', rel='stylesheet', href='../assets/css/style.css')
		doc.line('script', '', type='text/javascript', src='../assets/js/interaction.js')

		with tag('body'):
			with tag('div', klass='container-fluid'):
				with tag('div', klass='row'):
					with tag('div', id='dictFilter', klass='col-3'):
						doc.line('span', 'Literature', style='margin-top:0;')
						with tag('form'):
							if(os.path.isfile('./data-lists/bookList.txt')):
								with open('./data-lists/bookList.txt', 'rt') as bookList_file:
									for book in bookList_file:
										with tag('div', klass='tagWrapper'):
											doc.line('span', book, klass='filterTag', type='book', value=book.lower().replace('\n', ''))
									bookList_file.close()
						doc.line('span', 'Authors')
						with tag('form'):
							if(os.path.isfile('./data-lists/authorList.txt')):
								with open('./data-lists/authorList.txt', 'rt') as authorList_file:
									for author in authorList_file:
										authorPrint = author.split(',')[0]
										with tag('div', klass='tagWrapper'):
											doc.line('span', authorPrint, klass='filterTag', type='author', value=authorPrint.lower())
									authorList_file.close()
						doc.line('span', 'Tags')
						with tag('form'):
							if(os.path.isfile('./data-lists/tagList.txt')):
								with open('./data-lists/tagList.txt', 'rt') as tagList_file:
									for tagItem in tagList_file:
										#doc.line('input', tagItem, type='checkbox', value=tagItem.replace(' ', '-'))
										with tag('div', klass='tagWrapper'):
											doc.line('span', tagItem.split(' ')[-0], klass='filterTag', type='tag', value=tagItem.lower().replace('\n', '').split(' ')[0])
											doc.line('span', tagItem.split(' ')[-1], klass='countTag', type='tag')
										#doc.asis('<br />')
									tagList_file.close()
						doc.line('span', 'Views')
						with tag('div', klass='tagWrapper'):
							doc.line('span', 'List', klass='viewTag', id='listViewToggle')
							doc.line('span', 'Field', klass='viewTag active', id='fieldViewToggle')
					for letter in os.listdir("./data/"):
						with tag('div', klass='dictLetter col'):
							text(letter)
						for word in os.listdir("./data/" + letter):
							#print(bytes(word, 'utf-8'))
							wordCount = 0
							for citation in os.listdir("./data/" + letter + "/" + word):
								if( str("./data/" + letter + "/" + word + '/' + citation).endswith('.csv') ):
									wordCount += 1
									with open("./data/" + letter + "/" + word + '/' + citation, "rt") as citation_csv:
										thisCitation = dict()
										thisCitationBook = ''
										thisCitationAuthor = ''
										thisCitationTags = ''
										print( citation )
										for key,value in csv.reader(citation_csv, delimiter='|'):
											thisCitation[key] = value
											if(key == 'author'):
												thisCitationAuthor += value.split(',')[0].lower()
											elif(key == 'in'):
												thisCitationBook += value.split(',')[0].lower()
											elif(key == 'tag'):
												tagString = ''.join(value.split('+'));
												tagString = tagString.replace(' ','').lower()
												thisCitationTags += tagString
										with tag('div', klass='dictWord col-3', book=thisCitationBook, author=thisCitationAuthor, tag=thisCitationTags):
											with tag('span'):
												#word = bytes(word, 'utf-8')
												text(word)
											doc.line('sup', wordCount, style='font-size:0.5em; margin-left:-0.5em;')
											with tag('div', klass='container-fluid'):
												with tag('div', klass='row'):
													with tag('div', klass='dictCitation col'):
														#print(type(thisCitation['quote'].encode()))
														if('image' in thisCitation):
															if (len(thisCitation["image"]) > 0):
																doc.stag('img', src=thisCitation["image"])
														if('text' in thisCitation):
															if (len(thisCitation["text"]) > 0):
																with tag('a', href=thisCitation["text"]):
																	text(thisCitation["text"].split('.')[-1].upper())
														# this is old image behaviour
														if("quote" in thisCitation):
															if (thisCitation['quote'] == 'img'):
																for imgFormat in imageFormats:
																	if( os.path.isfile( "./data/" + letter + "/" + word + '/' + citation.replace('csv', imgFormat) )):
																		doc.stag('img', src="../data/" + letter + "/" + word + '/' + citation.replace('csv', imgFormat))
															else:
																text( thisCitation['quote'] )
														with tag('span',klass='credits'):
															if( len(thisCitation["author"]) ):
																text(thisCitation["author"])
																authorList.append(thisCitation['author'].lower())
															if( len(thisCitation["title"]) > 0 ):
																text(':')
																doc.asis('<br />')
																text(thisCitation["title"])
															if( len(thisCitation["in"]) > 0 ):
																doc.asis('<br />')
																text(thisCitation['in'])
																bookList.append(thisCitation['in'].lower())
															if( len(thisCitation["year"]) > 0 ):
																doc.asis('<br />')
																text(thisCitation["year"])
															if( len(thisCitation["pages"]) > 0 ):
																doc.asis('<br />')
																if(thisCitation["pages"].startswith('http')):
																	doc.line('a', '[link]', href=thisCitation["pages"], target='_blank')
																else:
																	text('p. ' + thisCitation["pages"])
															if( len(thisCitation['tag']) > 0):
																doc.asis('<br /><br />')
																tags = thisCitation['tag'].split('+')
																for tagItem in tags:
																	tagList.append(tagItem.lower().replace(' ', ''))
																	with tag('span', klass='tag'):
																		tagItem = tagItem.replace(' ', '')
																		#tagItem = str.encode(tagItem, 'utf-8')
																		#print(type(tagItem))
																		#print(tagItem)
																		text('#' + tagItem)

												citation_csv.close()

bookList = sorted(list(set(bookList)))
authorList = sorted(list(set(authorList)))
tagListDuplicates = tagList
tagList = sorted(list(set(tagList)))

# create counts for each tag
for i,tagSingle in enumerate(tagList):
	count = 0;
	for tagDupl in tagListDuplicates:
		if tagDupl == tagSingle:
			count += 1
	tagList[i] = tagSingle + ' ' + str(count)


bookList_file = open('./data-lists/bookList.txt', 'wt');
for book in bookList:
	bookList_file.write(book + '\n')

authorList_file = open('./data-lists/authorList.txt', 'wt');
for author in authorList:
	authorList_file.write(author + '\n')

tagList_file = open('./data-lists/tagList.txt', 'wt');
for tagItem in tagList:
	tagList_file.write(tagItem + '\n')

#print(doc.getvalue())
#print(type( indent(doc.getvalue(), newline = '\r\n').encode() ) )
file.write(indent(doc.getvalue(), newline = '\r\n').encode() )
#file.write(doc.getvalue())
file.close()

spec.loader.exec_module(gen_STATS)