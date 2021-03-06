# initial NLP preprocessing, experimentation for final model
import numpy as np
import pandas as pd

# import data
fulldata = pd.read_csv('./data/fulldata.csv', index_col=0)


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

#prepare dataframe for sklearn
noblank = fulldata.replace('', np.nan, regex=True)
reduced = noblank[~pd.isnull(noblank.text)]
reduced = reduced.loc[:,('2mass','text')]

# encodeskrut = pd.get_dummies(reduced.loc[:, 'skrutskie'], drop_first=True, prefix = 'skrut')

# x = pd.concat([encodeskrut,reduced.loc[:,'text']], axis = 1, sort = False)
# simplex = x.loc[:,'text']
simplex = reduced[['text']]
y = pd.get_dummies(reduced.loc[:,'2mass'], drop_first=True, prefix = '2mass')

y = np.ravel(y)

simplex_train, simplex_test, y_train, y_test = train_test_split(simplex, y, test_size=0.3, random_state=27)
y_train = np.ravel(y_train)

# convert text
count_vect = CountVectorizer()
tfidf = TfidfTransformer()
simplex_train_count = count_vect.fit_transform(simplex_train)
simplex_train_tfidf = tfidf.fit_transform(simplex_train_count)

simplex_test_count = count_vect.transform(simplex_test) #use transform for all test inputs
simplex_test_tfidf = tfidf.transform(simplex_test_count)

# initial model with naive Bayes
nbmodel = MultinomialNB().fit(simplex_train_tfidf, y_train)
y_pred_nb = nbmodel.predict(simplex_test_tfidf)

#scoring
accuracy_score(y_test, y_pred_nb)


#logistic regression for baseline
from sklearn.linear_model import LogisticRegression

logreg = LogisticRegression().fit(simplex_train_tfidf, y_train)
y_pred_log = logreg.predict(simplex_test_tfidf)

accuracy_score(y_test, y_pred_log) #same as Naive Bayes


#support vector machine

from sklearn.linear_model import SGDClassifier
svmmodel = SGDClassifier(loss='hinge', penalty="l2", alpha=1e-3, max_iter=5, random_state=27)

_ = svmmodel.fit(simplex_train_tfidf, y_train)
y_pred_svm = svmmodel.predict(simplex_test_tfidf)

accuracy_score(y_test, y_pred_svm) #same as Naive Bayes


#create pipeline
from sklearn.pipeline import Pipeline
nb_pipe = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', MultinomialNB())])

#next - grid search for ngram range, use idf, alpha
from sklearn.model_selection import GridSearchCV
parameters = {'vect__ngram_range': [(1,1),(1,2)],
              'tfidf__use_idf': (True, False),
              'clf__alpha': (0.0001, 0.001, 0.01, 0.1)}

grid_nb = GridSearchCV(nb_pipe, parameters, cv=3, n_jobs=-1) #-1 n_jobs for multicore
grid_nb = grid_nb.fit(simplex, y)

grid_nb.best_score_  # 81.5%, 81.1% with full set
grid_nb.best_params_  # best ngrams is 1

#with stemming

from nltk.stem import SnowballStemmer
stemmer = SnowballStemmer("english", ignore_stopwords=True)

class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: ([stemmer.stem(w) for w in analyzer(doc)])

stemmed_count_vect = StemmedCountVectorizer(stop_words='english')

stem_pipe = Pipeline([('vect', stemmed_count_vect),
                      ('tfidf', TfidfTransformer()),
                      ('clf', MultinomialNB(fit_prior=False))])

stem_pipe = stem_pipe.fit(simplex_train, y_train)

pred_stemmed = stem_pipe.predict(simplex_test)

accuracy_score(y_test, pred_stemmed) #still only 75%

grid_stem_nb = GridSearchCV(stem_pipe, parameters, cv=3, n_jobs=-1) # -1 n_jobs for multicore
grid_stem_nb = grid_stem_nb.fit(simplex_train, y_train)

grid_stem_nb.best_score_ # 81.5% again, 81.1% with full set -- stemming does not seem to affect outcome
grid_stem_nb.best_params_


#support vector machine gridsearch

svm_pipe = Pipeline([('vect', CountVectorizer()),
                    ('tfidf', TfidfTransformer()),
                    ('clf', SGDClassifier(loss='hinge', penalty="l2", max_iter=5, random_state=27))])

parameters = {'vect__ngram_range': [(1,1),(1,2)],
              'tfidf__use_idf': (True, False),
              'clf__alpha': (0.0001, 0.001, 0.01)}

