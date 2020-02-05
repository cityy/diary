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
# import diary settings
from core_settings import * 
from core_listMaker import makeLists
# custom script to generate stats
spec = importlib.util.spec_from_file_location("generateSTATS", "./gen_HTML_stats.py")
gen_STATS = importlib.util.module_from_spec(spec)
# refresh lists for filter generation
makeLists()
# generate the HTML file
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
					## filters
					with tag('div', id='dictFilter', klass='col-24'):
						with tag('div', klass="row, filterRow"):
							with tag('form'):
								with tag('div', klass="tagWrapper"):
									doc.line('span', 'Display', klass="titleTag")
								with tag('div', klass="tagWrapper"):
									doc.line('span', 'Alphabet', klass="displayTag", type="alphabet", value="alphabet", id='fieldViewToggle')
								with tag('div', klass="tagWrapper"):
									doc.line('span', 'Alphabet-Compact', klass="displayTag", type="alphabet-compact", value="alphabet-compact", id='listViewToggle')
								with tag('div', klass="tagWrapper"):
									doc.line('span', 'Blog', klass="displayTag", type="blog", value="blog")
								with tag('div', klass="tagWrapper"):
									doc.line('span', 'Blog-Compact', klass="displayTag", type="blog-compact", value="blog-compact")
						with tag('div', klass="row, filterRow"):
							with tag('form'):
								with tag('div', klass="tagWrapper"):
									doc.line('span', 'Literature', klass="titleTag")
								if(os.path.isfile('./data-lists/bookList.txt')):
									with open('./data-lists/bookList.txt', 'rt') as bookList_file:
										for book in bookList_file:
											with tag('div', klass='tagWrapper'):
												doc.line('span', book, klass='filterTag', type='book', value=book.lower().replace('\n', ''))
										bookList_file.close()
						with tag('div', klass="row, filterRow"):
							with tag('form'):
								with tag('div', klass="tagWrapper"):
									doc.line('span', 'Authors', klass="titleTag")
								if(os.path.isfile('./data-lists/authorList.txt')):
									with open('./data-lists/authorList.txt', 'rt') as authorList_file:
										for author in authorList_file:
											authorPrint = author.split(',')[0]
											with tag('div', klass='tagWrapper'):
												doc.line('span', authorPrint, klass='filterTag', type='author', value=authorPrint.lower())
										authorList_file.close()
						with tag('div', klass="row, filterRow"):
							with tag('form'):
								with tag('div', klass="tagWrapper"):
									doc.line('span', 'Tags', klass="titleTag")
								if(os.path.isfile('./data-lists/tagList.txt')):
									with open('./data-lists/tagList.txt', 'rt') as tagList_file:
										for tagItem in tagList_file:
											with tag('div', klass='tagWrapper'):
												doc.line('span', tagItem.split(' ')[-0], klass='filterTag', type='tag', value=tagItem.lower().replace('\n', '').split(' ')[0])
												doc.line('span', tagItem.split(' ')[-1], klass='countTag', type='tag')
										tagList_file.close()

					## entries
					for letter in os.listdir(dataPath):
						with tag('div', klass='dictLetter col'):
							text(letter)
						for word in os.listdir(dataPath + letter):
							#print(bytes(word, 'utf-8'))
							wordCount = 0
							for citation in os.listdir(dataPath + letter + "/" + word):
								if( str(dataPath + letter + "/" + word + '/' + citation).endswith('.csv') ):
									wordCount += 1
									with open(dataPath + letter + "/" + word + '/' + citation, "rt") as citation_csv:
										thisCitation = dict()
										thisCitationBook = ''
										thisCitationAuthor = ''
										thisCitationTags = ''
										print( citation )
										for key,value in csv.reader(citation_csv, delimiter='|'):
											thisCitation[key] = value
										with tag('div', klass='dictWord col-3', book=thisCitationBook, author=thisCitationAuthor, tag=thisCitationTags):
											with tag('span'):
												#word = bytes(word, 'utf-8')
												text(word)
											doc.line('sup', wordCount, style='font-size:0.5em; margin-left:-0.5em;')
											with tag('div', klass='container-fluid'):
												with tag('div', klass='row'):
													with tag('div', klass='dictCitation col'):
														# IMAGES
														# new image behaviour
														if('image' in thisCitation):
															if (len(thisCitation["image"]) > 0):
																doc.stag('img', src=thisCitation["image"])
														## TEXT
														if('text' in thisCitation):
															if (len(thisCitation["text"]) > 0):
																with tag('a', href=thisCitation["text"]):
																	text(thisCitation["text"].split('.')[-1].upper())
														# this is old image behaviour
														if("quote" in thisCitation):
															if (thisCitation['quote'] == 'img'):
																for imgFormat in imageFormats:
																	if( os.path.isfile( dataPath + letter + "/" + word + '/' + citation.replace('csv', imgFormat) )):
																		doc.stag('img', src="." + dataPath + letter + "/" + word + '/' + citation.replace('csv', imgFormat))
															else:
																text( thisCitation['quote'] )
														# CITATION DATA
														with tag('span',klass='credits'):
															if( len( thisCitation["author"]) ):
																text( thisCitation["author"] )
															if( len(thisCitation["title"]) > 0 ):
																text(':')
																doc.asis('<br />')
																text(thisCitation["title"])
															if( len(thisCitation["in"]) > 0 ):
																doc.asis('<br />')
																text(thisCitation['in'])
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
																	with tag('span', klass='tag'):
																		tagItem = tagItem.replace(' ', '')
																		text('#' + tagItem)

												citation_csv.close()

#print(doc.getvalue())
#print(type( indent(doc.getvalue(), newline = '\r\n').encode() ) )
file.write(indent(doc.getvalue(), newline = '\r\n').encode() )
#file.write(doc.getvalue())
file.close()

spec.loader.exec_module(gen_STATS)