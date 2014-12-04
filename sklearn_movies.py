import config
import parse_movies
import utils
import numpy as np

import os

from sklearn.naive_bayes import MultinomialNB
#from sklearn.feature_extraction import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer

all_movies = list(parse_movies.load_all_movies(os.path.join(config.baseDir,config.data_file)))
#sample the data to 6000 for each decade from 1930 to 2010
sampled_movies = utils.sample_data(all_movies, 6000)

#split the data to train and test datasets
train_data = []
test_data = []
flip = True
for m in sampled_movies:
    if (flip):
        train_data.append(m)
        flip = False
    else:
        test_data.append(m)
        flip = True

#===============================================
#4a Use sklearn library to train the data
#for everyiterm in training data, find the bag of word, convert to feature vector, correspond to year
sumList = []
Y = []#data_target
for tmpMov in train_data:
    tmpS = unicode(tmpMov['summary'], errors = 'replace')
    sumList.append(tmpS)
    Y.append(tmpMov['year'])
#after X and Y, train -> fit a Naive Bayes model to the data
model = MultinomialNB()
vec = CountVectorizer()
X = vec.fit_transform(sumList)
model.fit(X, Y)
print 'Training finished'

# get the word list for each review
testSum = []
testY = []
for tmpMov in test_data:
    tmpS = unicode(tmpMov['summary'], errors = 'replace')
    testSum.append(tmpS)
    testY.append(tmpMov['year'])
# start testing
testX = vec.transform(testSum)
predY = model.predict(testX)

print np.mean(predY == testY)
