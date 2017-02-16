import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
vmt=pd.read_csv('./vmt.csv')
bikers=pd.read_csv('./bicycle_commuters_by_state.csv')
bikers=bikers[bikers['Survey']=='ACS5']
bikers.rename(inplace=True,columns={'Geography':'state_abbv','Year':'year'})


states=pd.read_csv('./US State Abbreviations.csv')
states.rename(columns={'Postal Code':'state_abbv','Name':'state'},inplace=True)

deaths=pd.read_csv('./bicycle_deaths_with_temps.csv')

deaths.rename(columns={'DEATH_YR':'year','ST_CASE':'bike_deaths'},inplace=True)





deaths_states=pd.merge(states,deaths, how='inner',left_on='FIPS',right_on='STATE')


#print deaths_states
# deaths_states[(deaths_states['TEMP_F']>0) & (deaths_states['state_abbv']=='AL')]['TEMP_F'].plot.hist(bins=100)
#
#
# plt.show()
# exit()






deaths_states_year=pd.DataFrame( deaths_states.groupby(['state','year','state_abbv'])
                                 .agg({'bike_deaths':'count','TEMP_F':'mean'})).reset_index()


vmt_state_year= pd.DataFrame( vmt.groupby(['year','state'],)['vmt'].sum()).reset_index()



deaths_vmt_state_year=pd.merge(deaths_states_year,vmt_state_year,on=['state','year'])



deaths_vmt_bikers_state_year=pd.merge(left=deaths_vmt_state_year,right=bikers,on=['state_abbv','year'])

deaths_vmt_bikers_state_year['year']=deaths_vmt_bikers_state_year['year'].apply(lambda x: int(x))


print deaths_vmt_bikers_state_year.columns
deaths_vmt_bikers_year=deaths_vmt_bikers_state_year.groupby('year').agg({

    'bike_deaths':'sum','TEMP_F':"mean",'vmt':"sum",'Population':"sum",'Commuters':"sum",'Bicycle commuters':'sum'})



deaths_vmt_bikers_year=pd.DataFrame(deaths_vmt_bikers_year).reset_index()
# print deaths_vmt_bikers_year
print deaths_vmt_bikers_state_year
print vmt.groupby('year')['vmt'].sum()

deaths_vmt_bikers_state_year.to_csv('deaths_vmt_bikers_state_year.csv')


sns.pairplot(deaths_vmt_bikers_year,hue='year',palette='husl',markers=["o", "s", "D",'x','v','8'])
plt.show()


