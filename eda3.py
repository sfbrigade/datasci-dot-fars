import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor,RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import ridge_regression
from sklearn.metrics import r2_score
'''Index([u'STATE', u'YEAR', u'MONTH', u'ST_CASE', u'TEMP_F', u'Name',
       u'Postal Code', u'FIPS', u'Census region'],
      dtype='object')
Index([u'state', u'vmt', u'year', u'month', u'file'], dtype='object')
'''
df=pd.read_csv('bicycle_deaths_with_temps.csv')

df['age']=df['AGE'].apply(lambda x: x if x<200 else np.nan)


df['sex']=df['SEX'].apply(lambda x: 'M' if x==1 else 'F' if x==2 else 'U')
df['alcohol']=df['DRINKING'].apply(lambda x: 'N' if x==0 else 'Y' if x==1 else 'U')
df['drugs']=df['DRUGS'].apply(lambda x: 'N' if x==0 else 'Y' if x==1 else 'U')
#df['race']=df['RACE'].apply(lambda x: 'N' if 0 else 'Y' if 1 else 'U')

df['temp']=df['TEMP_F'].apply(lambda x: np.nan if x==-9999 else x)


st=pd.read_csv('US State Abbreviations.csv')
vmt=pd.read_csv('vmt.csv')
df_st=pd.merge(df,st,left_on='STATE',right_on='FIPS')
df_st_vmt=pd.merge(df_st,vmt,left_on=['Name','YEAR','MONTH'],right_on=['state','year','month'],how='inner')
pop_data=pd.read_csv('./bicycle_commuters_by_state.csv')
pop_data=pop_data[pop_data.Survey=='ACS5']

df_st_vmt_pop=pd.merge(df_st_vmt,pop_data,left_on=['Postal Code','YEAR'], right_on=['Geography','Year'])
data=df_st_vmt_pop
data['season']=np.where(data['month'].isin([11,12,1,2]),'win',np.where(data['month'].isin([3,4,5]),'spr',np.where(data['month'].isin([7,8,9]),'sum','fal')))

# data['temp_buckets']=pd.cut(data['TEMP_F'],bins=[-10,32,50,70,85,95,107])
#
# data['vmt_buckets']=pd.qcut(data['vmt'],q=16)
# data['age_buckets']=pd.qcut(data['age'],6)
# data['bikers_buckets']=pd.qcut(data['Bicycle commuters'],6)
#data['commuter_buckets']=pd.qcut(data['Commuters'],6)
#data.drop(['STATE','Name','FIPS','MONTH','state','file','month','TEMP_F','Postal Code'],axis=1,inplace=True)
data['count']=data['ST_CASE']

data['yr_month']=data['year'].apply(lambda x: '{}'.format(x)) + '-' +data['month'].apply(lambda x: '{:02d}'.format(x))
season_dummy=pd.get_dummies(data['season'],drop_first=True)
sex_dummy=pd.get_dummies(data['sex'],drop_first=True,prefix='sex')
alc_dummy=pd.get_dummies(data['alcohol'],drop_first=True,prefix='alc')
data= pd.concat([data,season_dummy,sex_dummy,alc_dummy],axis=1)







get=['temp','vmt','Bicycle commuters','spr','sum','win','count','age','sex_M','sex_U','alc_U','alc_Y','year','month']

data2=data[get]






data2= data2.apply(pd.Series.interpolate)
data2['month2']=(data2['month']-6)**2



data_train=data2[data2['year']<2015]


data_test=data2[data2['year']==2015]

groups=['month2']
aggs={'vmt':'mean','Bicycle commuters':'mean','count':'count'} #,'age':'mean','count':'count'}



data_train_agg=pd.DataFrame(data_train.groupby(groups).agg(aggs)).reset_index()
data_test_agg=pd.DataFrame(data_test.groupby(groups).agg(aggs)).reset_index()

data_train_scale=data_train_agg

data_test_scale=data_test_agg


y_train=data_train_agg.pop('count')
y_test=data_test_agg.pop('count')


from sklearn.metrics import accuracy_score
model=LinearRegression(normalize=True)
model.fit(data_train_scale,y_train)


ytrain_pred=model.predict(data_train_scale)

ytest_pred=model.predict(data_test_scale)



print model.score(data_train_scale,y_train)
print r2_score(y_test,ytest_pred)

mean=np.mean(y_test)


print (y_test-ytest_pred)**2,(y_test-mean)**2

plt.scatter(ytrain_pred,y_train)
plt.show()
plt.scatter(ytest_pred,y_test)
plt.show()
exit()

import statsmodels.api as sm

# Fit and summarize OLS model
print data_train_scale
mod = sm.OLS(y_train,data_train_scale)
res = mod.fit_regularized()
print res.summary()
#

# print accuracy_score(y_test,ypred)

# import seaborn as sns
# sns.pairplot(pd.DataFrame(data_train.groupby(groups).agg(aggs)).reset_index())
#
# plt.show()
# exit()





aggs={'count':'count','vmt':'sum','Bicycle commuters':'mean'} #,'temp':'mean'}
vars=pd.DataFrame(data.groupby(groups).agg(aggs)).reset_index()




#vars['month2']=vars['month']#-(data['month']-7)**2



import seaborn as sns
vars.fillna(0,inplace=True)
plt.rcParams['figure.figsize']=(30,20)

sns.pairplot(vars[['season','vmt','Bicycle commuters','count']],kind='reg')

plt.show()

break_year=2015

vars_train=vars[vars['year']<break_year]
vars_test=vars[vars['year']>=break_year]
ytrain=vars_train['count']



inputs=['vmt','Bicycle commuters','month2']

xtrain=vars_train[inputs]

ytest=vars_test['count']
xtest=vars_test[inputs]

scale=False
if scale:
    s=StandardScaler()

    xtrain=s.fit_transform(xtrain)
    ytrain=s.fit_transform(ytrain)


    xtest=s.fit_transform(xtest)
    ytest=s.fit_transform(ytest)

import statsmodels.api as sm

# Fit and summarize OLS model
mod = sm.OLS(ytrain, xtrain)
res = mod.fit()
print res.summary()
#model=RandomForestRegressor()

from sklearn.linear_model import Ridge
model=Ridge()
model=LinearRegression()
model.fit(xtrain,ytrain)

print model.coef_
print model.score(xtrain,ytrain)
print model.score(xtest,ytest)


vars_train['ypred']=model.predict(xtrain)
vars_test['ypred']=model.predict(xtest)

plot_train=vars_train[['yr_month','count','ypred']]


plot_test=vars_test[['yr_month','count','ypred']]

f=plt.figure(1,figsize=(30,20))
plt.title('Bike deaths by month',fontsize=30)
plt.plot(range(1,len(plot_train)+1),plot_train['count'],label='ytrain',c='g',marker='o')
plt.plot(range(1,len(plot_train)+1),plot_train['ypred'],label='ytrain_predict',c='g',marker=None,ls='--')

plt.plot(range(len(plot_train)+1,len(plot_train)+1+len(plot_test)),plot_test['count'],label='ytest',c='r')
plt.plot(range(len(plot_train)+1,len(plot_train)+1+len(plot_test)),plot_test['ypred'],label='ytest_predict',c='r'
         , ls='--')

plt.xticks(range(0,len(vars)),vars['yr_month'],rotation=70,fontsize=15)
plt.ylabel('bike deaths',fontsize=20)
plt.yticks(fontsize=20)
plt.xlabel('month',fontsize=20)
plt.legend(fontsize=20,loc=0)
plt.grid(b=True)
plt.show()


# temps= pd.get_dummies(data.temp_buckets)
#
#
# print data