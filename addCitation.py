#!/usr/bin/env python
# -*- coding: utf-8 -*-

import chardet
import csv
import csv
import os
from random import randint
import locale
from io import BytesIO
from io import StringIO
import codecs
import datetime
encoding = locale.getpreferredencoding(True)

keyword = ''
author = ''
translator = ''
title = ''
editor = ''
in_ = ''
location = ''
publisher = ''
year = ''
pages = ''
tag = ''
significance = ''
quote = ''
date = str(datetime.datetime.now().strftime("%Y%m%d_%H%M"))

print('ADD A NEW CITATION TO THE CATALOGUE // PLEASE ENTER DETAILS // LEAVE BLANK IF NOT APPLICABLE')

keyword = input('KEYWORD TO STORE THE QUOTE: ')
quote = input('THE QUOTE: ')
author = input("AUTHOR: ")
title = input("Book/Essay/Chapter/Article TITLE: ")
in_ = input("CONTAINING BOOK: ")
year = input("YEAR: ")
pages = input("PAGES: ")
tag = input("TAGS (tag1 + tag2 + ...): ")
#significance = input("primary or secondary quote? (primary/secondary): ")

path = '../dict/' + keyword[0].upper() + '/' + keyword.lower() + '/'
if not os.path.isdir(path):
	os.mkdir(path)

filename = author.split(',')[0] + "_" + year + "_" + date + '.csv'
#str(randint(0,999))
while os.path.isfile(path + filename):
	filename = author.split(',')[0] + str(randint(0,999)) + '.csv'

with open(path + filename, 'wt') as f:
	w = csv.writer(f, delimiter='|', lineterminator='\n')
	w.writerow(['author', author])
	w.writerow(['translator', translator])
	w.writerow(['title', title])
	w.writerow(['editor', editor])
	w.writerow(['in', in_])
	w.writerow(['location', location])
	w.writerow(['publisher', publisher])
	w.writerow(['year', year])
	w.writerow(['pages', pages])
	w.writerow(['tag', tag])
	#w.writerow(['significance', significance])
	w.writerow(['quote', quote])
	w.writerow(['dateAdded', date])
	#f.write()
	f.close();

# for row in r:
# 	for char in row:
# 		print char.decode('utf-8')
# 	#print chardet.detect(row[0])['encoding']
#print("eCREATED CITATION FILE " + path + filename)
	#f.close()

import generateHTML