grid_svm = GridSearchCV(svm_pipe, parameters, cv=3, n_jobs=-1)
grid_svm = grid_svm.fit(simplex, y)

grid_svm.best_score_ # 78.9%
grid_svm.best_params_ # ngrams changed to 2, alpha still 0.001, use_idf may be changed to True for all

svm_pipe = Pipeline([('vect', CountVectorizer(ngram_range=(1,2))),
                    ('tfidf', TfidfTransformer(use_idf=True)),
                    ('clf', SGDClassifier(loss='hinge', penalty="l2", max_iter=5, random_state=27, alpha=0.001))])

parameters = {'clf__eta0': (0.0001, 0.001),
              'clf__power_t': (0.15, 0.2)}

grid_svm = GridSearchCV(svm_pipe, parameters, cv=3, n_jobs=-1)
grid_svm = grid_svm.fit(simplex, y)

grid_svm.best_score_ # no improvement with adjusted values
grid_svm.best_params_


# add skrut back in, use optimized Naive Bayes

count_vect = CountVectorizer(ngram_range=(1,1))
tfidf = TfidfTransformer(use_idf=True)
simplex_count = count_vect.fit_transform(simplex)
simplex_tfidf = tfidf.fit_transform(simplex_count)

from scipy.sparse import hstack
x_skrut_tfidf = hstack((simplex_tfidf, np.array(x['skrut_yes'])[:,None]))

nb_skrut = Pipeline([('clf', MultinomialNB())])

parameters = {'clf__alpha': (0.001, 0.01, 0.1)}

grid_nb_skrut = GridSearchCV(nb_skrut, parameters, cv=3, n_jobs=-1)
grid_nb_skrut = grid_nb_skrut.fit(x_skrut_tfidf, y)

grid_nb_skrut.best_score_ # 79.2% -- model is slightly worse than without skrut.
grid_nb_skrut.best_params_

# best combination (81.1%): simple nb, no skrut, alpha = 0.001, use_idf = True, ngrams = (1,1)

# look at most explanatory words (class 1 - yes, class 0 - no for 2mass)

vect = CountVectorizer(ngram_range=(1,1))
vect_fit = vect.fit_transform(simplex)
tfidf = TfidfTransformer(use_idf=True).fit_transform(vect_fit)
clf = MultinomialNB(alpha=0.001).fit(tfidf, y)

nb_coefs = clf.coef_
nb_coefs = [item for sublist in nb_coefs.tolist() for item in sublist]
words = vect.vocabulary_

grouped = list(zip(words.keys(),nb_coefs))
sort_group = sorted(grouped, key=lambda x: x[1], reverse=True)

top50_words = pd.DataFrame(sort_group[:50], columns=['word','coefficient'])
bottom50_words = pd.DataFrame(sort_group[-50:], columns=['word','coefficient'])

highest100_words = pd.concat([top50_words, bottom50_words], axis=0)

# notes for word coefficients
# om2pha is a program for clarifying celestial position for spectral fitting (detection/classification)
# kauffmann (co-)authored popular papers using 2MASS or relating to it
# numbers are likely stellar objects

# adding custom token to CountVectorizer, rerun GridSearchCV

vect = CountVectorizer(ngram_range=(1,1), token_pattern=r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)?")
vect_fit = vect.fit_transform(simplex_train)
tfidf = TfidfTransformer(use_idf=True)
tfidf_fit = tfidf.fit_transform(vect_fit)
clf = MultinomialNB(alpha=0.001).fit(tfidf_fit, y_train)

simplex_test_count = vect.transform(simplex_test) #use transform for all test inputs
simplex_test_tfidf = tfidf.transform(simplex_test_count)

pred_regex = clf.predict(simplex_test_tfidf)

accuracy_score(y_test, pred_regex) # 78.4% -- reduced from when using default tokenizer

nb_coefs = clf.coef_
nb_coefs = [item for sublist in nb_coefs.tolist() for item in sublist]
words = vect.vocabulary_

grouped = list(zip(words.keys(),nb_coefs))
sort_group = sorted(grouped, key=lambda x: x[1], reverse=True)

top50_words = pd.DataFrame(sort_group[:50], columns=['word','coefficient'])
bottom50_words = pd.DataFrame(sort_group[-50:], columns=['word','coefficient'])

highest100_words = pd.concat([top50_words, bottom50_words], axis=0)