import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression


'''Index(['YEAR', 'STATE', 'Postal code', 'VMT', 'VMT (B)', 'YEAR_STATE',
       'Total deaths', 'Deaths per BVMT', 'Deaths involving drivers under 16',
       'Deaths involving drivers under 16 per BVMT',
       'Deaths involving drivers between 25 & 44',
       'Deaths involving drivers between 25 & 44 per BVMT',
       'Multi-vehicle deaths', 'Multi-vehicle deaths per BVMT',
       'Bicyclist deaths', 'Bicyclist deaths per BVMT'],
      dtype='object')'''


def data(x=None, y=None):
    df = pd.read_csv('data-2.csv')

    dftest = df[df.YEAR >= 2015]
    dftrain = df[df.YEAR < 2015]

    # print model.score(x,y)

    ytrain = dftrain.pop("" + y + "")

    ytest = dftest.pop("" + y + "")

    xtrain = dftrain[x]
    xtest = dftest[x]

    return xtrain, ytrain, xtest, ytest


def model(xtrain, ytrain, xtest, ytest):
    model = LinearRegression()
    model.fit(xtrain, ytrain)

    print('train R2 = {:.2f}'.format(model.score(xtrain, ytrain)))
    print('test R2 = {:.2f}'.format(model.score(xtest, ytest)))

    # print('model coefficients: {}\nmodel intercept: {}'.format(model.coef_,model.intercept_))


if __name__ == '__main__':

    y_scenarios = ['Total deaths', 'Deaths involving drivers under 16',
                   'Deaths involving drivers between 25 & 44',
                   'Multi-vehicle deaths',
                   'Bicyclist deaths']

    for y_scenario in y_scenarios:
        xtrain, ytrain, xtest, ytest = data(x=['VMT'], y=y_scenario)
        print('\n{}'.format(y_scenario))
        model(xtrain, ytrain, xtest, ytest)

