import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler,scale
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import regression
import seaborn as sns
df=pd.read_csv('state-outliers/data.csv')
#deaths_vmt_bikers_state_year.csv')
'''[u'Unnamed: 0', u'state', u'year', u'state_abbv', u'TEMP_F',
       u'bike_deaths', u'vmt', u'Survey', u'Population', u'Commuters',
       u'Bicycle commuters']
   Index([u'Year', u'State', u'Population', u'Commuters', u'Bicycle commuters',
       u'VMT', u'No. deaths', u'Deaths per B miles'],
      dtype='object')
       '''

print df.columns


dftest=df[df.Year>=2015]
dftrain=df[df.Year<2015]

#print model.score(x,y)
ytrain=dftrain.pop('No. deaths')


ytest=dftest.pop('No. deaths')


xtrain=dftrain[['VMT']]
xtest=dftest[['VMT']]

#
# xtrain,xtest,ytrain,ytest,=train_test_split(x,y,train_size=.5)

#scalerx=StandardScaler().fit(xtrain)

#scalery=StandardScaler().fit(ytrain)

xtrain=sm.add_constant(xtrain)
model=sm.OLS(ytrain,xtrain,hasconst=True)
results=model.fit()


print results.summary()
r2_train= model.score(xtrain,ytrain)
r2_test= model.score(xtest,ytest)

xpoints=np.matrix(range(0,400000,50000)).T
ypoints=model.predict(xpoints)




plt.figure(figsize=(25,15))
plt.scatter(xtrain,ytrain,label='Training R2={:.2f}'.format(r2_train),color='b')
plt.scatter(xtest,ytest,label='Testing R2={:.2f}'.format(r2_test),color='g')

plt.plot(xpoints,ypoints,label='Fit',color='r',)
plt.legend(fontsize=24)
plt.ylabel('bike deaths',fontsize=16)
plt.xlabel('vehicle miles traveled (M)',fontsize=16)
plt.title('Bike Deaths vs Vehicle Miles Traveled ',fontsize=26)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.show()


exit()





mask=df['year']==2010
plt.figure(figsize=(25,12))
for j,i in enumerate(xrange(2010,2016)):
    mask=df['year']==i
    colors=['red','blue','green','orange','purple','brown']
    markers=['o','x','s','p','h','^']
    plt.scatter(x[mask],y[mask],label=i,color=colors[j],marker=markers[j])

plt.scatter(xpoints,ypred,linewidths=1, label='predictor')
plt.legend()

plt.show()


# plt.scatter(x,y,)
# plt.show()
#
# mean=np.mean(y)
# var1= sum((y-ypred)**2)
# vart =sum((y-mean)**2)
#
# plt.plot(y)
# plt.plot(ypred)
# plt.show()