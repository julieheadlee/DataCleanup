from numpy.lib.function_base import diff
import pandas as pd
import numpy as np
import re

# 4 Determines what is different and what is the same

NaN = np.nan

dfMaster = pd.read_csv('../MasterTracking_Data/Post Format of Columns.csv', dtype=str, low_memory=False)
#dfMaster = pd.read_csv('../MasterTracking_Data/Test1.csv')

print(dfMaster.info(verbose=True))

# Checks whether a corresponding profile exists in each of the databases for every row
# Assumes every row will have a Mobilize Profile
# Mobilize Existence Check mainly for custom checks which require 2 existence columns, this will produce a column of all Trues, unless something weird happens
MOEC = np.where(~dfMaster['EID_M'].isnull(), True, False)
AMEC = np.where(~dfMaster['FirstName_AM'].isnull() |
                ~dfMaster['LastName_AM'].isnull() |
                ~dfMaster['Email_AM'].isnull() |
                ~dfMaster['Phone_AM'].isnull() |
                ~dfMaster['City_AM'].isnull() |
                ~dfMaster['State_AM'].isnull() |
                ~dfMaster['Zip_AM'].isnull() |
                ~dfMaster['Gender_AM'].isnull() |
                ~dfMaster['Class_AM'].isnull() |
                ~dfMaster['Specialty_AM'].isnull(), True, False)
dfMaster['Profile Exists_AM'] = AMEC
BEEC = np.where(~dfMaster['FirstName_BE'].isnull() |
                ~dfMaster['MiddleName_BE'].isnull() |
                ~dfMaster['LastName_BE'].isnull() |
                ~dfMaster['Email_BE'].isnull() |
                ~dfMaster['Phone_BE'].isnull() |
                ~dfMaster['Gender_BE'].isnull() |
                ~dfMaster['DOB_BE'].isnull() |
                ~dfMaster['Class_BE'].isnull() |
                ~dfMaster['Specialty_BE'].isnull() |
                ~dfMaster['Address_BE'].isnull() |
                ~dfMaster['City_BE'].isnull() |
                ~dfMaster['State_BE'].isnull() |
                ~dfMaster['Zip_BE'].isnull(), True, False)
dfMaster['Profile Exists_BE'] = BEEC
WDEC = np.where(~dfMaster['FirstName_WD'].isnull() |
                ~dfMaster['MiddleName_WD'].isnull() |
                ~dfMaster['LastName_WD'].isnull() |
                ~dfMaster['Phone_WD'].isnull() |
                ~dfMaster['Email_WD'].isnull() |
                ~dfMaster['DOB_WD'].isnull(), True, False)
dfMaster['Profile Exists_WD'] = WDEC
EOCEC = np.where(~dfMaster['FirstName_EOC'].isnull() |
                ~dfMaster['LastName_EOC'].isnull() |
                ~dfMaster['MiddleName_EOC'].isnull() |
                ~dfMaster['Gender_EOC'].isnull() |
                ~dfMaster['Email_EOC'].isnull() |
                ~dfMaster['DOB_EOC'].isnull() |
                ~dfMaster['Phone_EOC'].isnull() |
                ~dfMaster['Class_EOC'].isnull(), True, False)
dfMaster['Profile Exists_EOC'] = EOCEC

# Comparisons
def Comparison(MobilizeColumn, ComparisonColumn, ExistenceColumn):
    return np.where((MobilizeColumn == ComparisonColumn) | ((MobilizeColumn != MobilizeColumn) & (ComparisonColumn != ComparisonColumn)) | ~ExistenceColumn, True, False)
def CustomComparison(DataBase, EqualityCheck, Column1, Column2, ExistenceColumn1, ExistenceColumn2):
    return np.where(DataBase.apply(lambda x: EqualityCheck(x[Column1], x[Column2]), axis=1) | ((Column1 != Column1) & (Column2 != Column2)) | ~ExistenceColumn1 | ~ExistenceColumn2, True, False)

# Whole Abbreviation searching
def SearchIn(Entry1, Entry2):
    x = f'(^|\s|/|,){Entry1}($|\s|/|;|,)' # Ensures Entry1 matches a whole Abbreviation and not a partial Abbreviation in Entry2
    if re.search(x, Entry2):
        return True
    else:
        return False

