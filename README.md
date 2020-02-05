**diary** is a low tech tool to mange image and text based references.

## Philosophy
- static web based reference display
- easily store data in your cloud service of trust, no additional service/client
- alphabetical ordering with meta filters and tags
- easily create a print backup of your references using the browser print dialogue
- easily create custom displays of references or stats through accessible csv data storage 

## Some day maybe
- rework the filters ui
- add date filters
- chrome plugin for saving images and pdfs: https://developer.chrome.com/extensions/getstarted
- create a proper program setup 
- add preferences
    - data storage location
- implement custom subjective user filters (e.g. for managing projects or major categories)

## How to use
You will need at least python 3.6 installed. Also yattag and pyqt5.

Currently there is no real proper concept for setting up **diary**. Just clone the repo and hit up ui_entryMaker.pyw. Entries are added from here.
Any data will be stored inside a */data/* folder inside the repo. HTML files will be generated in */output/*. Access the references display through */output/index.html*.