import pandas as pd
import numpy as np
import requests
import json

##TODO: create function to clean data files


##coverted txt to csv, read in
cite_1 = pd.read_csv("./data/2017-01to06-citeSkrutskie-NOTES.csv", skiprows=14, sep=',', header=None)
cite_1.columns = ["article", "note1", "note2", "note3", "note4", "note5"]
cite_1 = cite_1.iloc[:, 0:2]

##remove ambiguous answers
notna = cite_1['note1'].str.contains("YES|NO")
cite_1 = cite_1[notna]
##create col of only yes/no
cite_1['cited'] = np.where(cite_1['note1'].str.contains("YES"), 'yes', 'no')

##isolate article id to bibcode, reset index to prevent key errors
cite_1['bibcode'] = cite_1['article'].str.slice(start=9)
cite_1 = cite_1.reset_index()

##fetch article doi from API - search by bibcode
token = 'Fv6aJu1i3oV4uuG6LfStmnIg9Txxe1NfFY2vLRap'

doi = []

for bibcode in range(len(cite_1['bibcode'])):

    r = requests.get("https://api.adsabs.harvard.edu/v1/search/query?q=bibcode:" + cite_1['bibcode'][bibcode] + "&fl=doi", headers = {"Authorization": "Bearer " + token})
    newtext = json.loads(r.text)
    if not newtext['response']['docs']:
        doi.append(np.nan)
    else:
        if not newtext['response']['docs'][0]:
            doi.append(np.nan)
        else:
            doi.append(newtext['response']['docs'][0]['doi'])


doi = pd.Series(doi)
pattern = '\[|\]'
cite_1['doi'] = doi.str[0]

# export csv of identifiers
cleandf = cite_1.drop(['index','note1'],axis=1)
cleandf.to_csv("cleandf.csv",sep=',')

# find and download arxiv PDF with DOI

import urllib

#function to grab pdfs and store locally
def getthempdfs(doi_ids):
    retrieve = []
    for linenum, line in enumerate(doi_ids):
        if line != '':
            url = 'http://export.arxiv.org/api/query?search_query=all:' + line + '&start=0&max_results=1'
            data = urllib.request.urlopen(url).read()
            urlbegin = data.decode('utf8').find('http://arxiv.org/pdf/')  # beginning of pdf string
            if urlbegin != -1:
                if data[urlbegin] != 34:
                    pdfurl = data[urlbegin:urlbegin + 30]
                    urllib.request.urlretrieve(pdfurl.decode('utf8'), str(linenum) + '.pdf')
                else:
                    pdfurl = data[urlbegin + 1:urlbegin +31]
                    urllib.request.urlretrieve(pdfurl.decode('utf8'), str(linenum) + '.pdf')
            else: retrieve.append(linenum)
        else: continue
    return retrieve

getthempdfs(bits)

bits = cleandf["doi"][:5] # index 1 & 4 are problem

doi = '10.2298/SAJ160802003A'
url = 'http://export.arxiv.org/api/query?search_query=all:'+ doi + '&start=0&max_results=1'
data = urllib.request.urlopen(url).read()
urlbegin = data.decode('utf8').find('http://arxiv.org/pdf/') # beginning of pdf string
pdfurl = data[urlbegin + 1:urlbegin +31]
pdfurl = data[urlbegin:urlbegin+30]

urllib.request.urlretrieve(pdfurl.decode('utf8'),'thatwhat.pdf')


#extract and read PDF
from urllib.request import urlretrieve
import PyPDF2

urlretrieve('https://arxiv.org/pdf/1705.09063.pdf','whatwhat.pdf')
here = PyPDF2.PdfFileReader(open('whatwhat.pdf', 'rb'))
pg = here.getPage(0)
texts = pg.extractText()