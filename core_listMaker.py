#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv
import os
import datetime
import locale
import shutil
import time 
encoding = locale.getpreferredencoding(True)
# import diary settings
from core_settings import * 
# function to create lists for books, tags and authors
def makeLists( ):
    bookList = []
    tagList = []
    authorList = []
    # loop data
    for letter in os.listdir(dataPath):
        for word in os.listdir(dataPath + letter):
            for citation in os.listdir(dataPath + letter + "/" + word):
                if( str(dataPath + letter + "/" + word + '/' + citation).endswith('.csv') ):
                    with open(dataPath + letter + "/" + word + '/' + citation, "rt") as citation_csv:
                        for key,value in csv.reader(citation_csv, delimiter='|'):
                            if key == "author":
                                if len( value ) > 1:
                                    authorList.append( value.split(',')[0].lower() )
                            if key == "in":
                                if len( value ) > 1:
                                    bookList.append( value.split(',')[0].lower() )
                            if key == "tag":
                                tagString = value.split('+')
                                for tag in tagString:
                                    if len( tag ) > 1:
                                        tagList.append(tag.replace(' ', ''))
    # sort lists
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
    # write list files
    bookList_file = open( listPath + 'bookList.txt', 'wt' );
    for book in bookList:
        bookList_file.write(book + '\n')
    authorList_file = open( listPath + 'authorList.txt', 'wt');
    for author in authorList:
        authorList_file.write(author + '\n')
    tagList_file = open( listPath + 'tagList.txt', 'wt');
    for tagItem in tagList:
        tagList_file.write(tagItem + '\n')
# for single execution
makeLists()