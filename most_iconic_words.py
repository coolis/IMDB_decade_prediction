import config
import parse_movies
import naive_bayes
import utils

from sys import maxint
import os
import operator
import math

def predict(lh, prior, x, exclusive):
    y = {}
    for l in lh:
        p = 0
        for word in x:
            if word in exclusive[l][:100]:
                p += math.log(0.0001)
            elif word in lh[l] and x[word] in lh[l][word]:
                p += math.log(lh[l][word][x[word]])
            else:
                p += math.log(0.0001)
        y[l] = p + math.log(prior[l])

    return y

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
train_lh, train_prior = naive_bayes.naive_bayes(train_data)

#================================================
# 3a. 10 most informative words
#
informative = {}
for year in train_lh:
    informative[year] = {}
    for word in train_lh[year]:
        p = 0
        for probability in train_lh[year][word]:
            p += train_lh[year][word][probability]
        informative[year][word] = p

for year in informative:
    for word in informative[year]:
        smallest = maxint
        for other in informative:
            if other != year and word in informative[other] and informative[other][word] < smallest:
                smallest = informative[other][word]
        if smallest == maxint:
            smallest = 0.0001
        informative[year][word] /= float(smallest)

for year in informative:
    sorted_informative = sorted(informative[year].items(), key=operator.itemgetter(1), reverse=True)
    print year, sorted_informative[:10]
    informative[year] = sorted(informative[year], key=informative[year].get, reverse=True)

#========================================
# 3b. Performance degrade
#

#accuracy with all the words
accuracy = 0
for d in test_data:
    predicted_y = naive_bayes.predict(train_lh, train_prior, utils.bags(d['summary']))
    minY, maxY = naive_bayes.findMinMaxY(predicted_y)
    if maxY == d['year']:
        accuracy += 1

accuracy /= float(len(test_data))
print 'The accuracy of the model on test data is ', accuracy

#accuracy with all the words excluding top 100 informative words
e_accuracy = 0
for d in test_data:
    predicted_y = predict(train_lh, train_prior, utils.bags(d['summary']), informative)
    minY, maxY = naive_bayes.findMinMaxY(predicted_y)
    if maxY == d['year']:
        e_accuracy += 1

e_accuracy /= float(len(test_data))
print 'The accuracy of the model on test data excluding all top 100 informative words is ', e_accuracy
