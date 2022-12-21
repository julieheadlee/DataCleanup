from numpy.lib.function_base import diff
import pandas as pd
import numpy as np
import re

# 3 Formats file to be ready for comparison

dfMaster = pd.read_csv('../MasterTracking_Data/Master Tracking Trimmed.csv', dtype=str, low_memory=False)

# Float Formatting
def FloatFormatting(Column):
    return Column.str.replace('.0','',regex=False)

dfMaster['EID_M'] = FloatFormatting(dfMaster['EID_M'])
dfMaster['EID_AM'] = FloatFormatting(dfMaster['EID_AM'])
dfMaster['Phone_M'] = FloatFormatting(dfMaster['Phone_M'])
dfMaster['Phone_AM'] = FloatFormatting(dfMaster['Phone_AM'])
dfMaster['Phone_BE'] = FloatFormatting(dfMaster['Phone_BE'])
dfMaster['Phone_WD'] = FloatFormatting(dfMaster['Phone_WD'])
dfMaster['Phone_EOC'] = FloatFormatting(dfMaster['Phone_EOC'])
dfMaster['Zip_M'] = FloatFormatting(dfMaster['Zip_M'])
dfMaster['Zip_AM'] = FloatFormatting(dfMaster['Zip_AM'])
dfMaster['Zip_BE'] = FloatFormatting(dfMaster['Zip_BE'])
dfMaster['Zip_WD'] = FloatFormatting(dfMaster['Zip_WD'])
dfMaster['LicenseNumber_BE'] = FloatFormatting(dfMaster['LicenseNumber_BE'])
dfMaster['LicenseNumber_EOC'] = FloatFormatting(dfMaster['LicenseNumber_EOC'])
dfMaster['SS#_BE'] = FloatFormatting(dfMaster['SS#_BE'])
dfMaster['SS#_WD'] = FloatFormatting(dfMaster['SS#_WD'])

dfMaster['FirstName_M'] = dfMaster['FirstName_M'].str.title()
dfMaster['FirstName_AM'] = dfMaster['FirstName_AM'].str.title()
dfMaster['FirstName_BE'] = dfMaster['FirstName_BE'].str.title()
dfMaster['FirstName_WD'] = dfMaster['FirstName_WD'].str.title()
dfMaster['FirstName_EOC'] = dfMaster['FirstName_EOC'].str.title()

dfMaster['LastName_M'] = dfMaster['LastName_M'].str.title()
dfMaster['LastName_AM'] = dfMaster['LastName_AM'].str.title()
dfMaster['LastName_BE'] = dfMaster['LastName_BE'].str.title()
dfMaster['LastName_WD'] = dfMaster['LastName_WD'].str.title()
dfMaster['LastName_EOC'] = dfMaster['LastName_EOC'].str.title()

dfMaster['MiddleName_BE'] = dfMaster['MiddleName_BE'].str.title()
dfMaster['MiddleName_WD'] = dfMaster['MiddleName_WD'].str.title()
dfMaster['MiddleName_EOC'] = dfMaster['MiddleName_EOC'].str.title()

print('Name formatted')

# Abbreviating classes in Mobilize, classes that will show as DC but should stay the same in Mobilize are abbreviated to DC
dfFormatMClass = pd.read_csv('../MasterTrackingFormatting/MobilizeClass.csv', index_col=0, low_memory=False)
MClassFormat = dfFormatMClass.to_dict()['Abbreviation'] # Grabs the embedded dictionary
# Turns the Dictionary into a regular expression that replaces only whole words
MClassFormat = {
    f'(^|,\s\s){MobilizeClass}($|,)': f'\\1{Abbreviation}\\2'
    for MobilizeClass, Abbreviation in MClassFormat.items()
}

dfMaster['Class_M'] = dfMaster['Class_M'].str.replace('Federal ', '', regex=False)
dfMaster['Class_M'] = dfMaster['Class_M'].replace(MClassFormat, regex=True)

dfMaster['Class_BE'] = dfMaster['Class_BE'].str.upper().replace('(^|\s)RT($|\s)', '\\1RRT\\2', regex=True)
dfMaster['Class_BE'] = dfMaster['Class_BE'].str.upper().replace('(^|\s|-)GOV($|\s)', '\\1\\2', regex=True)