# Splits a given entry of Mobilize Classes or Areas and checks whether each one of them is in AM
def MInAM(MobilizeEntry, AMEntry):
    mEntries = MobilizeEntry.split(',')
    mEntries = [s.strip() for s in mEntries]
    mobInAM = True
    for i in mEntries:
        mobInAM *= SearchIn(i, AMEntry)
    return mobInAM

# Lists of Ranked Classes
dfRankedClass1 = pd.read_csv('../MasterTrackingFormatting/RankedClasses.csv', index_col=0, low_memory=False)
dfRankedClass2 = pd.read_csv('../MasterTrackingFormatting/RankedClasses.csv', index_col=1, low_memory=False)
RankedClass1 = dfRankedClass1.to_dict()['Rank2'] # Grabs the embedded dictionary
RankedClass2 = dfRankedClass2.to_dict()['Rank3'] # Grabs the embedded dictionary
# Turns the Dictionary into a regular expression that replaces only whole words, if not using can ignore this
RankedClass1 = {
    f'(^|,\s\s|/){Rank1}($|/|,)': f'\\1{Rank2}\\2'
    for Rank1, Rank2 in RankedClass1.items()
}
RankedClass2 = {
    f'(^|,\s\s|/){Rank2}($|/|,)': f'\\1{Rank3}\\2'
    for Rank2, Rank3 in RankedClass2.items()
}
RankedClass3 = {
    '(^|,\s\s|/)(.*?)($|/|,)': '\\1DC\\3'
}

# Checks whether Entry2 has an equivalent or higher class
def RankedSearchIn(Entry1, Entry2):
    w = Entry2
    x = w
    for key in RankedClass1:
        x = re.sub(key, RankedClass1[key], x)
    y = x
    for key in RankedClass2:
        y = re.sub(key, RankedClass2[key], y)
    z = y
    for key in RankedClass3:
        z = re.sub(key, RankedClass3[key], z)
    Rank1 = SearchIn(Entry1, w)
    Rank2 = SearchIn(Entry1, x)
    Rank3 = SearchIn(Entry1, y)
    Rank4 = SearchIn(Entry1, z)
    return Rank1 or Rank2 or Rank3 or Rank4

dfMaster['MOBILIZE ID Okay?'] = np.where(Comparison(dfMaster['EID_M'], dfMaster['EID_AM'], AMEC), 'Correct', 'Fix')

comparisonWorkdayID1 = Comparison(dfMaster['WDID_M'], dfMaster['WDID_AM'], AMEC)
comparisonWorkdayID2 = Comparison(dfMaster['WDID_M'], dfMaster['WDID_WD'], WDEC)
dfMaster['WORKDAY ID Okay?'] = np.where(comparisonWorkdayID1 & comparisonWorkdayID2, 'Correct', 'Fix')

comparisonFirst1 = Comparison(dfMaster['FirstName_M'], dfMaster['FirstName_AM'], AMEC)
comparisonFirst2 = Comparison(dfMaster['FirstName_M'], dfMaster['FirstName_BE'], BEEC)
comparisonFirst3 = Comparison(dfMaster['FirstName_M'], dfMaster['FirstName_WD'], WDEC)
comparisonFirst4 = Comparison(dfMaster['FirstName_M'], dfMaster['FirstName_EOC'], EOCEC)
dfMaster['FIRST NAME Okay?'] = np.where(comparisonFirst1 & comparisonFirst2 & comparisonFirst3 & comparisonFirst4, 'Correct', 'Fix')

comparisonLast1 = Comparison(dfMaster['LastName_M'], dfMaster['LastName_AM'], AMEC)
comparisonLast2 = Comparison(dfMaster['LastName_M'], dfMaster['LastName_BE'], BEEC)
comparisonLast3 = Comparison(dfMaster['LastName_M'], dfMaster['LastName_WD'], WDEC)
comparisonLast4 = Comparison(dfMaster['LastName_M'], dfMaster['LastName_EOC'], EOCEC)
dfMaster['LAST NAME Okay?'] = np.where(comparisonLast1 & comparisonLast2 & comparisonLast3 & comparisonLast4, 'Correct', 'Fix')

