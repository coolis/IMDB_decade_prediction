import utils
import math
from sys import maxint

def naive_bayes(data):
    likilihood = {}
    decades = {}
    for i in data:
        #calculate the prior
        if i['year'] in decades:
            decades[i['year']] += 1
        else:
            decades[i['year']] = 1

        #convert the data to bag of words representation
        X = utils.bags(i['summary'])
        if i['year'] not in likilihood:
            likilihood[i['year']] = {}
            for word in X:
                likilihood[i['year']][word] = {X[word]:1}
        else:
            for word in X:
                if word not in likilihood[i['year']]:
                    likilihood[i['year']][word] = {X[word]:1}
                else:
                    if X[word] in likilihood[i['year']][word]:
                        likilihood[i['year']][word][X[word]] += 1
                    else:
                        likilihood[i['year']][word][X[word]] = 1

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
            max_Y = year
        if y[year] < min_tmp:
            min_tmp = y[year]
            min_Y = year
    return min_Y, max_Y
