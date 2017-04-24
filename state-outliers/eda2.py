import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from statsmodels.api import OLS

'''Index(['YEAR', 'STATE', 'Postal code', 'VMT', 'VMT (B)', 'YEAR_STATE',
       'Total deaths', 'Deaths per BVMT', 'Deaths involving drivers under 16',
       'Deaths involving drivers under 16 per BVMT',
       'Deaths involving drivers between 25 & 44',
       'Deaths involving drivers between 25 & 44 per BVMT',
       'Multi-vehicle deaths', 'Multi-vehicle deaths per BVMT',
       'Bicyclist deaths', 'Bicyclist deaths per BVMT'],
      dtype='object')'''


def model_data(x=None, y=None, state=False, excludebig=False, exclude0=True):
    df = pd.read_csv('data-2.csv')
    if excludebig:
        mask = (df['Postal code'].apply(lambda x: x not in ['CA', 'FL', 'TX']))
        df = df[mask]
    if exclude0:
        mask = df[y] != 0
        df = df[mask]

    dftest = df[df.YEAR >= 2015]
    dftrain = df[df.YEAR < 2015]
    # print model.score(x,y)

    ytrain = dftrain.pop("" + y + "")

    ytest = dftest.pop("" + y + "")

    xtrain = dftrain[x]
    xtest = dftest[x]

    ystrain = dftrain['YEAR'].astype(str) + '-' + dftrain['Postal code']
    ystest = dftest['YEAR'].astype(str) + '-' + dftest['Postal code']

    return xtrain, ytrain, xtest, ytest, ystrain, ystest


class model(LinearRegression):
    def __init__(self, xtrain, ytrain, xtest, ytest):
        super(model, self).__init__()

        self.xtrain = xtrain
        self.ytrain = ytrain
        self.xtest = xtest
        self.ytest = ytest

        self.fit(self.xtrain, self.ytrain)
        print('train R2 = {:.2f}'.format(self.score(self.xtrain, self.ytrain)))
        print('test R2 = {:.2f}'.format(self.score(self.xtest, self.ytest)))


        # print('model coefficients: {}\nmodel intercept: {}'.format(model.coef_,model.intercept_))


class model2(OLS):
    def __init__(self, xtrain, ytrain, xtest, ytest):
        # xtrain=add_constant(xtrain)
        print(xtrain)

        super(model2, self).__init__(ytrain, xtrain, hasconst=False)

        self.xtrain = xtrain
        self.ytrain = ytrain
        self.xtest = xtest
        self.ytest = ytest

        results = self.fit()

        print(results.summary())


def plot(m, ax, y_scenario, ystrain=None, ystest=None):
    # xline=np.linspace(0,xtest.VMT.max().round(),10)

    ax.scatter(m.xtest, m.ytest, label='test_data', c='b', marker='o')
    ax.scatter(m.xtrain, m.ytrain, label='train data', c='g', marker='x')

    yline = m.predict(m.xtest)
    ax.plot(m.xtest, m.predict(m.xtest), label='regression', c='b')

    plt.text(.7, .1, 'test R2={:.2f}\ntrain R2={:.2f}'.format(m.score(m.xtest, m.ytest), m.score(m.xtrain, m.ytrain)),
             transform=ax.transAxes, fontsize=12)
    plt.xlabel('Vehicle Miles Traveled', fontsize=17)
    plt.ylabel('Deaths', fontsize=17)
    plt.title('{}\n{:.0f} deaths per MVMT'.format(y_scenario, m.coef_[0] * 1e+6), fontsize=20)
    plt.legend(loc=2, fontsize=15)
    plt.xticks(rotation=45)
    plt.tight_layout(h_pad=5)
    # ystest.reset_index()
    # m.xtest.reset_index()
    # m.ytest.reset_index()
    if ystest.any():
        for i in range(len(m.xtest)):
            # print(m.xtest.loc[i][0],m.xtest.loc[i].any()>2)

            # plt.annotate(ystest.index[i],xy=(m.xtest.index[i],m.ytest.index[i]))
            plt.annotate(ystest.iloc[i], xy=(m.xtest.iloc[i], m.ytest.iloc[i]))


def plot_scenarios():
    y_scenarios = ['Total deaths', 'Deaths involving drivers under 16',
                   'Deaths involving drivers between 25 & 44',
                   'Bicyclist deaths']

    f = plt.figure(1, figsize=(20, 12))
    for i, y_scenario in enumerate(y_scenarios):
        xtrain, ytrain, xtest, ytest, ystrain, ystest = model_data(x=['VMT'], y=y_scenario)

        print('\n{}'.format(y_scenario))
        m = model(xtrain, ytrain, xtest, ytest)
        print(m.predict(xtest))
        ax = f.add_subplot(2, 2, i + 1)
        plot(m, ax, y_scenario, ystrain, ystest)

    plt.show()


if __name__ == '__main__':
    df = pd.read_csv('data-2.csv')

    plot_scenarios()
