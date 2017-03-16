
from tsa import test_stationarity
import pandas as pd
from pandas.tools.plotting import lag_plot,autocorrelation_plot

import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler,scale
import seaborn as sns
from datetime import datetime,date
from sklearn.metrics import r2_score
from statsmodels.tsa.ar_model import AR
from sklearn.metrics import mean_squared_error

'''Index([u'STATE', u'YEAR', u'MONTH', u'ST_CASE', u'TEMP_F', u'Name',
       u'Postal Code', u'FIPS', u'Census region'],
      dtype='object')
Index([u'state', u'vmt', u'year', u'month', u'file'], dtype='object')
'''

def scale_df(df,columns=None):

    for i in df[columns]:
        if i:
            df[i]=df[i].apply(lambda x: x*1./max(df[i]))

    return df




def data():

    df=pd.read_csv('bicycle_deaths_with_temps.csv')

    '''remove -9999'''
    df['TEMP_F']=df['TEMP_F'].apply(lambda x: np.nan if x==-9999 else x)

    """"""
    dfm=df.groupby(['STATE','YEAR','MONTH']).agg({'TEMP_F':'mean','ST_CASE':'count'})

    dfm.reset_index(inplace=True)

    st=pd.read_csv('US State Abbreviations.csv')
    vmt=pd.read_csv('vmt.csv')

    dfm_st=pd.merge(dfm,st,left_on='STATE',right_on='FIPS')

    print dfm_st.head()

    exit()

    dfm_st_vmt=pd.merge(dfm_st,vmt,left_on=['Name','YEAR','MONTH'],right_on=['state','year','month'],how='inner')
    pop_data=pd.read_csv('./bicycle_commuters_by_state.csv')
    pop_data=pop_data[pop_data.Survey=='ACS5'][pop_data.Geography!='US'].groupby('Year')['Population'].sum()





    df_st_vmt_pop=pd.merge(dfm_st_vmt,pop_data,how='left',left_on=['Postal Code','YEAR'], right_on=['Geography','Year'])

    print df_st_vmt_pop.groupby('Year')['Population'].sum()

    df_filt=df_st_vmt_pop[['Population','Commuters','Bicycle commuters','ST_CASE','TEMP_F','vmt','Postal Code','year','month','Census region']]
    df_filt.rename(columns={'Bicycle commuters': 'bikers', 'Population': 'population', 'Commuters': 'commuters', 'TEMP_F': 'temp','Postal Code': 'state', 'ST_CASE': 'deaths', 'Census region': 'region'}, inplace=True)

    dg = df_filt.groupby(['year', 'month']).agg(
        {'population': 'mean', 'commuters': 'mean', 'bikers': 'mean', 'temp': 'mean', 'vmt': 'sum',
         'deaths': 'sum'}).reset_index()
    dg['day']=1

    dg['date']=pd.to_datetime(dg[['year','month','day']])

    dg=dg.set_index(['date'])

    return dg


class linear_model(object):

    def fit(self,x=None,y=None):

        print x.shape,y.shape

        self.model= LinearRegression()
        self.model.fit(x,y)
        return self.model

    def predict(self,x=None):

        return self.model.predict(x)

    def score(self,x,y):

        self.model.score(x,y)

def run_regression():
    dg=data()
    regions=['Midwest', 'Northeast' ,'South', 'West']

    fig,ax=plt.subplots(4,2)
    fig.set_size_inches(30, 20, forward=True)


    #ax=ax.T

    for region,splot in zip(regions,ax):



        dfiltered=dg[dg['region']==region]

        dtrain=dfiltered[dfiltered['year']<2015]
        dtest=dfiltered[dfiltered['year']==2015]

        xtrain=dtrain['vmt']
        dates_train=dtrain['date']
        ytrain=dtrain['deaths']
        xtest=dtest['vmt']
        dates_test=dtest['date']
        ytest=dtest['deaths']

        model=linear_model()
        model.fit(xtrain,ytrain)

        ytrain_predict=model.predict(xtrain)
        ytest_predict=model.predict(xtest)



        splot[0].plot(dates_train,ytrain_predict,label='Prediction')
        splot[0].plot(dates_train,ytrain,label='Actual')



        plt.setp(splot[0].xaxis.get_majorticklabels(), rotation=45)
        #splot[1].hist(ypredict-dfiltered['deaths'], label='Residual Error')


        splot[1].plot(dates_test,ytest_predict,label='Prediction')
        splot[1].plot(dates_test,ytest,label='Actual')

        splot[1].set_title('{} Regression Testing R2= {}'.format(region,r2_score(ytest,ytest_predict)))
        plt.setp(splot[1].xaxis.get_majorticklabels(), rotation=45)
        #splot[1].hist(ypredict-dfiltered['deaths'], label='Residual Error')

    splot[0].legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)

    splot[1].legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)


    # plt.xticks(rotation=45)
    # plt.title(region)
    # plt.legend()
    plt.show()