dfMaster['Class_M'] = dfMaster['Class_M'].str.replace('-', '', regex=False).str.strip()
dfMaster['Class_BE'] = dfMaster['Class_BE'].str.replace('-', '', regex=False).str.strip()
dfMaster['Class_AM'] = dfMaster['Class_AM'].str.replace('-', '', regex=False).str.strip()

print('Class formatted')

dfFormatMArea = pd.read_csv('../MasterTrackingFormatting/MobilizeArea.csv', index_col=0, low_memory=False)
MAreaFormat = dfFormatMArea.to_dict()['Abbreviation'] # Grabs the embedded dictionary
# Turns the Dictionary into a regular expression that replaces only whole words
MAreaFormat = {
    f'(^|,\s\s){MobilizeArea}($|,)': f'\\1{Abbreviation}\\2'
    for MobilizeArea, Abbreviation in MAreaFormat.items()
}

dfMaster['Specialty_M'] = dfMaster['Specialty_M'].replace(MAreaFormat, regex=True)

print('Specialty formatted')

#dfMaster['DOB_M'] = dfMaster['DOB_M'].str.replace(' 00:00:00', '', regex=True)
#dfMaster['DOB_M'] = dfMaster['DOB_M'].str.replace('-', '/', regex=True)
#taking first 5 characters from the year
#dfTemp = dfMaster['DOB_M'].str[:5]
#getting rid of the rest
#dfMaster['DOB_M'] = dfMaster['DOB_M'].str[5:]
#dfTemp = dfTemp.str.replace('/', '', regex=True)
#dfTemp2 = dfMaster['DOB_M'] + '/' + dfTemp
#dfMaster['DOB_M'] = dfTemp2


# Takes first 5 of the zip - removing the extension from sources in w/e, and adds preceding zeros for places like Mobilize
dfMaster['Zip_M'] = dfMaster['Zip_M'].str[:5].str.zfill(5)
dfMaster['Zip_AM'] = dfMaster['Zip_AM'].str[:5].str.zfill(5)
dfMaster['Zip_BE'] = dfMaster['Zip_BE'].str[:5].str.zfill(5)
dfMaster['Zip_WD'] = dfMaster['Zip_WD'].str[:5].str.zfill(5)

#replacing '-' in licenses number as Rn-1111 and RN1111 are the same thing
dfMaster['LicenseNumber_BE'] = dfMaster['LicenseNumber_BE'].str.replace('-', '', regex=True)
dfMaster['LicenseNumber_EOC'] = dfMaster['LicenseNumber_EOC'].str.replace('-', '', regex=True)

def format_Dates(series):
    date_parts = series.str.split('/', expand=True)
    return date_parts[0].str.zfill(2) + '/' + date_parts[1].str.zfill(2) + '/' + date_parts[2]


dfMaster['DOB_M'] = format_Dates(dfMaster['DOB_M'])
dfMaster['DOB_BE'] = format_Dates(dfMaster['DOB_BE'])
dfMaster['DOB_WD'] = format_Dates(dfMaster['DOB_WD'])
dfMaster['DOB_EOC'] = format_Dates(dfMaster['DOB_EOC'])

dfMaster['DOB_M'] = np.where(dfMaster.apply(lambda x: x['DOB_M'][-4:] != '1900', axis=1), dfMaster['DOB_M'], '')

genderAbr = {'Male': 'M', 'Female': 'F'}

dfMaster['Gender_AM'] = dfMaster['Gender_AM'].str.strip().str.title().replace(genderAbr)
dfMaster['Gender_BE'] = dfMaster['Gender_BE'].str.strip().str.title().replace(genderAbr)
dfMaster['Gender_EOC'] = dfMaster['Gender_EOC'].str.strip().str.title().replace(genderAbr)

print('Gender formatted')

dfAddressAbr = pd.read_csv('../MasterTrackingFormatting/AddressAbbreviations.csv', index_col=0, low_memory=False)
addressLingo = dfAddressAbr.to_dict()['Abbreviation'] # Grabs the embedded dictionary
# Turns the Dictionary into a regular expression that replaces only whole words
addressLingo = {
    f'(^|\s){AddressElement}($|\s)': f'\\1{Abbreviation}\\2'
    for AddressElement, Abbreviation in addressLingo.items()
}

