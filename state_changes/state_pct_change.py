import pandas as pd


if __name__ == '__main__':
    # accident = pd.read_csv('accident.csv')
    # opioids = pd.read_csv('2014-2015-increase-data.csv')
    #
    # acc_14 = accident[accident['YEAR'] == 2014]
    # acc_15 = accident[accident['YEAR'] == 2015]
    #
    # state_14 = acc_14.groupby('STATE', as_index = False).sum()[['STATE', 'FATALS']]
    # state_15 = acc_15.groupby('STATE', as_index = False).sum()[['STATE', 'FATALS']]
    #
    # combined = pd.merge(state_14, state_15, how = 'outer', on = 'STATE')
    #
    # combined['percent_change'] = (combined.FATALS_y - combined.FATALS_x) / combined.FATALS_x
