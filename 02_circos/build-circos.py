#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
from num2words import num2words

#helpers
def remUml(str):
    return str.replace('ä','a').replace('ö','o').replace('ü','u').replace('Ä','A').replace('Ö','O').replace('Ä','A').replace('Ü','U')

# template file
template = open('circos-template.html', 'r', encoding='utf-8')

# newly generated file takes the content of the template
file = open('../circos.html', 'w')

# temporarily store the template content
templateContent = template.readlines()
# template no longer needed
template.close()

# find spot in template to insert new js code
insertionIndex = 0
for index, line in enumerate(templateContent):
  if 'PYTHON-GENERATED-CODE' in line:
    # print(index, line)
    insertionIndex = index+1

##
## generate the new code
##

# build a dict of entries sorted by the date they were added
regions = []
entries = dict()
letters = sorted(os.listdir("../dict/"))
longest = dict()
for letter in letters:
    longest[letter] = 0
    for word in os.listdir('../dict/' + letter + '/'):
        for entry in os.listdir('../dict/' + letter + '/' + word + '/'):
            if entry.endswith('csv'):
                with open('../dict/' + letter + '/' + word + '/' + entry ) as entry_csv:
                    tempDict = dict()
                    for key,value in csv.reader(entry_csv, delimiter='|'):
                        tempDict[key] = value;
                        if key == 'dateAdded':
                            # dateAdded Pattern YYYYMMDD_TTTT
                            yyyy = str(value[:4]) #year
                            mm = value[4:6].replace('0', '') # month
                            dd = value[6:8] # day
                            # find out what quarter of the year the month is
                            q = 0
                            if int(mm) <= 4:
                                q = '1'
                            elif int(mm) <= 8:
                                q = '2'
                            else:
                                q = '3'
                            
                            # check if the year exists in the entries dict
                            if yyyy not in entries:
                                entries[yyyy] = dict() # stores the quarters
                                entries[yyyy][q] = dict()
                                entries[yyyy][q][letter] = dict()
                                entries[yyyy][q][letter]['content'] = [word] # stores the words
                                entries[yyyy][q][letter]['len'] = 1 # stores the word count
                            else:
                                if q not in entries[yyyy]:
                                    entries[yyyy][q] = dict()
                                    entries[yyyy][q][letter] = dict()
                                    entries[yyyy][q][letter]['content'] = [word]
                                    entries[yyyy][q][letter]['len'] = 1 # stores the word count
                                else:
                                    if letter not in entries[yyyy][q]:
                                        entries[yyyy][q][letter] = dict()
                                        entries[yyyy][q][letter]['content'] = []    
                                        entries[yyyy][q][letter]['len'] = 0    
                                    entries[yyyy][q][letter]['content'].append(word)
                                    entries[yyyy][q][letter]['len'] += 1

# find out what quarter has the most entries to eventually determine the region lengths
for year in entries:
    for quarter in entries[year]:
        for letter in entries[year][quarter]:
            if letter in entries[year][quarter] and entries[year][quarter][letter]['len'] > longest[letter]:
               longest[letter] = entries[year][quarter][letter]['len']

# generate the region code
for letter in letters:
    if letter in longest and longest[letter] > 0:
        regions.append('\t{ len: ' + str( longest[letter] ) + ', id: ' + '\'' + letter + '\'' + ', label: ' + '\'' + letter + '\'' + ', color: "#ffffff" },')

regions.insert(0, 'myCircos.layout( [')
regions.append('], regionConfig);')

# generate the tracks code
## the date added forms the tracks, one track for each year quarter
tracks = dict()
innerRegionRadius = 325
trackCounter = 1
trackFactor = 15
trackWidth = 10
for year in entries:
    for quarter in entries[year]:
        tracks[year+quarter] = []
        for letter in entries[year][quarter]:
            for index, word in enumerate(entries[year][quarter][letter]['content']):
                tracks[year+quarter].append( '\t{ block_id: "' + remUml(word[0].upper()) + '", start: ' + str(index) + ', end: ' + str(index+1) + ', value: "' + word + '" },' )
        tracks[year+quarter].insert(0,'myCircos.highlight( "' + num2words(int(year), to='year').replace(' ', '_') + "_" + num2words(int(quarter)) + '", [ ')
        tracks[year+quarter].append( '], { innerRadius: ' + str(innerRegionRadius-trackWidth-(trackCounter*trackFactor)) + ', outerRadius: ' + str(innerRegionRadius-(trackCounter*trackFactor)) + ' });' )
        trackCounter+=1

#generate the cords
chords = []
chords.append('\t{ source: { id: "A", start: 0, end: 1 } , target: { id: "O", start: 0, end: 1 }, },')
chords.insert(0, 'myCircos.chords( "chords", [')
chords.append('], chordsConfig);')

##
## insert the new code
##

# letters form the regions
for region in regions:
    templateContent.insert(insertionIndex, '\n\t\t' + region + '\n')
    insertionIndex += 1

for track in tracks:
    for item in tracks[track]:
        templateContent.insert(insertionIndex, '\n\t\t' + item + '\n')
        insertionIndex += 1

for chord in chords:
    templateContent.insert(insertionIndex, '\n\t\t' + chord + '\n')
    insertionIndex += 1
#
## transfer contents to the new file
#
templateContent = "".join(templateContent)
file.write(templateContent)

# close the new file
file.close()