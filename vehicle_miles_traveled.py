import urllib

'''saving vmt excel files to vmt_files'''

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
years = range(10, 17)
years = [str(year) for year in years]

address = 'https://www.fhwa.dot.gov/policyinformation/travel_monitoring/{}/{}.xls'

for year in years:
    for month in months:
        file = '{}{}tvt'.format(year, month)
        url = address.format(file, file)
        print url
        urllib.urlretrieve(url, './vmt_files/{}.xls'.format(file))
