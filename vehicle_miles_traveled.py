import urllib
import xlrd
import os
import pandas as pd
from bs4 import BeautifulSoup
import urlparse
import re
import threading

'''saving vmt excel files to vmt_files'''

months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
full_months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
               'August', 'September', 'October', 'November', 'December']

save_dir='./vmt_files'
url = 'https://www.fhwa.dot.gov/policyinformation/travel_monitoring/tvt.cfm'

def get_xls(url=url):

    files_in_dir=os.listdir(save_dir)
    page = urllib.urlopen(url)

    soup = BeautifulSoup(page, 'lxml')

    for link in soup.find_all('a',href=True):
        if link.text=='XLS':
            url= urlparse.urljoin('https://www.fhwa.dot.gov/policyinformation/travel_monitoring/tvt.cfm',link['href'])

            print 'retrieving...',url
            file= re.search(r'1\d\D+\.xls$',url)
            if file in files_in_dir:
                break
            jobs=[]
            if file:
                urllib.urlretrieve(url,'{}/{}'.format(save_dir,file.group()))




states=[ u'Connecticut', u'Maine', u'Massachusetts', u'New Hampshire', u'New Jersey', u'New York', u'Pennsylvania', u'Rhode Island', u'Vermont', u'South Atlantic', u'Delaware', u'District of Columbia', u'Florida', u'Georgia', u'Maryland', u'North Carolina', u'South Carolina', u'Virginia', u'West Virginia', u'North Central', u'Illinois', u'Indiana', u'Iowa', u'Kansas', u'Michigan', u'Minnesota', u'Missouri', u'Nebraska', u'North Dakota', u'Ohio', u'South Dakota', u'Wisconsin',u'Alabama', u'Arkansas', u'Kentucky', u'Louisiana', u'Mississippi', u'Oklahoma', u'Tennessee', u'Texas', u'Alaska', u'Arizona', u'California', u'Colorado', u'Hawaii', u'Idaho', u'Montana', u'Nevada', u'New Mexico', u'Oregon', u'Utah', u'Washington', u'Wyoming',]



def open_xls(path=save_dir):

    for file in os.listdir(path):

        print file
        year=int('20'+file[:2])
        month=months.index(file[2:5])

        book=xlrd.open_workbook(os.path.join(path,file))
        yield year,month,book,file


def write_csv():
    vmt_csv=open('./vmt.csv','a')
    vmt_csv.write('state,vmt,year,month,file\n')

    for book in open_xls():
        yr,mo,wkb,file=book

        sheet = wkb.sheet_by_name('Page 6')
        sht_month= sheet.cell_value(rowx=2,colx=3)
        sht_year=int(sheet.cell_value(rowx=4,colx=5))


        if sht_month!=full_months[mo] or sht_year!=yr-1:
            print '*******'
            print    sht_month, sht_year

            print 'wrong month or year'
            print '*******'


        rows=sheet.get_rows()

        for row in rows:

            if row[0].value in states:
                print row[0].value,row[5].value, sht_year,full_months.index(sht_month)+1,file
                text='{},{},{},{},{}\n'.format(row[0].value,row[5].value, sht_year,full_months.index(sht_month)+1,file)
                vmt_csv.write(text)

def write_csv_single():
    vmt_csv = open('./vmt_new.csv', 'a')
    #vmt_csv.write('state,vmt,year,month,file\n')

    wkb=xlrd.open_workbook('./vmt_files/15dectvt.xls')


    sheet = wkb.sheet_by_name('Page 6')
    sht_month = sheet.cell_value(rowx=2, colx=3)
    sht_year = 2015  #int(sheet.cell_value(rowx=4, colx=5))


    rows = sheet.get_rows()

    for row in rows:

        if row[0].value in states:
            print row[0].value, row[4].value, sht_year, full_months.index(sht_month) + 1, '15dectvt.xls'
            text = '{},{},{},{},{}\n'.format(row[0].value, row[4].value, sht_year,
                                             full_months.index(sht_month) + 1, '15dectvt.xls')
            vmt_csv.write(text)

write_csv_single()
                                #write_csv()