comparisonMiddle1 = Comparison(dfMaster['MiddleName_BE'], dfMaster['MiddleName_WD'], BEEC & WDEC)
comparisonMiddle2 = Comparison(dfMaster['MiddleName_BE'], dfMaster['MiddleName_EOC'], BEEC & EOCEC)
dfMaster['MIDDLE NAME Okay?'] = np.where(comparisonMiddle1 & comparisonMiddle2, 'Correct', 'Fix')

comparisonPhone1 = Comparison(dfMaster['Phone_M'], dfMaster['Phone_AM'], AMEC)
comparisonPhone2 = Comparison(dfMaster['Phone_M'], dfMaster['Phone_BE'], BEEC)
comparisonPhone3 = Comparison(dfMaster['Phone_M'], dfMaster['Phone_WD'], WDEC)
comparisonPhone4 = Comparison(dfMaster['Phone_M'], dfMaster['Phone_EOC'], EOCEC)
dfMaster['PHONE Okay?'] = np.where(comparisonPhone1 & comparisonPhone2 & comparisonPhone3 & comparisonPhone4, 'Correct', 'Fix')

comparisonEmail1 = Comparison(dfMaster['Email_M'], dfMaster['Email_AM'], AMEC)
comparisonEmail2 = Comparison(dfMaster['Email_M'], dfMaster['Email_BE'], BEEC)
comparisonEmail3 = Comparison(dfMaster['Email_M'], dfMaster['Email_WD'], WDEC)
comparisonEmail4 = Comparison(dfMaster['Email_M'], dfMaster['Email_EOC'], EOCEC)
dfMaster['EMAIL Okay?'] = np.where(comparisonEmail1 & comparisonEmail2 & comparisonEmail3 & comparisonEmail4, 'Correct', 'Fix')

# List of Equivalent Classes that can be compared without changing
dfClassEqui = pd.read_csv('../MasterTrackingFormatting/EquivalentClasses.csv', index_col=0, low_memory=False)
ClassEqui = dfClassEqui.to_dict()['Equivalent'] # Grabs the embedded dictionary
# Turns the Dictionary into a regular expression that replaces only whole words, if not using can ignore this
ClassEqui = {
    f'(^|\s|/|,){Class}($|\s|/|;|,)': f'\\1{Equivalent}\\2'
    for Class, Equivalent in ClassEqui.items()
}

tempdf = pd.DataFrame()
tempdf['Class_M'] = dfMaster['Class_M'].str.upper().replace(ClassEqui, regex=True).astype(str)
tempdf['Class_AM'] = dfMaster['Class_AM'].str.upper().replace(ClassEqui, regex=True).astype(str)
tempdf['Class_BE'] = dfMaster['Class_BE'].str.upper().replace(ClassEqui, regex=True).astype(str)

# Checks if BE abbreviation is within AM and M, if BE doesn't exist, then checks whether all M abbreviations are in AM
comparisonClass1 = CustomComparison(tempdf, RankedSearchIn, 'Class_BE', 'Class_M', BEEC, MOEC)
comparisonClass2 = CustomComparison(tempdf, RankedSearchIn, 'Class_BE', 'Class_AM', BEEC, AMEC)
comparisonClass3 = CustomComparison(tempdf, MInAM, 'Class_M', 'Class_AM', AMEC, ~BEEC) # If BE exists, this will always be true
dfMaster['CLASS Okay?'] = np.where(comparisonClass1 & comparisonClass2 & comparisonClass3, 'Correct', 'Fix')

##If the class is NOT one of these 3: RN NP or PA
##Do not compare, mark as correct
##Otherwise, do the comp as normal

tempdf['Specialty_M'] = dfMaster['Specialty_M'].astype(str).str.upper()
tempdf['Specialty_AM'] = dfMaster['Specialty_AM'].replace(regex='(^|\s|/|,)MS($|\s|/|,)', value='\\1M/S\\2').astype(str).str.upper()
tempdf['Specialty_BE'] = dfMaster['Specialty_BE'].astype(str).str.upper()

# Checks whether we need to compare Specialties, if negated, and used with or logic, will make certain comparisons are correct if Class does not contain one of the 3
SpecialtyCompare = dfMaster.apply(lambda x: ('RN' in x['Class_M']) or ('NP' in x['Class_M']) or ('PA' in x['Class_M']), axis=1)

