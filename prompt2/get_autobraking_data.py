import pandas as pd
import requests
import plotly.plotly as py
import time


def get_make_names(year):
    url = 'http://www.iihs.org/ratings/hldifeatures/getselectcrashavoidanceviewmodel/{}'.format(year)
    r = requests.get(url)
    makes = r.json()['Makes']
    return [make['Value'] for make in makes]


def get_safety_data(year, make):
    url = 'http://www.iihs.org/ratings/hldifeatures/getcrashavoidancevehicleresults'
    payload = {'SelectedYear':year, 'SelectedMakeName':make}
    r = requests.post(url, data = payload)
    try:
        vehicles = r.json()['Vehicles']
    except ValueError:
        vehicles = []
    data_list = []
    for vehicle in vehicles:
        warning = vehicle['Features'].get('Feature8006', {'OptionValue':'Not available'})['OptionValue']
        auto_braking = vehicle['Features'].get('Feature8020', {'OptionValue':'Not available'})['OptionValue']
        data_list.append({'year':year, 'make':make, 'warning':warning, 'auto_braking':auto_braking})
    return data_list


if __name__ == '__main__':
    years = range(2001, 2018)
    make_dict = dict()
    for year in years:
        make_dict[year] = get_make_names(year)

    data_list = []
    for year, makes in make_dict.iteritems():
        for make in makes:
            data_list.extend(get_safety_data(year, make))

    df = pd.DataFrame(data_list)
    # df.to_csv('autobraking_data.csv', index=False)
