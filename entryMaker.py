#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import datetime
import locale
import importlib.util
import shutil

# custom script to generate the html
spec = importlib.util.spec_from_file_location("generateHTML", "../00_tools/generateHTML.py")
generateHTML = importlib.util.module_from_spec(spec)
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

	path = '../dict/' + keyword[0].upper() + '/' + keyword.lower() + '/'
	filePath = './dict/' + keyword[0].upper() + '/' + keyword.lower() + '/'

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
		shutil.copy2(file, '.' + newFilePath)
		# check if file is an image or a text
		if(fileType == 'jpg' or fileType == 'png' or fileType == 'gif'):
		# if('jpg' in fileType or 'png' in fileType or 'gif' in fileType):
			newImagePath = newFilePath
			# newImagePath = newFilePath
			newTextPath = ''
			print('is image')
		elif(fileType == 'pdf' or fileType == 'docx' or fileType == 'odt' or  fileType =='txt'):
		# elif('pdf' in fileType or 'docx' in fileType or'odt' in fileType or 'txt' in fileType):
			newImagePath = ''
			newTextPath = newFilePath
			print('is Text')
		else:
			print('is neither')
			newImagePath = ''
			newTextPath = ''

	with open(path + filename, 'wt') as f:
		w = csv.writer(f, delimiter='|', lineterminator='\n')
		w.writerow(['author', author])
		# w.writerow(['translator', translator])
		w.writerow(['title', title])
		# w.writerow(['editor', editor])
		w.writerow(['in', in_])
		# w.writerow(['location', location])
		# w.writerow(['publisher', publisher])
		w.writerow(['year', year])
		w.writerow(['pages', pages])
		w.writerow(['tag', tag])
		#w.writerow(['significance', significance])
		w.writerow(['quote', quote])
		w.writerow(['image', newImagePath])
		w.writerow(['text', newTextPath])
		w.writerow(['dateAdded', date])
		#f.write()
		f.close();

	spec.loader.exec_module(generateHTML)