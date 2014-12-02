import utils
import parse_movies
import config
import os

all_movies = list(parse_movies.load_all_movies(os.path.join(config.baseDir,"plot.list.gz")))

#==============================================
# 2a. PMF of P(Y)
#==============================================
pmf, data_year = utils.cal_pmf(all_movies)
n = len(data_year)
x = []
y = []
for year, amount in pmf.iteritems():
    x.append(year)
    y.append(float(amount)/float(n))
utils.histogram(x, y, 'Decade', 'PMF', 'PMF of P(Y)')
print 'PMF of P(Y) done'

#==============================================
# 2b. PMF of P(Y|X"radio">0)
#==============================================
pmf, data_year = utils.cal_pmf(all_movies, 'radio')
n = len(data_year)
x = []
y = []
for year, amount in pmf.iteritems():
    x.append(year)
    y.append(float(amount)/float(n))
utils.histogram(x, y, 'Decade', 'PMF', 'PMF of P(Y|X"radio">0)')
print 'PMF of P(Y|X"radio">0) done'

#==============================================
# 2c. PMF of P(Y|X"beaver">0)
#==============================================
pmf, data_year = utils.cal_pmf(all_movies, 'beaver')
n = len(data_year)
x = []
y = []
for year, amount in pmf.iteritems():
    x.append(year)
    y.append(float(amount)/float(n))
utils.histogram(x, y, 'Decade', 'PMF', 'PMF of P(Y|X"beaver">0)')
print 'PMF of PMF of P(Y|X"beaver">0) done'

#==============================================
# 2d. PMF of P(Y|X"the">0)
#==============================================
pmf, data_year = utils.cal_pmf(all_movies, 'the')
n = len(data_year)
x = []
y = []
for year, amount in pmf.iteritems():
    x.append(year)
    y.append(float(amount)/float(n))
utils.histogram(x, y, 'Decade', 'PMF', 'Blananced PMF of P(Y|X"the">0)')
print 'Blananced PMF of P(Y|X"the">0) done'

#sample the data to 6000 for each decade from 1930 to 2010
sampled_movies = utils.sample_data(all_movies, 6000, (1930, 2010))

#==============================================
# 2e. PMF of P(Y|X"radio">0)
#==============================================
pmf, data_year = utils.cal_pmf(sampled_movies, 'radio')
n = len(data_year)
x = []
y = []
for year, amount in pmf.iteritems():
    x.append(year)
    y.append(float(amount)/float(n))
utils.histogram(x, y, 'Decade', 'PMF', 'Blananced PMF of P(Y|X"radio">0)')
print 'Blananced PMF of P(Y|X"radio">0) done'

#==============================================
# 2f. PMF of P(Y|X"beaver">0)
#==============================================
pmf, data_year = utils.cal_pmf(sampled_movies, 'beaver')
n = len(data_year)
x = []
y = []
for year, amount in pmf.iteritems():
    x.append(year)
    y.append(float(amount)/float(n))
utils.histogram(x, y, 'Decade', 'PMF', 'Blananced PMF of P(Y|X"beaver">0)')
print 'Blananced PMF of PMF of P(Y|X"beaver">0) done'

#==============================================
# 2g. PMF of P(Y|X"the">0)
#==============================================
pmf, data_year = utils.cal_pmf(sampled_movies, 'the')
n = len(data_year)
x = []
y = []
for year, amount in pmf.iteritems():
    x.append(year)
    y.append(float(amount)/float(n))
utils.histogram(x, y, 'Decade', 'PMF', 'Blananced PMF of P(Y|X"the">0)')
print 'Blananced PMF of P(Y|X"the">0) done'
