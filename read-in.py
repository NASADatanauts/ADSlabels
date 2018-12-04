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
from bs4 import BeautifulSoup
import lxml

#function to grab pdfs and store locally - takes a list of DOIs, returns indexes that fail
def getthempdfs(doi_ids):
    retrieve = []
    for linenum, line in enumerate(doi_ids):
        if line != '' and not pd.isnull(line):
            url = 'http://export.arxiv.org/api/query?search_query=all:' + line + '&start=0&max_results=1'
            data = urllib.request.urlopen(url).read()
            urlbegin = data.decode('utf8').find('http://arxiv.org/pdf/')  # beginning of pdf string
            if urlbegin != -1:
                soup = BeautifulSoup(data, 'html.parser')
                tags = soup.find_all('link')
                for tag in tags:
                    if tag.get('href').find('pdf'):
                        urllib.request.urlretrieve(pdfurl.decode('utf8'), './pdfs/' + str(linenum) + '.pdf')
                    else: retrieve.append("NA")
            else: retrieve.append(linenum)
        else: continue
    return retrieve

getthempdfs(bits)
print(getthempdfs(cleandf["doi"]))
getthempdfs(cleandf['doi'][40:50])


#extract and read PDF
from urllib.request import urlretrieve
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.layout import LAParams
import os

urlretrieve('https://arxiv.org/pdf/1705.09063.pdf','./pdfs/whatwhat.pdf')

# takes filepath, returns text of single document
def pdf_to_text(path):
    here = open(path, 'rb')
    retstr = StringIO()
    laparams = LAParams()

    mgr = PDFResourceManager()
    device = TextConverter(mgr, retstr, codec='utf-8', laparams=laparams)
    interpret = PDFPageInterpreter(mgr, device)

    for page in PDFPage.get_pages(here, check_extractable=True):
        interpret.process_page(page)

    text = retstr.getvalue()

    here.close()
    device.close()
    retstr.close()

    return text


fulltext = pdf_to_text('whatwhat.pdf')

# take open directory, save directory -- saves .txt from PDF to save directory
def pdf_text_save(open_dir, save_dir):
    filelist = os.listdir(open_dir)
    for index, file in enumerate(filelist):
        text = pdf_to_text(open_dir + '/' + file)
        lowertext = text.lower()
        begin = lowertext.find("introduction")
        end = lowertext.rfind("references")
        prune_text = lowertext[begin:end]

        f = open(save_dir + '/' + str(index) + '.txt', 'w', encoding='utf-8')
        f.write(prune_text)
        f.close()


pdf_text_save('./pdfs','./txts')