comparisonSpecialty1 = CustomComparison(tempdf, SearchIn, 'Specialty_BE', 'Specialty_M', BEEC, SpecialtyCompare)
comparisonSpecialty2 = CustomComparison(tempdf, SearchIn, 'Specialty_BE', 'Specialty_AM', BEEC & AMEC, SpecialtyCompare)
comparisonSpecialty3 = CustomComparison(tempdf, MInAM, 'Specialty_M', 'Specialty_AM', AMEC & ~BEEC, SpecialtyCompare) # If BE exists, this will always be true
dfMaster['SPECIALTY Okay?'] = np.where(comparisonSpecialty1 & comparisonSpecialty2 & comparisonSpecialty3, 'Correct', 'Fix')

comparisonDOB1 = Comparison(dfMaster['DOB_M'], dfMaster['DOB_BE'], BEEC)
comparisonDOB2 = Comparison(dfMaster['DOB_M'], dfMaster['DOB_WD'], WDEC)
comparisonDOB3 = Comparison(dfMaster['DOB_M'], dfMaster['DOB_EOC'], EOCEC)
#this part on new chunks, 2nd correct should be fix
dfMaster['DOB Okay?'] = np.where(comparisonDOB1 & comparisonDOB2 & comparisonDOB3, 'Correct', 'Fix')


comparisonGender1 = Comparison(dfMaster['Gender_AM'], dfMaster['Gender_BE'], AMEC & BEEC)
comparisonGender2 = Comparison(dfMaster['Gender_AM'], dfMaster['Gender_EOC'], AMEC & EOCEC)
dfMaster['GENDER Okay?'] = np.where(comparisonGender1 & comparisonGender2, 'Correct', 'Fix')

comparisonAddress1 = Comparison(dfMaster['Address_M'], dfMaster['Address_BE'], BEEC)
comparisonAddress2 = Comparison(dfMaster['Address_M'], dfMaster['Address_WD'], WDEC)
dfMaster['ADDRESS Okay?'] = np.where(comparisonAddress1 & comparisonAddress2, 'Correct', 'Fix')

comparisonCity1 = Comparison(dfMaster['City_M'], dfMaster['City_AM'], AMEC)
comparisonCity2 = Comparison(dfMaster['City_M'], dfMaster['City_BE'], BEEC)
comparisonCity3 = Comparison(dfMaster['City_M'], dfMaster['City_WD'], WDEC)
dfMaster['CITY Okay?'] = np.where(comparisonCity1 & comparisonCity2 & comparisonCity3, 'Correct', 'Fix')

comparisonState1 = Comparison(dfMaster['State_M'], dfMaster['State_AM'], AMEC)
comparisonState2 = Comparison(dfMaster['State_M'], dfMaster['State_BE'], BEEC)
comparisonState3 = Comparison(dfMaster['State_M'], dfMaster['State_WD'], WDEC)
dfMaster['STATE Okay?'] = np.where(comparisonState1 & comparisonState2 & comparisonState3, 'Correct', 'Fix')

comparisonZip1 = Comparison(dfMaster['Zip_M'], dfMaster['Zip_AM'], AMEC)
comparisonZip2 = Comparison(dfMaster['Zip_M'], dfMaster['Zip_BE'], BEEC)
comparisonZip3 = Comparison(dfMaster['Zip_M'], dfMaster['Zip_WD'], WDEC)
dfMaster['ZIP Okay?'] = np.where(comparisonZip1 & comparisonZip2 & comparisonZip3, 'Correct', 'Fix')

tempdf['LicenseState_AM'] = dfMaster['LicenseState_AM'].astype(str)
tempdf['LicenseState_BE'] = dfMaster['LicenseState_BE'].astype(str)
dfMaster['LICENSE STATE Okay?'] = np.where(CustomComparison(tempdf, SearchIn, 'LicenseState_BE', 'LicenseState_AM', BEEC, AMEC), 'Correct', 'Fix')

dfMaster['LICENSE NUMBER Okay?'] = np.where(Comparison(dfMaster['LicenseNumber_BE'], dfMaster['LicenseNumber_EOC'], BEEC) | ~EOCEC, 'Correct', 'Fix')

