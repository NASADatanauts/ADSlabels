# initial NLP preprocessing, experimentation for final model
from nltk.tokenize import regexp_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import sent_tokenize
from nltk.stem import SnowballStemmer
from nltk.stem. porter import *

pattern = r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)?"

f = open('./txts/' + '0' + '.pdf.txt', encoding = 'utf-8')
test = f.read()

testsent = sent_tokenize(test)
wnlemma = WordNetLemmatizer()
testsplit_sentences = []
for sentence in testsent:
    tokens = regexp_tokenize(sentence,pattern)
    tokens = [wnlemma.lemmatize(w) for w in tokens]
    testsplit_sentences.append(tokens)


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder
from numpy import nan

#prepare dataframe for sklearn
noblank = fulldata.replace('', np.nan, regex=True)
reduced = noblank[~pd.isnull(noblank.text)]
reduced = reduced.loc[:,('2mass','skrutskie','text')]

encodeskrut = pd.get_dummies(reduced.loc[:, 'skrutskie'], drop_first=True, prefix = 'skrut')

x = pd.concat([encodeskrut,reduced.loc[:,'text']], axis = 1, sort = False)
y = pd.get_dummies(reduced.loc[:,'2mass'], drop_first=True, prefix = '2mass')

