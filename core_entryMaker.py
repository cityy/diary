#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import datetime
import locale
import importlib.util
import shutil
import time 

# custom script to generate the html
spec = importlib.util.spec_from_file_location("gen_HTML", "./gen_HTML.py")
gen_HTML = importlib.util.module_from_spec(spec)
encoding = locale.getpreferredencoding(True)

def run(data):
	keyword = data['keyword']
	author = data['authors']
	title = data['chapter']
	in_ = data['book']
	year = data['year']
	pages = data['pages']
	tag = data['tags']
	quote = data['quote']
	file = data['file']
	# text = data['text']
	date = str(datetime.datetime.now().strftime("%Y%m%d_%H%M"))

	path = './data/' + keyword[0].upper() + '/' + keyword.lower() + '/'
	filePath = './data/' + keyword[0].upper() + '/' + keyword.lower() + '/'

	if not os.path.isdir(path):
		os.mkdir(path)
	filename = author.split(',')[0] + "_" + year + "_" + date + '.csv'

	while os.path.isfile(path + filename):
		filename = author.split(',')[0] + str(randint(0,999)) + '.csv'

	newImagePath = ''
	newFilePath = ''
	newTextPath = ''

	if len(file) > 0 :
		fileType = file.split('.')[-1]
		newFilePath = filePath + filename.replace('.csv', '.' + fileType)
		shutil.copy2(file, newFilePath)
		# check if file is an image or a text
		if(fileType == 'jpg' or fileType == 'png' or fileType == 'gif'):
			newImagePath = "." + newFilePath
			newTextPath = ''
			print('is image')
		elif(fileType == 'pdf' or fileType == 'docx' or fileType == 'odt' or  fileType =='txt'):
			newImagePath = ''
			newTextPath = "." + newFilePath
			print('is text')
		else:
			print('is neither')
			newImagePath = ''
			newTextPath = ''

	with open(path + filename, 'wt') as f:
		w = csv.writer(f, delimiter='|', lineterminator='\n')
		w.writerow( [ 'author', author ] )
		# w.writerow(['translator', translator])
		w.writerow( [ 'title', title ] )
		# w.writerow(['editor', editor])
		w.writerow( [ 'in', in_ ] )
		# w.writerow(['location', location])
		# w.writerow(['publisher', publisher])
		w.writerow( [ 'year', year ] )
		w.writerow( [ 'pages', pages ] )
		w.writerow( [ 'tag', tag ] )
		#w.writerow(['significance', significance])
		w.writerow( [ 'quote', quote ] )
		w.writerow( [ 'image', newImagePath ] )
		w.writerow( [ 'text', newTextPath ] )
		w.writerow( [ 'dateAdded', date ] )
		w.writerow( [ 'dateModified', str( datetime.datetime.fromtimestamp ( os.path.getmtime( file ) ).strftime("%Y%m%d_%H%M") ) ] )
		#f.write()
		f.close();

	spec.loader.exec_module(gen_HTML)