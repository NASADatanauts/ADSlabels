# ADSlabels
Finding all Astrophysics Data System papers with ML/NLP

Full description may be found on the [official Datanauts project page](https://open.nasa.gov/explore/datanauts/app/solve/using-machine-learning-find-nasa-data-ads).

Classification with Python: 2MASS or not 2MASS?



**CONTENTS**

Data collection

Data processing

Using the model

Acknowledgements

--------------

#### DATA COLLECTION

Training data provided by Luisa Rebull, listing articles, manual determination of whether the dataset used 2MASS, and whether the paper gave proper attribution to the dataset through citing the Skrutskie et al paper.
The text for each article was extracted from PDFs found on the physics arXiv; not all articles were available from this source.

#### DATA PROCESSING

The raw datasets from Luisa Rebull were transformed into a tidy format (data/fulldata.csv) with read-in.py.

Fetch PDFs of papers listed in fulldata.csv with getthempdfs in functions.py. Run these through pdf_to_text to get the parsed text, then through pdf_text_save to extract the bulk of the article (excluding references and abstract).

nlprocess.py then converts string-filled columns to dummy variables to train sklearn models.

nlprocess uses TF-IDF and Count Vectorizer to bring out words (tokens) that are most descriptive of the texts.

Stemming did not seem to affect the accuracy of the model, so for simplicity I recommend against stemming here. The model that best predicted the test set (81.1% accuracy) after using GridSearch to find parameters on different model types was a Naive Bayes. This model left out the variable containing whether the paper cited Skrutskie et al, alpha = 0.001, use_idf = True, ngram of 1.

This accuracy held as best, even after creating a custom tokenizer.

#### USING THE MODEL

Run imports from nlprocess.py, then lines 16-30 to create a clean dataset with a training and test set. Initialize tf-idf and Count Vectorizer, then fit/transform the data.

```
count_vect = CountVectorizer(ngram_range=(1,1))
tfidf = TfidfTransformer(use_idf=True)

simplex_train_count = count_vect.fit_transform(simplex_train)
simplex_train_tfidf = tfidf.fit_transform(simplex_train_count)

simplex_test_count = count_vect.transform(simplex_test) #use transform for all test inputs
simplex_test_tfidf = tfidf.transform(simplex_test_count)
```


Train the model below. Use accuracy_score to find the ~80% accuracy.

```nbmodel = MultinomialNB().fit(simplex_train_tfidf, y_train)
y_pred_nb = nbmodel.predict(simplex_test_tfidf)

#scoring
accuracy_score(y_test, y_pred_nb)
```


Similarly, predict whether a new article uses 2MASS by running the article's body text through CountVectorizer and tfidf. A prediction of 0 from the model means the article likely does not use 2MASS data.

```new_data_predictions = nbmodel.predict(new_data_text)```

#### ACKNOWLEDGEMENTS
Many thanks to the Datanauts program and its participants for all your support and camaraderie. This project was conducted on Iroquois land in Western Pennsylvania.