dfMaster['SSN Okay?'] = np.where(Comparison(dfMaster['SS#_BE'], dfMaster['SS#_WD'], BEEC) | ~WDEC, 'Correct', 'Fix')

# Determine Rows Correct
dfMaster['RowCorrect?'] = np.where(dfMaster['MOBILIZE ID Okay?'] == 'Fix','', (
                        np.where(dfMaster['WORKDAY ID Okay?'] == 'Fix','', (
                        np.where(dfMaster['FIRST NAME Okay?'] == 'Fix','', (
                        np.where(dfMaster['LAST NAME Okay?'] == 'Fix','', (
                        np.where(dfMaster['MIDDLE NAME Okay?'] == 'Fix','', (
                        np.where(dfMaster['PHONE Okay?'] == 'Fix','', (
                        np.where(dfMaster['EMAIL Okay?'] == 'Fix','', (
                        np.where(dfMaster['CLASS Okay?'] == 'Fix','', (
                        np.where(dfMaster['SPECIALTY Okay?'] == 'Fix','', (
                        np.where(dfMaster['DOB Okay?'] == 'Fix','', (
                        np.where(dfMaster['GENDER Okay?'] == 'Fix','', (
                        np.where(dfMaster['ADDRESS Okay?'] == 'Fix','', (
                        np.where(dfMaster['CITY Okay?'] == 'Fix','', (
                        np.where(dfMaster['STATE Okay?'] == 'Fix','', (
                        np.where(dfMaster['ZIP Okay?'] == 'Fix','', (
                        np.where(dfMaster['LICENSE STATE Okay?'] == 'Fix','', (
                        np.where(dfMaster['LICENSE NUMBER Okay?'] == 'Fix','', (
                        np.where(dfMaster['SSN Okay?'] == 'Fix','', 'RowCorrect')))))))))))))))))))))))))))))))))))

# If information matches, fills Final column with info
dfMaster['MOBILIZE ID FINAL'] = np.where(dfMaster['MOBILIZE ID Okay?'] == 'Correct', dfMaster['EID_M'], '')
dfMaster['WORKDAY ID FINAL'] = np.where(dfMaster['WORKDAY ID Okay?'] == 'Correct', dfMaster['WDID_M'], '')
dfMaster['FIRST NAME FINAL'] = np.where(dfMaster['FIRST NAME Okay?'] == 'Correct', dfMaster['FirstName_M'], '')
dfMaster['LAST NAME FINAL'] = np.where(dfMaster['LAST NAME Okay?'] == 'Correct', dfMaster['LastName_M'], '')
dfMaster['MIDDLE NAME FINAL'] = np.where(dfMaster['MIDDLE NAME Okay?'] == 'Correct', np.where(BEEC, dfMaster['MiddleName_BE'], np.where(WDEC, dfMaster['MiddleName_WD'], dfMaster['MiddleName_EOC'])), '')
dfMaster['PHONE FINAL'] = np.where(dfMaster['PHONE Okay?'] == 'Correct', dfMaster['Phone_M'], '')
dfMaster['EMAIL FINAL'] = np.where(dfMaster['EMAIL Okay?'] == 'Correct', dfMaster['Email_M'], '')
dfMaster['CLASS FINAL'] = np.where(dfMaster['CLASS Okay?'] == 'Correct', dfMaster['Class_M'], '')
dfMaster['SPECIALTY FINAL'] = np.where(dfMaster['SPECIALTY Okay?'] == 'Correct', dfMaster['Specialty_M'], '')
dfMaster['DOB FINAL'] = np.where(dfMaster['DOB Okay?'] == 'Correct', dfMaster['DOB_M'], '')
dfMaster['GENDER FINAL'] = np.where(dfMaster['GENDER Okay?'] == 'Correct', np.where(AMEC, dfMaster['Gender_AM'], np.where(BEEC, dfMaster['Gender_BE'], dfMaster['Gender_EOC'])), '')
dfMaster['ADDRESS FINAL'] = np.where(dfMaster['ADDRESS Okay?'] == 'Correct', dfMaster['Address_M'], '')
dfMaster['CITY FINAL'] = np.where(dfMaster['CITY Okay?'] == 'Correct', dfMaster['City_M'], '')
dfMaster['STATE FINAL'] = np.where(dfMaster['STATE Okay?'] == 'Correct', dfMaster['State_M'], '')
dfMaster['ZIP FINAL'] = np.where(dfMaster['ZIP Okay?'] == 'Correct', dfMaster['Zip_M'], '')
dfMaster['LICENSE STATE FINAL'] = np.where(dfMaster['LICENSE STATE Okay?'] == 'Correct', np.where(AMEC, dfMaster['LicenseState_AM'], dfMaster['LicenseState_BE']), '')
dfMaster['LICENSE NUMBER FINAL'] = np.where(dfMaster['LICENSE NUMBER Okay?'] == 'Correct', np.where(BEEC, dfMaster['LicenseNumber_BE'], dfMaster['LicenseNumber_EOC']), '')
dfMaster['SSN FINAL'] = np.where(dfMaster['SSN Okay?'] == 'Correct', np.where(BEEC, dfMaster['SS#_BE'], dfMaster['SS#_WD']), '')


