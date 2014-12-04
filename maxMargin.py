# -*- coding: utf-8 -*-
import config
import parse_movies
import utils
import numpy as np

import os

from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing
from sklearn import linear_model
from sklearn import svm
from sklearn import neighbors
from sklearn import tree

import matplotlib.pyplot as plt

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

#train the data
#for everyiterm in training data, find the bag of word, convert to feature vector, correspond to year
print('start traning data!')
sumList = []
Y = []
for tmpMov in train_data:
    tmpS = unicode(tmpMov['summary'], errors = 'replace')
    sumList.append(tmpS)
    Y.append(tmpMov['year'])

# get the word list for each review
testSum = []
testY = []
for tmpMov in test_data:
    tmpS = unicode(tmpMov['summary'], errors = 'replace')
    testSum.append(tmpS)
    testY.append(tmpMov['year'])

# 5 a
vec = HashingVectorizer(decode_error='replace', n_features=600)
X = vec.fit_transform(sumList).toarray()
testX = vec.fit_transform(testSum).toarray()

# 5 b
# get new
scalar = preprocessing.StandardScaler().fit(X)
trainX = scalar.transform(X)
testX_hashed = scalar.transform(testX)

# 5 c
#train with all the models
model = MultinomialNB()
model.fit(trainX, Y)
#Accuracy measurement
# compute accuracy
predY = model.predict(testX_hashed)
print 'The accuracy of the MultinomialNB on test data is ', np.mean(predY == testY)

# linear_model.SGDClassifier uing newX and Y
model = linear_model.SGDClassifier()
model.fit(trainX, Y)
#Accuracy measurement
# compute accuracy
predY = model.predict(testX_hashed)
print 'The accuracy of the SGDClassifier on test data is ', np.mean(predY == testY)



# svm.LinearSVC, uing newX and Y
model = svm.LinearSVC(dual=False)
model.fit(trainX, Y)
#Accuracy measurement
# compute accuracy
predY = model.predict(testX_hashed)
print 'The accuracy of the LinearSVC on test data is ', np.mean(predY == testY)



# svm.SVC(kernel=’rbf’), uing newX and Y
model = svm.SVC(kernel='rbf')
model.fit(trainX, Y)
#Accuracy measurement
predY = model.predict(testX_hashed)
print 'The accuracy of the SVC(kernel="rbf") on test data is ', np.mean(predY == testY)


# linear_model.Perceptron(penalty=’l1’), uing newX and Y
model = linear_model.Perceptron(penalty='l1')
model.fit(trainX, Y)
#Accuracy measurement
predY = model.predict(testX_hashed)
print 'The accuracy of the Perceptron(penalty="l1") on test data is ', np.mean(predY == testY)



# linear_model.Perceptron(penalty=’l2’,n_iter=25), uing newX and Y
model = linear_model.Perceptron(penalty='l2',n_iter=25)
model.fit(trainX, Y)
#Accuracy measurement
predY = model.predict(testX_hashed)
print 'The accuracy of the Perceptron(penalty="l2",n_iter=25) on test data is ', np.mean(predY == testY)



# sklearn.neighbors.KNeighborsClassifier, uing newX and Y
model = neighbors.KNeighborsClassifier()
model.fit(trainX, Y)
#Accuracy measurement
predY = model.predict(testX_hashed)
print 'The accuracy of the KNeighborsClassifier on test data is ', np.mean(predY == testY)

model = tree.DecisionTreeClassifier()
model.fit(trainX, Y)
#Accuracy measurement
predY = model.predict(testX_hashed)
print 'The accuracy of the DecisionTreeClassifier on test data is ', np.mean(predY == testY)

# 5 f
plot_X = []
plot_Y = []
model = svm.LinearSVC(dual=False)
for k in range(1,11):
    feature_space = k * 300
    vec = HashingVectorizer(non_negative=True, n_features=feature_space)
    trainX = vec.transform(sumList).toarray()
    testX = vec.transform(testSum).toarray()
    scalar = preprocessing.StandardScaler().fit(trainX)
    trainX_scaled = scalar.transform(trainX)
    testX_scaled = scalar.transform(testX)
    model.fit(trainX_scaled, Y)
    predY = model.predict(testX_scaled)
    accuracy = np.mean(predY == testY)
    plot_X.append(feature_space)
    plot_Y.append(accuracy)
    print accuracy

fig = plt.figure()
plt.scatter(plot_X, plot_Y, c='r')
plt.title('Dimensionality Reduction Comparision')
plt.ylabel('Feature Space')
plt.xlabel('Accuarcy')
fig.savefig(os.path.join(config.baseDir, 'Figures/Dimensionality Reduction Comparision.png'))
