import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler,scale
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import regression
import seaborn as sns
df=pd.read_csv('deaths_vmt_bikers_state_year.csv')
'''[u'Unnamed: 0', u'state', u'year', u'state_abbv', u'TEMP_F',
       u'bike_deaths', u'vmt', u'Survey', u'Population', u'Commuters',
       u'Bicycle commuters']'''
print df.columns

g= df.groupby('year').agg({'bike_deaths':'sum','vmt':'sum'})
print g
plt.scatter(g.vmt,g.bike_deaths)
plt.show()


#df.drop(['year','Commuters','Unnamed: 0','state','state_abbv', 'TEMP_F','Survey','Bicycle commuters','Population'],axis=1,inplace=True)

dftest=df[df.year>=2015]
dftrain=df[df.year<2015]

#print model.score(x,y)
ytrain=dftrain.pop('bike_deaths')


ytest=dftest.pop('bike_deaths')


xtrain=dftrain[['vmt']]
xtest=dftest[['vmt']]

#
# xtrain,xtest,ytrain,ytest,=train_test_split(x,y,train_size=.5)

#scalerx=StandardScaler().fit(xtrain)

#scalery=StandardScaler().fit(ytrain)


model=RandomForestRegressor()

model.fit(xtrain,ytrain)


print model.score(xtest,ytest)

xpoints=np.matrix(range(0,400000,50000)).T
ypoints=model.predict(xpoints)





plt.figure(figsize=(25,15))
plt.scatter(xtrain,ytrain,label='Training',color='b')
plt.scatter(xtest,ytest,label='Testing',color='g')

plt.scatter(xpoints,ypoints,label='Fit',color='r')
plt.legend()

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