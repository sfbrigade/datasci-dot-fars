import pandas as pd
import urllib
import zipfile
import os


def get_data(start_year, end_year):
    for year in xrange(start_year, end_year + 1):
        if year <= 2011:
            url = 'ftp://ftp.nhtsa.dot.gov/FARS/{}/SAS/FSAS{}.zip'.format(year, year)
        elif year == 2012:
            url = 'ftp://ftp.nhtsa.dot.gov/FARS/{}/National/SAS/FSAS{}.zip'.format(year, year)
        else:
            url = 'ftp://ftp.nhtsa.dot.gov/FARS/{}/National/FARS{}NationalSAS.zip'.format(year, year)
        filename = url.split('/')[-1]

        urllib.urlretrieve(url, filename)


def unzip_and_read(zip_file):
    zf = zipfile.ZipFile(zip_file)
    zf.extract('vehicle.sas7bdat')
    df = pd.read_sas('vehicle.sas7bdat')
    df['YEAR'] = int(zip_file[4:8])
    zf.close()
    return df


if __name__ == '__main__':
    os.chdir('./fars_raw')
    # get_data(2013, 2015)

    zip_files = os.listdir('.')
    df = unzip_and_read(zip_files.pop(0))
    for zip_file in zip_files:
        df = pd.merge(df, unzip_and_read(zip_file), how = 'outer')

    df.to_csv('vehicle_01_15.csv', index = False)


    car_make_dict = {1: "American Motors",
    2: "Jeep/Kaiser-Jeep/Willys Jeep",
    3: "AM General",
    6: "Chrysler",
    7: "Dodge",
    8: "Imperial",
    9: "Plymouth",
    10: "Eagle",
    12: "Ford",
    13: "Lincoln",
    14: "Mercury",
    18: "Buick/Opel",
    19: "Cadillac",
    20: "Chevrolet",
    21: "Oldsmobile",
    22: "Pontiac",
    23: "GMC",
    24: "Saturn",
    25: "Grumman",
    26: "Coda (Since 2013)",
    29: "Other Domestic, Avanti Checker DeSoto Excalibur Hudson Packard Panoz Saleen Studebaker Stutz, Tesla (Since 2014)",
    30: "Volkswagen",
    31: "Alfa Romeo",
    32: "Audi",
    33: "Austin/Austin Healey",
    34: "BMW",
    35: "Datsun/Nissan",
    36: "Fiat",
    37: "Honda",
    38: "Isuzu",
    39: "Jaguar",
    40: "Lancia",
    41: "Mazda",
    42: "Mercedes-Benz",
    43: "MG",
    44: "Peugeot",
    45: "Porsche",
    46: "Renault",
    47: "Saab",
    48: "Subaru",
    49: "Toyota",
    50: "Triumph",
    51: "Volvo",
    52: "Mitsubishi",
    53: "Suzuki",
    54: "Acura",
    55: "Hyundai",
    56: "Merkur",
    57: "Yugo",
    58: "Infiniti",
    59: "Lexus",
    60: "Daihatsu",
    61: "Sterling",
    62: "Land Rover",
    63: "Kia",
    64: "Daewoo",
    65: "Smart (Since 2010)",
    66: "Mahindra (2011-2013)",
    67: "Scion (Since 2012)",
    69: "Other Imports",
    70: "BSA",
    71: "Ducati",
    72: "Harley-Davidson",
    73: "Kawasaki",
    74: "Moto Guzzi",
    75: "Norton",
    76: "Yamaha",
    77: "Victory",
    78: "Other Make Moped (Since 2010)",
    79: "Other Make Motored Cycle (Since 2010)",
    80: "Brockway",
    81: "Diamond Reo/Reo",
    82: "Freightliner",
    83: "FWD",
    84: "International Harvester/Navistar",
    85: "Kenworth",
    86: "Mack",
    87: "Peterbilt",
    88: "Iveco/Magirus",
    89: "White/Autocar, White/GMC",
    90: "Bluebird",
    91: "Eagle Coach",
    92: "Gillig",
    93: "MCI",
    94: "Thomas Built",
    97: "Not Reported (Since 2010)",
    98: "Other Make",
    99: "Unknown Make"}
