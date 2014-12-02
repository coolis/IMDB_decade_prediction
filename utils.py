import config

import os
import re
import string
import matplotlib.pyplot as plt

def cal_pmf(data, condition=None):
    pmf = {}
    data_year = []
    for i in data:
        for word in bags(i['summary']):
            if condition == None or word == condition:
                data_year.append(i['year'])
                if (i['year'] in pmf):
                    pmf[i['year']] += 1
                else:
                    pmf[i['year']] = 1

    return pmf, data_year

def histogram(x, y, xlabel, ylabel, title):
    fig = plt.figure()
    plt.bar(x, y, width=10, linewidth=1)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    fig.savefig(os.path.join(config.baseDir, 'Figures/'+title+'.png'))

def sample_data(data, bin_size, range=None):
    sampled_data = []
    counter = {}
    for d in data:
        if (d['year'] < range[0] or d['year'] > range[1]):
            continue
        if d['year'] in counter:
            counter[d['year']] += 1
            if counter[d['year']] <= bin_size:
                sampled_data.append(d)
        else:
            counter[d['year']] = 1
            if counter[d['year']] <= bin_size:
                sampled_data.append(d)
    return sampled_data

def bags(data):
    bag_of_words = {}
    words = data.translate(string.maketrans(string.punctuation, ' '*len(string.punctuation))).split(' ')
    for w in words:
        if w in bag_of_words:
            bag_of_words[w] += 1
        else:
            bag_of_words[w] = 1
    return bag_of_words