dfMaster['Address_M'] = dfMaster['Address_M'].str.replace('.', '', regex=True)
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.replace('.', '', regex=True)
dfMaster['Address_WD'] = dfMaster['Address_WD'].str.replace('.', '', regex=True)

dfMaster['Address_M'] = dfMaster['Address_M'].str.replace(',', '', regex=True)
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.replace(',', '', regex=True)
dfMaster['Address_WD'] = dfMaster['Address_WD'].str.replace(',', '', regex=True)

dfMaster['Address_M'] = dfMaster['Address_M'].str.strip().str.title().replace(addressLingo, regex=True)
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.strip().str.title().replace(addressLingo, regex=True)
dfMaster['Address_WD'] = dfMaster['Address_WD'].str.strip().str.title().replace(addressLingo, regex=True)
dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.strip().str.title().replace(addressLingo, regex=True)

dfMaster['Address_BE'] = dfMaster['Address_BE'].str.title()
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.replace('#', '', regex=True)
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.replace('.', '', regex=True)
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.replace('Apt ', '', regex=True)
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.replace('Unit ', '', regex=True)
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.replace('Fl ', '', regex=True)
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.replace('Ste ', '', regex=True)
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.replace('Bsmt ', '', regex=True)
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.replace('Lot ', '', regex=True)
dfMaster['Address_BE'] = dfMaster['Address_BE'].str.replace('Pmb ', '', regex=True)

dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.title()
dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.replace('Apt', '', regex=True)
dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.replace('Unit', '', regex=True)
dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.replace('Fl', '', regex=True)
dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.replace('Ste', '', regex=True)
dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.replace('Bsmt', '', regex=True)
dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.replace('Lot', '', regex=True)
dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.replace('Pmb', '', regex=True)
dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.replace('.', '', regex=True)
dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.replace('#', '', regex=True)
dfMaster['Address Line 2'] = dfMaster['Address Line 2'].str.replace(' ', '', regex=True)
dfMaster['Address_WD'] = np.where(dfMaster['Address Line 2'].isnull(), dfMaster['Address_WD'], dfMaster['Address_WD'].map(str) + ' ' + dfMaster['Address Line 2'].map(str))

dfMaster['Address_WD'] = dfMaster['Address_WD'].str.replace(' nan', '', regex=True)
dfMaster['Address_WD'] = dfMaster['Address_WD'].str.replace('nan', '', regex=True)

print('Address formatted')

dfMaster['City_M'] = dfMaster['City_M'].str.strip().str.title()
dfMaster['City_AM'] = dfMaster['City_AM'].str.strip().str.title()
dfMaster['City_BE'] = dfMaster['City_BE'].str.strip().str.title()
dfMaster['City_WD'] = dfMaster['City_WD'].str.strip().str.title()

print('City formatted')

dfStateAbr = pd.read_csv('../MasterTrackingFormatting/StateAbbreviations.csv', index_col=0, low_memory=False)
stateAbr = dfStateAbr.to_dict()['Abbreviation'] # Grabs the embedded dictionary

dfMaster['State_M'] = dfMaster['State_M'].str.strip().str.upper().replace(stateAbr, regex=True)
dfMaster['State_AM'] = dfMaster['State_AM'].str.strip().str.upper().replace(stateAbr, regex=True)
dfMaster['State_BE'] = dfMaster['State_BE'].str.strip().str.upper().replace(stateAbr, regex=True)
dfMaster['State_WD'] = dfMaster['State_WD'].str.strip().str.upper().replace(stateAbr, regex=True)

print('State formatted')

dfMaster['Zip_M'] = dfMaster['Zip_M'].str.zfill(5)
dfMaster['Zip_AM'] = dfMaster['Zip_AM'].str.zfill(5)
dfMaster['Zip_BE'] = dfMaster['Zip_BE'].str.zfill(5)
dfMaster['Zip_WD'] = dfMaster['Zip_WD'].str.zfill(5)

print('Zip formatted')

dfMaster['LicenseState_AM'] = dfMaster['LicenseState_AM'].str.strip().str.upper().replace(stateAbr, regex=True)
dfMaster['LicenseState_BE'] = dfMaster['LicenseState_BE'].str.strip().str.upper().replace(stateAbr, regex=True)

dfMaster.to_csv('../MasterTracking_Data/Post Format of Columns.csv')
print('FormattingFile Generated')
