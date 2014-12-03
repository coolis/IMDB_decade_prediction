import config

import os
import string
import random
import matplotlib.pyplot as plt

def histogram(x, y, xlabel, ylabel, title):
    fig = plt.figure()
    plt.bar(x, y, width=10, linewidth=1)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    fig.savefig(os.path.join(config.baseDir, 'Figures/'+title+'.png'))

def line(x, y, xlabel, ylabel, title):
    fig = plt.figure()
    plt.plot(x,y)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    fig.savefig(os.path.join(config.baseDir, 'Figures/'+title+'.png'))

def spectrom(X, xlabel, ylabel, title):
    fig = plt.figure()
    cax = plt.matshow(X, fignum=False)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.colorbar(cax, orientation='horizontal')
    fig.savefig(os.path.join(config.baseDir, 'Figures/'+title+'.png'))

def sample_data(data, bin_size):
    cated_data = {1930:[],1940:[],1950:[],1960:[],1970:[],1980:[],1990:[],2000:[],2010:[]}
    sampled_data = []
    for d in data:
        cated_data[d['year']].append(d)

    for year in cated_data:
        sampled_data += random.sample(cated_data[year], bin_size)

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
