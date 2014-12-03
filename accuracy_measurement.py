import config
import parse_movies
import naive_bayes
import utils
import numpy as np

import os
import operator

#test the data
def findMovie(data, sample):
    result = []
    for d in data:
        for s in sample:
            if d['title'] == s:
                result.append(d)
    return result

def probability_distribution(data):
    probability = {}

    for m in data:
        if m['year'] not in probability:
            probability[m['year']] = 1
        else:
            probability[m['year']] += 1

    for p in probability:
        probability[p] /= float(len(data))

    return probability

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

#=====================================
# 2j. plot and predict the movies
#
movies = ['Finding Nemo', 'The Matrix', 'Gone with the Wind', 'Harry Potter and the Goblet of Fire', 'Avatar']
test_movies = findMovie(all_movies, movies)
for tm in test_movies:
    predicted_y = naive_bayes.predict(train_lh, train_prior, utils.bags(tm['summary']))
    minY, maxY = naive_bayes.findMinMaxY(predicted_y)
    x = []
    y = []
    for year in predicted_y:
        x.append(year)
        y.append(predicted_y[year]+abs(predicted_y[minY]))
    utils.histogram(x, y, 'Decade', 'Posterior Probability', tm['title']+' ('+str(tm['year'])+') Histogram of Posterior Probability for each decade')
    print tm['title']+' is done.', 'Predicted decade '+str(maxY), 'Real decade '+str(tm['year'])

#======================================
# 2k. Accuracy measurement
#
accuracy = 0
for d in test_data:
    predicted_y = naive_bayes.predict(train_lh, train_prior, utils.bags(d['summary']))
    minY, maxY = naive_bayes.findMinMaxY(predicted_y)
    if maxY == d['year']:
        accuracy += 1

accuracy /= float(len(test_data))
print 'The accuracy of the model on test data is ', accuracy

#==============================================
# 2l. plot cmc
#
cmc = []
for k in range(1,10):
    accuracy = 0
    for d in test_data:
        predicted_y = naive_bayes.predict(train_lh, train_prior, utils.bags(d['summary']))
        sorted_y = sorted(predicted_y.items(), key=operator.itemgetter(1), reverse=True)
        for i in range(k):
            if sorted_y[i][0] == d['year']:
                accuracy += 1
                break
    cmc.append(accuracy/float(len(test_data)))
print 'The CMC is ', cmc
utils.line([1,2,3,4,5,6,7,8,9], cmc, 'K', 'Accuracy', 'Cumulative Match Curve')

#==============================================
# 2m. Plot confusion matrix
#
cmatrix = np.zeros(shape=(9,9))
for d in test_data:
    predicted_y = naive_bayes.predict(train_lh, train_prior, utils.bags(d['summary']))
    sorted_y = sorted(predicted_y.items(), key=operator.itemgetter(1), reverse=True)
    predicted_year = sorted_y[0][0]
    cmatrix[(d['year']-1930)/10][(predicted_year-1930)/10] += 1

utils.spectrom(cmatrix, 'Decade', 'Decade', 'Confusion Matrix')
