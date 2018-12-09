import pandas as pd
import numpy as np
import requests
import json

# text files partially needed to be cleaned in Excel to obtain bibcodes -- inconsistent labelling
# Excel also needed to properly format the text file to be read in as a CSV
# 2mass = used 2MASS, skrutskie = cited skrutskie yes/no

## 2017-01to06
##coverted txt to csv, read in
cite_1 = pd.read_csv("./data/2017-01to06-citeSkrutskie-NOTES.csv", skiprows=14, sep=',', header=None)
cite_1.columns = ["article", "note1", "note2", "note3", "note4", "note5"]
cite_1 = cite_1.iloc[:, 0:2]

##remove ambiguous answers
notna = cite_1['note1'].str.contains("YES|NO")
cite_1 = cite_1[notna]
##create col of only yes/no
cite_1['2mass'] = np.where(cite_1['note1'].str.contains("YES"), 'yes', 'no')
# create col of Skrutskie yes/no
cite_1['skrutskie'] = 'yes'

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
cite_1['doi'] = doi.str[0]

# export csv of identifiers
cleandf = cite_1.drop(['index','note1'],axis=1)
cleandf.to_csv("cleandf.csv",sep=',')

## 2017-01to06-NO
##coverted txt to csv, read in
cite_2 = pd.read_csv("./data/2017-01to06-NOciteSkrutskie-NOTES.csv", skiprows=23, sep=',', header=None)
cite_2.columns = ["article", "note1", "note2", "note3", "note4"]
cite_2 = cite_2.iloc[:, 0:2]

##remove ambiguous answers
notna = cite_2['note1'].str.contains("YES|NO")
cite_2 = cite_2[notna]
##create col of only yes/no
cite_2['2mass'] = np.where(cite_2['note1'].str.contains("YES"), 'yes', 'no')
# create col of Skrutskie yes/no
cite_2['skrutskie'] = 'no'

##isolate article id to bibcode, reset index to prevent key errors
cite_2['bibcode'] = cite_2['article'].str.slice(start=9)
cite_2 = cite_2.reset_index()


##fetch article doi from API - search by bibcode
token = 'Fv6aJu1i3oV4uuG6LfStmnIg9Txxe1NfFY2vLRap'

doi = []

for bibcode in range(len(cite_2['bibcode'])):

    r = requests.get("https://api.adsabs.harvard.edu/v1/search/query?q=bibcode:" + cite_2['bibcode'][bibcode] + "&fl=doi", headers = {"Authorization": "Bearer " + token})
    newtext = json.loads(r.text)
    if not newtext['response']['docs']:
        doi.append(np.nan)
    else:
        if not newtext['response']['docs'][0]:
            doi.append(np.nan)
        else:
            doi.append(newtext['response']['docs'][0]['doi'])


doi = pd.Series(doi)
cite_2['doi'] = doi.str[0]

# export csv of identifiers
cleandf2 = cite_2.drop(['index','note1'],axis=1)
cleandf2.to_csv("cleandf2.csv",sep=',')


## 2017-06to12
##coverted txt to csv, read in
cite_3 = pd.read_csv("./data/2017-06to12-citeSkrutskie-NOTES.csv", skiprows=10, sep=',', header=None)
cite_3.columns = ["article", "note1", "note2", "note3"]
cite_3 = cite_3.iloc[:, 0:2]

##remove ambiguous answers
notna = ~pd.isnull(cite_3['note1'].str.contains("YES|NO"))
cite_3 = cite_3[notna]
##create col of only yes/no
cite_3['2mass'] = np.where(cite_3['note1'].str.contains("YES"), 'yes', 'no')
# create col of Skrutskie yes/no
cite_3['skrutskie'] = 'yes'

##isolate article id to bibcode, reset index to prevent key errors
cite_3['bibcode'] = cite_3['article'].str.slice(start=9)
cite_3 = cite_3.reset_index()


##fetch article doi from API - search by bibcode
token = 'Fv6aJu1i3oV4uuG6LfStmnIg9Txxe1NfFY2vLRap'

doi = []

for bibcode in range(len(cite_3['bibcode'])):

    r = requests.get("https://api.adsabs.harvard.edu/v1/search/query?q=bibcode:" + cite_3['bibcode'][bibcode] + "&fl=doi", headers = {"Authorization": "Bearer " + token})
    newtext = json.loads(r.text)
    if not newtext['response']['docs']:
        doi.append(np.nan)
    else:
        if not newtext['response']['docs'][0]:
            doi.append(np.nan)
        else:
            doi.append(newtext['response']['docs'][0]['doi'])


doi = pd.Series(doi)
cite_3['doi'] = doi.str[0]

# export csv of identifiers
cleandf3 = cite_3.drop(['index','note1'],axis=1)
cleandf3.to_csv("cleandf3.csv",sep=',')


## 2017-06to12-NO
##coverted txt to csv, read in
cite_4 = pd.read_csv("./data/2017-06to12-NOciteSkrutskie-NOTES.csv", skiprows=11, sep=',', header=None)
cite_4.columns = ["article", "note1", "note2", "note3"]
cite_4 = cite_4.iloc[:, 0:2]

##remove ambiguous answers
notna = cite_4['note1'].str.contains("YES|NO")
cite_4 = cite_4[notna]
##create col of only yes/no
cite_4['2mass'] = np.where(cite_4['note1'].str.contains("YES"), 'yes', 'no')
# create col of Skrutskie yes/no
cite_4['skrutskie'] = 'yes'

##isolate article id to bibcode, reset index to prevent key errors
cite_4['bibcode'] = cite_4['article'].str.slice(start=9)
cite_4 = cite_4.reset_index()


##fetch article doi from API - search by bibcode
token = 'Fv6aJu1i3oV4uuG6LfStmnIg9Txxe1NfFY2vLRap'

doi = []

for bibcode in range(len(cite_4['bibcode'])):

    r = requests.get("https://api.adsabs.harvard.edu/v1/search/query?q=bibcode:" + cite_4['bibcode'][bibcode] + "&fl=doi", headers = {"Authorization": "Bearer " + token})
    newtext = json.loads(r.text)
    if not newtext['response']['docs']:
        doi.append(np.nan)
    else:
        if not newtext['response']['docs'][0]:
            doi.append(np.nan)
        else:
            doi.append(newtext['response']['docs'][0]['doi'])


doi = pd.Series(doi)
cite_4['doi'] = doi.str[0]

# export csv of identifiers
cleandf4 = cite_4.drop(['index','note1'],axis=1)
cleandf4.to_csv("cleandf4.csv",sep=',')



# combine dataframes
frames = [cleandf, cleandf2, cleandf3, cleandf4]
fulldata = pd.concat(frames)
fulldata = fulldata.reset_index(drop=True)

# find and download arxiv PDF with DOI
print(getthempdfs(fulldata["doi"]))
#returns 115 out of 312 in first batch
#returns 451 out of 1436 in full batch


# take pdfs from first directory, convert to text, save in second directory
# chunked individually to check progress and prevent stoppage
pdf_text_save('./pdfs', 0, 50, './txts')
pdf_text_save('./pdfs', 50, 100, './txts')
pdf_text_save('./pdfs', 100, 150, './txts')
pdf_text_save('./pdfs', 150, 200, './txts')
pdf_text_save('./pdfs', 200, 250, './txts')
pdf_text_save('./pdfs', 250, 300, './txts')
pdf_text_save('./pdfs', 300, 350, './txts')
pdf_text_save('./pdfs', 350, 400, './txts')
pdf_text_save('./pdfs', 400, 451, './txts')
