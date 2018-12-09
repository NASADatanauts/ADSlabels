import urllib
from bs4 import BeautifulSoup

#function to grab pdfs and store locally - takes a list of DOIs, returns line numbers if not on arxiv and NA when no PDF found
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
                    maypdf = tag.get('href')
                    if maypdf.find('arxiv.org/pdf') != -1:
                        urllib.request.urlretrieve(maypdf, './pdfs/' + str(linenum) + '.pdf')
                    else: retrieve.append("NA")
            else: retrieve.append(linenum)
        else: continue
    return retrieve



#extract and read PDF
from urllib.request import urlretrieve
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from io import StringIO
from pdfminer.layout import LAParams
import os

# takes filepath, returns text of single PDF document
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


# takes open directory, start/stop indices, save directory -- saves .txt from PDF in open directory to save directory
def pdf_text_save(open_dir, start, stop, save_dir):
    filelist = os.listdir(open_dir)[start:stop]
    for file in filelist:
        text = pdf_to_text(open_dir + '/' + file)
        lowertext = text.lower()
        begin = lowertext.find("introduction")
        end = lowertext.rfind("references")
        prune_text = lowertext[begin:end]

        f = open(save_dir + '/' + str(file) + '.txt', 'w', encoding='utf-8')
        f.write(prune_text)
        f.close()