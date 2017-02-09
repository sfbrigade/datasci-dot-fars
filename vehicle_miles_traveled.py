import urllib

'''saving vmt excel files to vmt_files'''

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
years = range(10, 17)

yearstext = [str(year) for year in years]

addressnew = 'https://www.fhwa.dot.gov/policyinformation/travel_monitoring/{}/{}.xls'
addressold='https://www.fhwa.dot.gov/ohim/tvtw/{}/{}.xls'


for year in years:
    for month in months:
        file = '{}{}tvt'.format(year, month)

        if year>10:
            address=addressnew
        else:
            address=addressold

        url = address.format(file, file)

        print url
        urllib.urlretrieve(url, './vmt_files/{}.xls'.format(file))
