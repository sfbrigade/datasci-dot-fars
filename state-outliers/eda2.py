import matplotlib.pyplot as plt
import seaborn as sns
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


class model(LinearRegression):
    def __init__(self,xtrain, ytrain, xtest, ytest):
        super(model,self).__init__()

        self.xtrain=xtrain
        self.ytrain=ytrain
        self.xtest=xtest
        self.ytest=ytest

        self.fit(self.xtrain, self.ytrain)
        print('train R2 = {:.2f}'.format(self.score(self.xtrain, self.ytrain)))
        print('test R2 = {:.2f}'.format(self.score(self.xtest, self.ytest)))


    # print('model coefficients: {}\nmodel intercept: {}'.format(model.coef_,model.intercept_))

def plot(m,ax,y_scenario):

    #xline=np.linspace(0,xtest.VMT.max().round(),10)

    ax.scatter(m.xtest,m.ytest,label='test_data',c='b',marker='o')
    ax.scatter(m.xtrain,m.ytrain,label='train data',c='g',marker='x')

    yline=m.predict(m.xtest)
    ax.plot(m.xtest,m.predict(m.xtest),label='regression',c='b')

    plt.text(.7,.1,'test R2={:.2f}\ntrain R2={:.2f}'.format(m.score(m.xtest,m.ytest),m.score(m.xtrain,m.ytrain)),transform=ax.transAxes,fontsize=12)
    plt.xlabel('Vehicle Miles Traveled',fontsize=17)
    plt.ylabel('Deaths',fontsize=17)
    plt.title(y_scenario,fontsize=20)
    plt.legend(loc=2,fontsize=15)
    plt.xticks(rotation=45)
    f.tight_layout(h_pad=5)



if __name__ == '__main__':

    y_scenarios = ['Total deaths', 'Deaths involving drivers under 16',
                   'Deaths involving drivers between 25 & 44',
                   'Multi-vehicle deaths',
                   'Bicyclist deaths']
    f=plt.figure(1,figsize=(12,7))
    for i,y_scenario in enumerate(y_scenarios):
        xtrain, ytrain, xtest, ytest = data(x=['VMT'], y=y_scenario)
        print('\n{}'.format(y_scenario))
        m=model(xtrain, ytrain, xtest, ytest)
        print(m.predict(xtest))
        ax=f.add_subplot(2,3,i+1)
        plot(m,ax,y_scenario)


    plt.show()