def run_regression1():
    dg=data()

    # dg['deaths']=dg['deaths'].shift(12)
    # dg['vmt']=dg['vmt'].shift(12)
    dg.dropna(inplace=True)
    xs=['temp','commuters','vmt','bikers','population']


    for i in xs:
        plt.plot(dg[i],label=i)
    plt.legend()
    plt.show()
    exit()

    split_year=2015
    dtrain=dg[dg['year']<split_year]
    dtest=dg[dg['year']>=split_year]






    xtrain=dtrain[xs]
    ytrain=dtrain['deaths']
    xtest=dtest[xs]
    ytest=dtest['deaths']

    print xtrain


    model=linear_model()
    model.fit(xtrain,ytrain)

    ytrain_predict=model.predict(xtrain)
    ytest_predict=model.predict(xtest)



    plt.plot(dtrain.index,ytrain_predict,label='Prediction')


    plt.plot(dtrain.index,ytrain,label='Actual')

    plt.legend()
    plt.title('Regression Training R2={}'.format(r2_score(ytrain,ytrain_predict)))
    plt.xticks(rotation=45)
    #plt.setp(splot[0].xaxis.get_majorticklabels(), rotation=45)
    #splot[1].hist(ypredict-dfiltered['deaths']e label='Residual Error')
    plt.show()

    train_resid=ytrain_predict-ytrain

    test_stationarity(train_resid)

    plt.plot(dtest.index,ytest_predict,label='Prediction')
    plt.plot(dtest.index,ytest,label='Actual')
    plt.xticks(rotation=45)
    plt.legend()
    plt.title('Regression Testing R2= {}'.format(r2_score(ytest,ytest_predict)))
    # plt.setp(splot[1].xaxis.get_majorticklabels(), rotation=45)
    #splot[1].hist(ypredict-dfiltered['deaths'], label='Residual Error')
    plt.show()

    test_resid = ytest_predict - ytest

    test_stationarity(test_resid)


# splot[0].legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)
#
# splot[1].legend(bbox_to_anchor=(1.05, 0), loc='lower left', borderaxespad=0.)


# plt.xticks(rotation=45)
# plt.title(region)
# plt.legend()



if __name__ =='__main__':

    run_regression1()







"""
dg=data()

cl=['red','blue','orange','green']
regions=['Midwest', 'Northeast' ,'South', 'West']
fig, ax_list = plt.subplots(2, 2, sharex=True)

print

fig.set_size_inches(10,7)

for region,splot,color in zip(regions,ax_list, cl):


    md=dg[dg['region']==region]
    splot[1].plot(md['date'],md['deaths'], label= region +' deaths',ls='--',color=color)
    splot[1].plot(md['date'], md['vmt'], label= region + ' vmt', ls='--',color=color)



    # # ax0.plot(md['date'],md['vmt'],label=r + ' vmt')
    #ax


    #sns.jointplot(x='vmt',y='deaths',data=md)
    #plt.scatter(md['vmt'],md['deaths'],label=r,c=cl[i])
    # plt.title(r)
    #
    #
    #
plt.legend()
plt.show()














exit()

data_train=data[data.year<2015]
data_test=data[data.year>=2015]

inputs=['vmt','Commuters']

xtrain=data_train[inputs]
xtrain=StandardScaler().fit_transform(xtrain)
ytrain=StandardScaler().fit_transform(data_train['ST_CASE'])

xtest=data_test[inputs]
xtest=StandardScaler().fit_transform(xtest)
ytest=StandardScaler().fit_transform(data_test['ST_CASE'])



model=RandomForestRegressor()
model=LinearRegression()
model.fit(xtrain,ytrain)


print model.score(xtrain,ytrain)
print model.score(xtest,ytest)


# args= model.feature_importances_
# print args

ypredict=model.predict(xtest)

index= np.argsort(ytest)

plt.figure(figsize=(25,15))
plt.plot(ypredict,label='predict_test')
plt.plot(ytest,label='test')
plt.legend()

ypredict=model.predict(xtrain)


plt.figure(figsize=(25,15))

plt.plot(ypredict,label='predict_train')
plt.plot(ytrain,label='train')


plt.legend()
plt.show()


# print data


"""
