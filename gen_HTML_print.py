#!/usr/bin/env python
# -*- coding: utf-8 -*-

# 3RD PARTY MODULES
from yattag import Doc
from yattag import indent
import csv
import os
import locale
from itertools import chain
from collections import deque
encoding = locale.getpreferredencoding(True)
#import math+

imageFormats = ['jpg', 'gif']
bookList = []
tagList = []
authorList = []

def flattenList(list):
	flatList = []
	for sublist in list:
		for item in sublist:
			flatList.append(item)
	return flatList


# enable drag and drop
# don't handle images with the quote key, make an extra file key
# add pdf support
# add print backup support (generate pdfs ? make it a book?)

file = open('../print.html', 'wb')

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
		doc.stag('link', rel='stylesheet', href='./lib/bootstrap-4.0.0/bootstrap-grid.min.css')
		doc.stag('link', rel='stylesheet', href='./css/print.css')
		doc.line('script', '', type='text/javascript', src='./js/interaction.js')

		with tag('body'):
					# with tag('div', id='dictFilter', klass='col-3'):
					# 	doc.line('span', 'Literature', style='margin-top:0;')
					# 	with tag('form'):
					# 		if(os.path.isfile('../lists/bookList.txt')):
					# 			with open('../lists/bookList.txt', 'rt') as bookList_file:
					# 				for book in bookList_file:
					# 					with tag('div', klass='tagWrapper'):
					# 						doc.line('span', book, klass='filterTag', type='book', value=book.lower().replace('\n', ''))
					# 				bookList_file.close()
					# 	doc.line('span', 'Authors')
					# 	with tag('form'):
					# 		if(os.path.isfile('../lists/authorList.txt')):
					# 			with open('../lists/authorList.txt', 'rt') as authorList_file:
					# 				for author in authorList_file:
					# 					authorPrint = author.split(',')[0]
					# 					with tag('div', klass='tagWrapper'):
					# 						doc.line('span', authorPrint, klass='filterTag', type='author', value=authorPrint.lower())
					# 				authorList_file.close()
					# 	doc.line('span', 'Tags')
					# 	with tag('form'):
					# 		if(os.path.isfile('../lists/tagList.txt')):
					# 			with open('../lists/tagList.txt', 'rt') as tagList_file:
					# 				for tagItem in tagList_file:
					# 					#doc.line('input', tagItem, type='checkbox', value=tagItem.replace(' ', '-'))
					# 					with tag('div', klass='tagWrapper'):
					# 						doc.line('span', tagItem.split(' ')[-0], klass='filterTag', type='tag', value=tagItem.lower().replace('\n', '').split(' ')[0])
					# 						doc.line('span', tagItem.split(' ')[-1], klass='countTag', type='tag')
					# 					#doc.asis('<br />')
					# 				tagList_file.close()
					# 	doc.line('span', 'Views')
					# 	with tag('div', klass='tagWrapper'):
					# 		doc.line('span', 'List', klass='viewTag', id='listViewToggle')
					# 		doc.line('span', 'Field', klass='viewTag active', id='fieldViewToggle')

			citlist = []
			entryCounter = 0;
			for letter in os.listdir("../dict/"):
				entryCounter += 1;
				thisCitation = dict()
				thisCitation['word'] = letter
				thisCitation['pageNr'] = entryCounter
				citlist.append(thisCitation)
				for word in os.listdir("../dict/" + letter):
					for citation in os.listdir("../dict/" + letter + "/" + word):
						thisCitation = dict()
						if( str("../dict/" + letter + "/" + word + '/' + citation).endswith('.csv') ):
							with open("../dict/" + letter + "/" + word + '/' + citation, "rt") as citation_csv:
								entryCounter += 1;
								thisCitation['pageNr'] = entryCounter
								thisCitation['letter'] = letter
								thisCitation['word'] = word
								for key,value in csv.reader(citation_csv, delimiter='|'):
									thisCitation[key] = value.split(',')[0].lower()
									if(key == 'quote'):
										thisCitation[key] = value
								if(key == 'tag'):
									thisCitation[key] = ''.join(value.split('+')[0]).lower()
								if(thisCitation['quote'] == 'img'):
									for imgFormat in imageFormats:
										if( os.path.isfile( "../dict/" + letter + "/" + word + '/' + citation.replace('csv', imgFormat) )):
											thisCitation['img'] = "./dict/" + letter + "/" + word + '/' + citation.replace('csv', imgFormat)
								citlist.append(thisCitation)
			
			duplex = 1
			# DUPLEX PRINTING
			citStraight = []
			citOdd = []
			if(duplex):
				citDuplex = citlist
				# sort straight and odd pages/cols
				for i,cit in enumerate(citDuplex):
					#print(i+1)
					if((i+1) % 2): # odd
						citOdd.append(cit)
					else: # straight
						citStraight.append(cit)
				if(len(citStraight) % 2 == True):
					citStraight.append({'word': ''})
				if(len(citOdd) % 2 == True):
					citOdd.append({'word': ''})
				print(len(citStraight))
				print(len(citOdd))
				# create the duplex weaving pattern
				pattern = [ True, True, True, True, False, False, False, False ]
				patternProj = []
				for x in range( round(len(citDuplex)/len(pattern)) ):
					patternProj.append(pattern)
				patternProj = flattenList(patternProj)
				# print(patternnProj)
				n = len(citlist) - len(patternProj)
				del patternProj[n:]
				citlist = []
				#print(citOdd[0])
				nextStraight = 'a'
				for item in patternProj:
					#print(item)
					if(item == True): # true = odd
						citlist.append(citOdd[:1])
						del citOdd[:1]
					else: # false = straight
						citlist.append(citStraight[:1])
						del citStraight[:1]
				citlist = flattenList(citlist)
				#print(len(citlist))
				#print(citlist)

				#print(len(citlist))
				#print(citlist)



			citQuads = []
			quadCounter = 0
			totalCounter = 0
			tempQuad = []
			for index,cit in enumerate(citlist):
				if(duplex == 1):
					if(quadCounter < 4):
						if( (len(citQuads) > 0) and (len(citQuads) % 2) == True): # only straight quads, switch positions 1 and 2 + 3 and 4
							if ((len(tempQuad)+1) % 2): # positions 1 and 3 of the straight quad
								if (len(citlist)-1) >= index+1:
									tempQuad.append(citlist[index+1])
									quadCounter+=1
							else: # positions 2 and 4 of the straight quad
								tempQuad.append(citlist[index-1])
								quadCounter+=1
						else: # for odd quads, proceed normally
							tempQuad.append(cit)
							quadCounter += 1
						# check if cit is the last item in citlist, if so push any unfinished quad
						if(cit == citlist[-1]):
							citQuads.append(tempQuad)
					else:
						# print(tempQuad)
						citQuads.append(tempQuad)
						tempQuad = []
						quadCounter = 0
						if( (len(citQuads) > 0) and (len(citQuads) % 2) == True): # only straight quads, switch positions 1 and 2 + 3 and 4
							if ((len(tempQuad)+1) % 2): # positions 1 and 3 of the straight quad
								if (len(citlist)-1) >= index+1:
									tempQuad.append(citlist[index+1])
									quadCounter+=1
							else: # positions 2 and 4 of the straight quad
								tempQuad.append(citlist[index-1])
								quadCounter+=1
						else: # for odd quads, proceed normally
							tempQuad.append(cit)
							quadCounter += 1
						if((cit == citlist[-1]) and (len(tempQuad)>0)) :
							citQuads.append(tempQuad)


				else: # duplex = 0
					if(quadCounter < 4):
						tempQuad.append(cit)
						quadCounter += 1
						# check if cit is the last item in citlist, if so push any unfinished quad
						if(cit == citlist[-1]):
							citQuads.append(tempQuad)
							totalCounter += 1
					else:
						# print(tempQuad)
						citQuads.append(tempQuad)
						tempQuad = []
						quadCounter = 0
						tempQuad.append(cit)
						quadCounter += 1
						#print('quad reset')

			print(len(citlist))
			print(len(flattenList(citQuads)))
			print(len(citQuads))

			prevWord = ''
			wordCount=1
			counter = 0;
			for quad in citQuads:
				with tag('div', klass='printWrapper'):
					for cit in quad:
						#print(cit)
						# manage the word count
						if cit['word'] == prevWord:
							wordCount += 1
						else: 
							wordCount = 1
						prevWord = cit['word']
						#draw the html
						with tag('div', klass='dictWord printCol'):
							with tag('div', style="padding:5mm;"):
								with tag('span'):
									if('quote' not in cit):
										with tag('div', klass='letterCol'):
											with tag('svg', height="100%", width="100%",):
												with tag('rect', height="100%", width="100%", fill='#000'):
													text('')
												with tag('text', klass='letterText', y="30", x="10"):
													text(cit['word'])
												counter += 1
									else:
										counter +=1
										text(str(cit['pageNr']) + ': ' + cit['word'])
										doc.line('sup', str(wordCount), klass='wordCount')
								with tag('div', klass='container-fluid'):
									with tag('div', klass='row'):
										# print(cit)
										if(('quote' in cit)):
											if (cit['quote'] == 'img'):
												#print('img')
												with tag('div', klass='imgWrapper'):
													doc.attr(style = 'background-image: url(" ' + cit['img'] + '");')
											else:
												with tag('div', klass='quote'):
													text( cit['quote'] )
										with tag('span',klass='credits'):
											if( ('author' in cit) and (len(cit["author"])) ):
												text(cit["author"])
												authorList.append(cit['author'].lower())
											if( ('title' in cit) and (len(cit["title"]) > 0) ):
												text(':')
												doc.asis('<br />')
												text(cit["title"])
											if( ('in' in cit) and (len(cit["in"]) > 0) ):
												doc.asis('<br />')
												text(cit['in'])
												bookList.append(cit['in'].lower())
											if( ('year' in cit) and (len(cit["year"]) > 0) ):
												doc.asis('<br />')
												text(cit["year"])
											if( ('pages' in cit) and (len(cit["pages"]) > 0) ):
												doc.asis('<br />')
												if(cit["pages"].startswith('http')):
													doc.line('a', '[link]', href=cit["pages"], target='_blank')
												else:
													text('p. ' + cit["pages"])
											if( ('tag' in cit) and (len(cit['tag']) > 0) ):
												doc.asis('<br /><br />')
												tags = cit['tag'].split('+')
												for tagItem in tags:
													tagList.append(tagItem.lower().replace(' ', ''))
													with tag('span', klass='tag'):
														tagItem = tagItem.replace(' ', '')
														#tagItem = str.encode(tagItem, 'utf-8')
														#print(type(tagItem))
														#print(tagItem)
														text('#' + tagItem)


					#with tag('div', klass='printWrapper'):
					# for letter in os.listdir("../dict/"):
					# 	with tag('div'):
					# 		if counter == 4:
					# 			doc.attr(klass='printWrapper')
					# 			counter = 1
					# 		with tag('div', klass='dictLetter printCol'):
					# 			text(letter)
					# 			counter += 1
					# 		for word in os.listdir("../dict/" + letter):
					# 			#print(bytes(word, 'utf-8'))
					# 			wordCount = 0
					# 			for citation in os.listdir("../dict/" + letter + "/" + word):
					# 				if( str("../dict/" + letter + "/" + word + '/' + citation).endswith('.csv') ):
					# 					wordCount += 1
					# 					with open("../dict/" + letter + "/" + word + '/' + citation, "rt") as citation_csv:
					# 						thisCitation = dict()
					# 						thisCitationBook = ''
					# 						thisCitationAuthor = ''
					# 						thisCitationTags = ''
					# 						for key,value in csv.reader(citation_csv, delimiter='|'):
					# 							thisCitation[key] = value
					# 							if(key == 'author'):
					# 								thisCitationAuthor += value.split(',')[0].lower()
					# 							elif(key == 'in'):
					# 								thisCitationBook += value.split(',')[0].lower()
					# 							elif(key == 'tag'):
					# 								tagString = ''.join(value.split('+'));
					# 								tagString = tagString.replace(' ','').lower()
					# 								thisCitationTags += tagString
					# 						with tag('div', klass='dictWord printCol', book=thisCitationBook, author=thisCitationAuthor, tag=thisCitationTags):
					# 							with tag('span'):
					# 								#word = bytes(word, 'utf-8')
					# 								text(word)
					# 							doc.line('sup', wordCount, style='font-size:0.5em; margin-left:-0.5em;')
					# 							with tag('div', klass='container-fluid'):
					# 								with tag('div', klass='row'):
					# 									with tag('div', klass='dictCitation printCol'):
					# 										#print(type(thisCitation['quote'].encode()))
					# 										if(thisCitation['quote'] == 'img'):
					# 											for imgFormat in imageFormats:
					# 												if( os.path.isfile( "../dict/" + letter + "/" + word + '/' + citation.replace('csv', imgFormat) )):
					# 													doc.stag('img', src="./dict/" + letter + "/" + word + '/' + citation.replace('csv', imgFormat))
					# 										else:
					# 											text( thisCitation['quote'] )
					# 										with tag('span',klass='credits'):
					# 											if( len(thisCitation["author"]) ):
					# 												text(thisCitation["author"])
					# 												authorList.append(thisCitation['author'].lower())
					# 											if( len(thisCitation["title"]) > 0 ):
					# 												text(':')
					# 												doc.asis('<br />')
					# 												text(thisCitation["title"])
					# 											if( len(thisCitation["in"]) > 0 ):
					# 												doc.asis('<br />')
					# 												text(thisCitation['in'])
					# 												bookList.append(thisCitation['in'].lower())
					# 											if( len(thisCitation["year"]) > 0 ):
					# 												doc.asis('<br />')
					# 												text(thisCitation["year"])
					# 											if( len(thisCitation["pages"]) > 0 ):
					# 												doc.asis('<br />')
					# 												if(thisCitation["pages"].startswith('http')):
					# 													doc.line('a', '[link]', href=thisCitation["pages"], target='_blank')
					# 												else:
					# 													text('p. ' + thisCitation["pages"])
					# 											if( len(thisCitation['tag']) > 0):
					# 												doc.asis('<br /><br />')
					# 												tags = thisCitation['tag'].split('+')
					# 												for tagItem in tags:
					# 													tagList.append(tagItem.lower().replace(' ', ''))
					# 													with tag('span', klass='tag'):
					# 														tagItem = tagItem.replace(' ', '')
					# 														#tagItem = str.encode(tagItem, 'utf-8')
					# 														#print(type(tagItem))
					# 														#print(tagItem)
					# 														text('#' + tagItem)

					# 								citation_csv.close()

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


bookList_file = open('../lists/bookList.txt', 'wt');
for book in bookList:
	bookList_file.write(book + '\n')

authorList_file = open('../lists/authorList.txt', 'wt');
for author in authorList:
	authorList_file.write(author + '\n')

tagList_file = open('../lists/tagList.txt', 'wt');
for tagItem in tagList:
	tagList_file.write(tagItem + '\n')

#print(doc.getvalue())
#print(type( indent(doc.getvalue(), newline = '\r\n').encode() ) )
file.write(indent(doc.getvalue(), newline = '\r\n').encode() )
#file.write(doc.getvalue())
file.close()