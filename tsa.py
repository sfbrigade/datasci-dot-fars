from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import acf,pacf

from statsmodels.tsa.stattools import adfuller
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
def test_stationarity(timeseries):
    # Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    # Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue' ,label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()
    # Perform Dickey-Fuller test:
    print 'Results of Dickey-Fuller Test:'
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic' ,'p-value' ,'#Lags Used' ,'Number of Observations Used'])
    for key ,value in dftest[4].items():
        dfoutput[ 'Critical Value (%s)' %key] = value
    print dfoutput

def decompose():

    deaths=data()[['deaths']]

    ts_log=np.log(deaths)


    from statsmodels.tsa.seasonal import seasonal_decompose
    decomposition = seasonal_decompose(ts_log)

    trend = decomposition.trend
    seasonal = decomposition.seasonal
    residual = decomposition.resid

    # plt.subplot(411)
    # plt.plot(ts_log, label='Original')
    # plt.legend(loc='best')
    # plt.subplot(412)
    # plt.plot(trend, label='Trend')
    # plt.legend(loc='best')
    # plt.subplot(413)
    # plt.plot(seasonal,label='Seasonality')
    # plt.legend(loc='best')
    # plt.subplot(414)
    # plt.plot(residual, label='Residuals')
    # plt.legend(loc='best')
    # plt.tight_layout()
    #plt.show()



    ts_log_decompose=residual
    ts_log_decompose.dropna(inplace=True)

    #test_stationarity(ts_log_decompose['deaths'])

    return ts_log_decompose

def acf_pacf():
    deaths=data()['deaths']
    ts_log=np.log(deaths)

    ts_log_diff = ts_log - ts_log.shift()
    ts_log_diff.dropna(inplace=True)

    lag_acf = acf(ts_log_diff, nlags=20)



    lag_pacf = pacf(ts_log_diff, nlags=20, method='ols')

    #Plot ACF:
    plt.subplot(121)
    plt.plot(lag_acf)
    plt.axhline(y=0,linestyle='--',color='gray')
    plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.title('Autocorrelation Function')

    #Plot PACF:
    plt.subplot(122)
    plt.plot(lag_pacf)
    plt.axhline(y=0,linestyle='--',color='gray')
    plt.axhline(y=-1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.axhline(y=1.96/np.sqrt(len(ts_log_diff)),linestyle='--',color='gray')
    plt.title('Partial Autocorrelation Function')
    plt.tight_layout()

    plt.show()

#
# deaths=data()['deaths']
# ts_log=np.log(deaths)
#
# ts_log_diff = ts_log - ts_log.shift()
# ts_log_diff.dropna(inplace=True)


# model = ARIMA(ts_log, order=(2, 0, 0))
# results_AR = model.fit(disp=-1)
# plt.plot(ts_log_diff)
# plt.plot(results_AR.fittedvalues, color='red')
# plt.title('RSS: %.4f'% sum((results_AR.fittedvalues-ts_log_diff)**2))
#
# plt.show()
# model = ARIMA(ts_log, order=(0, 1, 0))
# results_MA = model.fit(disp=-1)
# plt.plot(ts_log_diff)
# plt.plot(results_MA.fittedvalues, color='red')
# plt.title('RSS: %.4f'% sum((results_MA.fittedvalues-ts_log_diff)**2))
#
# # plt.show()
# model = ARIMA(ts_log, order=(3,1, 3))
# results_ARIMA = model.fit(disp=-1)
# # plt.plot(ts_log_diff)
# # plt.plot(results_ARIMA.fittedvalues, color='red')
# # print len(results_ARIMA.fittedvalues)
# # print len(ts_log_diff)
# # plt.title('RSS: %.4f'% sum((results_ARIMA.fittedvalues-ts_log_diff)**2))
#
# # plt.show()
#
# predictions_ARIMA_diff = pd.Series(results_ARIMA.fittedvalues, copy=True)
# print predictions_ARIMA_diff.head()
#
# predictions_ARIMA_diff_cumsum = predictions_ARIMA_diff.cumsum()
# print predictions_ARIMA_diff_cumsum.head()
#
# predictions_ARIMA_log = pd.Series(ts_log.ix[0], index=ts_log.index)
# predictions_ARIMA_log = predictions_ARIMA_log.add(predictions_ARIMA_diff_cumsum,fill_value=0)
# predictions_ARIMA_log.head()
#

#
# predictions_ARIMA = np.exp(predictions_ARIMA_log)
# plt.plot(deaths)
# plt.plot(predictions_ARIMA)
# plt.title('RMSE: %.4f'% np.sqrt(sum((predictions_ARIMA-deaths)**2)/len(deaths)))
#
# plt.show()