dfMaster['Email'] = dfMaster['Email_M']
dfMaster = dfMaster[['Profile Exists_AM', 'Profile Exists_BE', 'Profile Exists_WD', 'Profile Exists_EOC', 'EffectiveDate_WD',
                     'Email', 'EID_M', 'EID_AM', 'MOBILIZE ID FINAL', 'MOBILIZE ID Okay?',
                     'WDID_M','WDID_AM', 'WDID_WD', 'WORKDAY ID FINAL', 'WORKDAY ID Okay?',
                     'FirstName_M', 'FirstName_AM', 'FirstName_BE', 'FirstName_WD', 'FirstName_EOC', 'FIRST NAME FINAL', 'FIRST NAME Okay?',
                     'LastName_M', 'LastName_AM', 'LastName_BE', 'LastName_WD', 'LastName_EOC', 'LAST NAME FINAL', 'LAST NAME Okay?',
                     'MiddleName_BE', 'MiddleName_WD', 'MiddleName_EOC', 'MIDDLE NAME FINAL', 'MIDDLE NAME Okay?',
                     'Phone_M', 'Phone_AM', 'Phone_BE', 'Phone_WD', 'Phone_EOC', 'PHONE FINAL', 'PHONE Okay?',
                     'Email_M', 'Email_AM', 'Email_BE', 'Email_WD', 'Email_EOC', 'EMAIL FINAL', 'EMAIL Okay?',
                     'Class_M', 'Class_AM', 'Class_BE', 'Class_EOC', 'CLASS FINAL', 'CLASS Okay?',
                     'Specialty_M', 'Specialty_AM', 'Specialty_BE', 'SPECIALTY FINAL', 'SPECIALTY Okay?',
                     'DOB_M', 'DOB_BE', 'DOB_WD', 'DOB_EOC', 'DOB FINAL', 'DOB Okay?',
                     'Gender_AM', 'Gender_BE', 'Gender_EOC', 'GENDER FINAL', 'GENDER Okay?',
                     'Address_M', 'Address_BE', 'Address_WD', 'ADDRESS FINAL', 'ADDRESS Okay?',
                     'City_M', 'City_AM', 'City_BE', 'City_WD', 'CITY FINAL', 'CITY Okay?',
                     'State_M', 'State_AM', 'State_BE', 'State_WD', 'STATE FINAL', 'STATE Okay?',
                     'Zip_M', 'Zip_AM', 'Zip_BE', 'Zip_WD', 'ZIP FINAL', 'ZIP Okay?',
                     'LicenseState_AM', 'LicenseState_BE', 'LICENSE STATE FINAL', 'LICENSE STATE Okay?',
                     'LicenseNumber_BE', 'LicenseNumber_EOC', 'LICENSE NUMBER FINAL', 'LICENSE NUMBER Okay?', 
                     'SS#_BE', 'SS#_WD', 'SSN FINAL', 'SSN Okay?',
                     'AlertMedia Updated', 'Mobilize Updated', 'Backend Updated', 'WebEOC Updated',
                     'Workday Updated', 'Completed By', 'DATE COMPLETED', 'Notes', 'RowCorrect?', 'ProfileActive_M']]

#print(dfMaster.info(verbose=True))

dfMaster.to_csv('../MasterTracking_Data/PostFormatting-Comparison.csv')
print('Generated File PostFormatting-Comparison')
