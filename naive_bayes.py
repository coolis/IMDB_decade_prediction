import config
import parse_movies
import utils

import os
import math
from sys import maxint

def naive_bayes(data):
    likilihood = {}
    decades = {}
    for i in data:
        if i['year'] in decades:
            decades[i['year']] += 1
        else:
            decades[i['year']] = 1
        X = utils.bags(i['summary'])
        if i['year'] in likilihood:
            for word in X:
                if word in likilihood[i['year']]:
                    if X[word] in likilihood[i['year']][word]:
                        likilihood[i['year']][word][X[word]] += 1
                    else:
                        likilihood[i['year']][word][X[word]] = 1
                else:
                    likilihood[i['year']][word] = {X[word]:1}
        else:
            likilihood[i['year']] = {}
            for word in X:
                likilihood[i['year']][word] = {X[word]:1}

    for l in likilihood:
        for word in likilihood[l]:
            for occurence in likilihood[l][word]:
                likilihood[l][word][occurence] /= float(decades[l])
        decades[l] /= float(len(data))

    return likilihood, decades

def predict(lh, prior, x):
    y = {}
    for l in lh:
        p = 0
        for word in x:
            if word in lh[l] and x[word] in lh[l][word]:
                p += math.log(lh[l][word][x[word]])
            else:
                p += math.log(0.0001)
        y[l] = p + math.log(prior[l])

    return y

def findMinMaxY(y):
    max_Y = 0
    min_Y = 0
    max_tmp = -maxint-2
    min_tmp = maxint
    for year in y:
        if y[year] > max_tmp:
            max_tmp = y[year]
            max_year = year
        if y[year] < min_tmp:
            min_tmp = y[year]
            min_year = year
    return min_year, max_year

all_movies = list(parse_movies.load_all_movies(os.path.join(config.baseDir,"plot.list.gz")))
#sample the data to 6000 for each decade from 1930 to 2010
sampled_movies = utils.sample_data(all_movies, 6000, (1930, 2010))

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
train_lh, train_prior = naive_bayes(train_data)

#test the data
for d in all_movies:
    if d['title'] == 'Finding Nemo' or d['title'] == 'The Matrix' or d['title'] == 'Gone with the Wind' or d['title'] == 'Harry Potter and the Goblet of Fire' or d['title'] == 'Avatar':
        predicted_y = predict(train_lh, train_prior, utils.bags(d['summary']))
        minY, maxY = findMinMaxY(predicted_y)
        x = []
        y = []
        for year in predicted_y:
            x.append(year)
            y.append(predicted_y[year]+abs(predicted_y[minY]))
        utils.histogram(x, y, 'Decade', 'Posterior Probability', d['title']+' ('+str(d['year'])+') Histogram of Posterior Probability for each decade')
        print d['title']+' is done.', 'Predicted decade '+str(maxY), 'Real decade '+str(d['year'])
