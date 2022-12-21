import pandas as pd
import numpy as np
import os
import sys

# 2 Combines sources from different databases into single file.

# If set to true, will print out extra information, slows processing down
DEBUG = False

sources = '12.21 Sources'

#merging mobilize with AM
dfM = pd.read_csv(f'../MasterTracking_Data/{sources}/Mobilize.csv', dtype=str, low_memory=False)
dfAM = pd.read_csv(f'../MasterTracking_Data/{sources}/AM.csv', dtype=str, low_memory=False)
dfBE = pd.read_csv(f'../MasterTracking_Data/{sources}/Backend_Combined.csv', dtype=str, low_memory=False)
dfWD = pd.read_csv(f'../MasterTracking_Data/{sources}/Workday.csv', dtype=str, low_memory=False)
dfEOC = pd.read_csv(f'../MasterTracking_Data/{sources}/webEOC.csv', dtype=str, low_memory=False)

if DEBUG:
    print("Mobilize\n", dfM.info(verbose=True))
    print("Alert Media\n", dfAM.info(verbose=True))
    print("Backend\n", dfBE.info(verbose=True))
    print("Workday\n", dfWD.info(verbose=True))
    print("WebEOC\n", dfEOC.info(verbose=True))

# Rename columns
dfM.rename(columns={'First Name':'FirstName_M', 'Last Name': 'LastName_M', 'Is Profile Active?': 'ProfileActive_M', 'Phone': 'Phone_M',
                    'Email Address': 'Email_M', 'Address 1': 'Address_M', 'City': 'City_M', 'State': 'State_M',
                    'ZIP': 'Zip_M', 'Profile ID': 'EID_M', 'WorkdayId': 'WDID_M', 'Class': 'Class_M', 'Area': 'Specialty_M',
                    'Birth Date': 'DOB_M'}, inplace=True)
dfM = dfM[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M', 'ProfileActive_M']]

dfAM.rename(columns={'first_name': 'FirstName_AM', 'last_name':'LastName_AM','email': 'Email_AM', 'mobile_phone':'Phone_AM',
                     'city': 'City_AM', 'state': 'State_AM', 'zipcode': 'Zip_AM', 'gender': 'Gender_AM',
                     'employee_id': 'EID_AM', 'workday_id': 'WDID_AM', 'classification': 'Class_AM',
                     'license_state': 'LicenseState_AM', 'area': 'Specialty_AM'}, inplace=True)
dfAM = dfAM[['FirstName_AM', 'LastName_AM', 'Email_AM', 'Phone_AM', 'City_AM', 'State_AM', 'Zip_AM', 'Gender_AM', 'WDID_AM', 'EID_AM', 'Class_AM', 'LicenseState_AM', 'Specialty_AM']]

dfBE.rename(columns={'First Name_be': 'FirstName_BE', 'Middle Name_be': 'MiddleName_BE', 'Last Name_be': 'LastName_BE',
                     'Email Address_be': 'Email_BE', 'Phone Number_be': 'Phone_BE', 'Gender_be': 'Gender_BE', 'Date of Birth_be': 'DOB_BE',
                     'SS#_be': 'SS#_BE', 'Class_be': 'Class_BE', 'Clinical Area of Specialty_be': 'Specialty_BE',
                     'Address_be': 'Address_BE', 'City of Residency_be': 'City_BE', 'State of Residency_be': 'State_BE', 'Zip Code_be': 'Zip_BE',
                     'State(s) Medical License is Valid In_be': 'LicenseState_BE', 'Professional License Number_be': 'LicenseNumber_BE'},
                     inplace=True)

dfBE = dfBE[['Activation Date', 'FirstName_BE', 'MiddleName_BE', 'LastName_BE', 'Email_BE', 'Phone_BE', 'Gender_BE', 'DOB_BE', 'SS#_BE', 'Specialty_BE', 'Class_BE', 'Address_BE', 'City_BE', 'State_BE', 'Zip_BE', 'LicenseState_BE', 'LicenseNumber_BE']]

dfWD.rename(columns={'Employee ID': 'WDID_WD', 'Social Security Number - Formatted': 'SS#_WD', 'Date of Birth': 'DOB_WD',
                     'Primary Home Address': 'Address_WD', 'Primary Home Address - City': 'City_WD',
                     'Primary Home Address - State': 'State_WD', 'Primary Home Address - Postal Code': 'Zip_WD', 'Legal First Name': 'FirstName_WD',
                     'Legal Name - Middle Name': 'MiddleName_WD', 'Legal Name - Last Name': 'LastName_WD', 'Phone - Primary Home': 'Phone_WD',
                     'Email - Primary Work or Primary Home': 'Email_WD', 'Address Effective Date': 'EffectiveDate_WD'}, inplace=True)

dfWD = dfWD[['WDID_WD', 'SS#_WD', 'DOB_WD', 'Address_WD', 'City_WD', 'State_WD', 'Zip_WD', 'FirstName_WD', 'MiddleName_WD', 'LastName_WD', 'Phone_WD', 'Email_WD', 'EffectiveDate_WD', 'Address Line 2']]


dfEOC.rename(columns={'Class': 'Class_EOC', 'Phone Number': 'Phone_EOC', 'Last Name': 'LastName_EOC', 'First Name': 'FirstName_EOC',
                      'Middle Name': 'MiddleName_EOC', 'Gender': 'Gender_EOC', 'Email': 'Email_EOC', 'Date of Birth': 'DOB_EOC',
                      'Medical/Nursing License Number': 'LicenseNumber_EOC'}, inplace=True)
dfEOC = dfEOC[['Class_EOC', 'Phone_EOC', 'LastName_EOC', 'FirstName_EOC', 'MiddleName_EOC', 'Gender_EOC', 'Email_EOC', 'DOB_EOC', 'LicenseNumber_EOC']]

# Removes duplicate Database Entries
dfBE['Activation Date'] = dfBE['Activation Date'].astype('datetime64[ns]')
dfBE.sort_values(by=['Activation Date'], ascending=False, inplace=True)
dfBE.drop_duplicates(subset=['Email_BE'], keep='first', inplace=True)

# Make emails comparable
dfM['Email_M'] = dfM['Email_M'].str.lower()
dfAM['Email_AM'] = dfAM['Email_AM'].str.lower()
dfBE['Email_BE'] = dfBE['Email_BE'].str.lower()
dfWD['Email_WD'] = dfWD['Email_WD'].str.lower()
dfEOC['Email_EOC'] = dfEOC['Email_EOC'].str.lower()

# Make phone numbers comparable
def Phone_Formatting(s):
    return s.str.replace('|'.join(['-','\.','\)','\(',' ',"'",'\+1']), '', regex=True).str.slice(0, 10, 1)

dfM['Phone_M'] = Phone_Formatting(dfM['Phone_M'])
dfAM['Phone_AM'] = Phone_Formatting(dfAM['Phone_AM'])
dfBE['Phone_BE'] = Phone_Formatting(dfBE['Phone_BE'])
dfWD['Phone_WD'] = Phone_Formatting(dfWD['Phone_WD'])
dfEOC['Phone_EOC'] = Phone_Formatting(dfEOC['Phone_EOC'])

# Merge Databases
# AM merges
AMmergeEM = pd.merge(dfM, dfAM.loc[lambda x: x['Email_AM'].notna()], left_on='Email_M', right_on='Email_AM', how='left')
MEmailNA = AMmergeEM.loc[lambda x: x['Email_AM'].isna()]
MEmailNA = MEmailNA[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M']]

AMmergePN = pd.merge(MEmailNA, dfAM.loc[lambda x: x['Phone_AM'].notna()], left_on='Phone_M', right_on='Phone_AM', how='left')
MPhoneNA = AMmergePN.loc[lambda x: x['Phone_AM'].isna()]
MPhoneNA = MPhoneNA[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M']]

AMmergeEID = pd.merge(MPhoneNA, dfAM.loc[lambda x: x['EID_AM'].notna()], left_on='EID_M', right_on='EID_AM', how='left')
MEIDNA = AMmergeEID.loc[lambda x: x['EID_AM'].isna()]
MEIDNA = MEIDNA[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M']]

AMmergeWDID = pd.merge(MEIDNA, dfAM.loc[lambda x: x['WDID_AM'].notna()], left_on='WDID_M', right_on='WDID_AM', how='left')
MWDIDNA = AMmergeWDID.loc[lambda x: x['WDID_AM'].isna()]
MWDIDNA = MWDIDNA[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M']]

# Combine AM merges
AMmergeEM = AMmergeEM.loc[lambda x: x['Email_AM'].notna()]
AMmergePN = AMmergePN.loc[lambda x: x['Phone_AM'].notna()]
AMmergeEID = AMmergeEID.loc[lambda x: x['EID_AM'].notna()]
AMmergeWDID = AMmergeWDID.loc[lambda x: x['WDID_AM'].notna()]
AMmerge = pd.concat([AMmergeEM, AMmergePN, AMmergeEID, AMmergeWDID, MWDIDNA])

# BE merges
BEmergeEM = pd.merge(AMmerge, dfBE.loc[lambda x: x['Email_BE'].notna()], left_on='Email_M', right_on='Email_BE', how='left')
AMEmailNA = BEmergeEM.loc[lambda x: x['Email_BE'].isna()]
AMEmailNA = AMEmailNA[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M', 'ProfileActive_M',
                        'FirstName_AM', 'LastName_AM', 'Email_AM', 'Phone_AM', 'City_AM', 'State_AM', 'Zip_AM', 'Gender_AM', 'WDID_AM', 'EID_AM', 'Class_AM', 'LicenseState_AM', 'Specialty_AM']]

BEmergePN = pd.merge(AMEmailNA, dfBE.loc[lambda x: x['Phone_BE'].notna()], left_on='Phone_M', right_on='Phone_BE', how='left')
AMPhoneNA = BEmergePN.loc[lambda x: x['Phone_BE'].isna()]
AMPhoneNA = AMPhoneNA[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M', 'ProfileActive_M',
                        'FirstName_AM', 'LastName_AM', 'Email_AM', 'Phone_AM', 'City_AM', 'State_AM', 'Zip_AM', 'Gender_AM', 'WDID_AM', 'EID_AM', 'Class_AM', 'LicenseState_AM', 'Specialty_AM',]]

# Combine BE merges
BEmergeEM = BEmergeEM.loc[lambda x: x['Email_BE'].notna()]
BEmergePN = BEmergePN.loc[lambda x: x['Phone_BE'].notna()]
BEmerge = pd.concat([BEmergeEM, BEmergePN, AMPhoneNA])

# WD merges
WDmergeEM = pd.merge(BEmerge, dfWD.loc[lambda x: x['Email_WD'].notna()], left_on='Email_M', right_on='Email_WD', how='left')
BEEmailNA = WDmergeEM.loc[lambda x: x['Email_WD'].isna()]
BEEmailNA = BEEmailNA[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M', 'ProfileActive_M',
                        'FirstName_AM', 'LastName_AM', 'Email_AM', 'Phone_AM', 'City_AM', 'State_AM', 'Zip_AM', 'Gender_AM', 'WDID_AM', 'EID_AM', 'Class_AM', 'LicenseState_AM', 'Specialty_AM',
                        'Activation Date', 'FirstName_BE', 'MiddleName_BE', 'LastName_BE', 'Email_BE', 'Phone_BE', 'Gender_BE', 'DOB_BE', 'SS#_BE', 'Specialty_BE', 'Class_BE', 'Address_BE', 'City_BE', 'State_BE', 'Zip_BE', 'LicenseState_BE', 'LicenseNumber_BE']]

WDmergePN = pd.merge(BEEmailNA, dfWD.loc[lambda x: x['Phone_WD'].notna()], left_on='Phone_M', right_on='Phone_WD', how='left')
BEPhoneNA = WDmergePN.loc[lambda x: x['Phone_WD'].isna()]
BEPhoneNA = BEPhoneNA[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M', 'ProfileActive_M',
                        'FirstName_AM', 'LastName_AM', 'Email_AM', 'Phone_AM', 'City_AM', 'State_AM', 'Zip_AM', 'Gender_AM', 'WDID_AM', 'EID_AM', 'Class_AM', 'LicenseState_AM', 'Specialty_AM',
                        'Activation Date', 'FirstName_BE', 'MiddleName_BE', 'LastName_BE', 'Email_BE', 'Phone_BE', 'Gender_BE', 'DOB_BE', 'SS#_BE', 'Specialty_BE', 'Class_BE', 'Address_BE', 'City_BE', 'State_BE', 'Zip_BE', 'LicenseState_BE', 'LicenseNumber_BE']]

WDmergeWDID = pd.merge(BEPhoneNA, dfWD.loc[lambda x: x['WDID_WD'].notna()], left_on='WDID_M', right_on='WDID_WD', how='left')
BEWDIDNA = WDmergeWDID.loc[lambda x: x['WDID_WD'].isna()]
BEWDIDNA = BEWDIDNA[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M', 'ProfileActive_M',
                    'FirstName_AM', 'LastName_AM', 'Email_AM', 'Phone_AM', 'City_AM', 'State_AM', 'Zip_AM', 'Gender_AM', 'WDID_AM', 'EID_AM', 'Class_AM', 'LicenseState_AM', 'Specialty_AM',
                    'Activation Date', 'FirstName_BE', 'MiddleName_BE', 'LastName_BE', 'Email_BE', 'Phone_BE', 'Gender_BE', 'DOB_BE', 'SS#_BE', 'Specialty_BE', 'Class_BE', 'Address_BE', 'City_BE', 'State_BE', 'Zip_BE', 'LicenseState_BE', 'LicenseNumber_BE']]

# Combine WD merges
WDmergeEM = WDmergeEM.loc[lambda x: x['Email_WD'].notna()]
WDmergePN = WDmergePN.loc[lambda x: x['Phone_WD'].notna()]
WDmergeWDID = WDmergeWDID.loc[lambda x: x['WDID_WD'].notna()]
WDmerge = pd.concat([WDmergeEM, WDmergePN, WDmergeWDID, BEWDIDNA])

# EOC merges
EOCmergeEM = pd.merge(WDmerge, dfEOC.loc[lambda x: x['Email_EOC'].notna()], left_on='Email_M', right_on='Email_EOC', how='left')
WDEmailNA = EOCmergeEM.loc[lambda x: x['Email_EOC'].isna()]
WDEmailNA = WDEmailNA[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M', 'ProfileActive_M',
                        'FirstName_AM', 'LastName_AM', 'Email_AM', 'Phone_AM', 'City_AM', 'State_AM', 'Zip_AM', 'Gender_AM', 'WDID_AM', 'EID_AM', 'Class_AM', 'LicenseState_AM', 'Specialty_AM',
                        'Activation Date', 'FirstName_BE', 'MiddleName_BE', 'LastName_BE', 'Email_BE', 'Phone_BE', 'Gender_BE', 'DOB_BE', 'SS#_BE', 'Specialty_BE', 'Class_BE', 'Address_BE', 'City_BE', 'State_BE', 'Zip_BE', 'LicenseState_BE', 'LicenseNumber_BE',
                        'WDID_WD', 'SS#_WD', 'DOB_WD', 'Address_WD', 'City_WD', 'State_WD', 'Zip_WD', 'FirstName_WD', 'MiddleName_WD', 'LastName_WD', 'Phone_WD', 'Email_WD', 'EffectiveDate_WD', 'Address Line 2']]

EOCmergePN = pd.merge(WDEmailNA, dfEOC.loc[lambda x: x['Phone_EOC'].notna()], left_on='Phone_M', right_on='Phone_EOC', how='left')
WDPhoneNA = EOCmergePN.loc[lambda x: x['Phone_EOC'].isna()]
WDPhoneNA = WDPhoneNA[['FirstName_M', 'LastName_M', 'Phone_M', 'Email_M', 'Class_M', 'Specialty_M', 'Address_M', 'City_M', 'State_M', 'Zip_M', 'EID_M', 'WDID_M', 'DOB_M', 'ProfileActive_M',
                        'FirstName_AM', 'LastName_AM', 'Email_AM', 'Phone_AM', 'City_AM', 'State_AM', 'Zip_AM', 'Gender_AM', 'WDID_AM', 'EID_AM', 'Class_AM', 'LicenseState_AM', 'Specialty_AM',
                        'Activation Date', 'FirstName_BE', 'MiddleName_BE', 'LastName_BE', 'Email_BE', 'Phone_BE', 'Gender_BE', 'DOB_BE', 'SS#_BE', 'Specialty_BE', 'Class_BE', 'Address_BE', 'City_BE', 'State_BE', 'Zip_BE', 'LicenseState_BE', 'LicenseNumber_BE',
                        'WDID_WD', 'SS#_WD', 'DOB_WD', 'Address_WD', 'City_WD', 'State_WD', 'Zip_WD', 'FirstName_WD', 'MiddleName_WD', 'LastName_WD', 'Phone_WD', 'Email_WD', 'EffectiveDate_WD', 'Address Line 2']]

# Combine EOC merges
EOCmergeEM = EOCmergeEM.loc[lambda x: x['Email_EOC'].notna()]
EOCmergePN = EOCmergePN.loc[lambda x: x['Phone_EOC'].notna()]
mergedEmail_df = pd.concat([EOCmergeEM, EOCmergePN, WDPhoneNA])

if DEBUG:
    print(len(dfM.axes[0]))
    print(len(AMmerge.axes[0]))
    print(len(BEmerge.axes[0]))
    print(len(WDmerge.axes[0]))
    print(len(mergedEmail_df.axes[0]))
    AMmerge.to_csv('../MasterTracking_Data/Master Tracking w AM.csv')
    BEmerge.to_csv('../MasterTracking_Data/Master Tracking w Backend.csv')
    WDmerge.to_csv('../MasterTracking_Data/Master Tracking w Workday.csv')
    mergedEmail_df.to_csv('../MasterTracking_Data/Master Tracking w WebEOC.csv')
    print("Combined\n", mergedEmail_df.info(verbose=True))

# Make activation date, an actual date and sort newest to oldest
mergedEmail_df['Activation Date'] = mergedEmail_df['Activation Date'].astype('datetime64[ns]')
mergedEmail_df.sort_values(by=['Activation Date'], ascending=False, inplace=True)

# Drop rows based on Mobilize ID
mergedEmail_df.drop_duplicates(subset=['EID_M'], keep='first', inplace=True)

if DEBUG:
    print("Sorted\n", mergedEmail_df.info(verbose=True))
    mergedEmail_df.to_csv('../MasterTracking_Data/Master Tracking Sorted.csv')

# Throw away extraneous columns
mergedEmail_df['AlertMedia Updated'] = np.NaN
mergedEmail_df['Mobilize Updated'] = np.NaN
mergedEmail_df['Backend Updated'] = np.NaN
mergedEmail_df['WebEOC Updated'] = np.NaN
mergedEmail_df['Workday Updated'] = np.NaN
mergedEmail_df['Completed By'] = np.NaN
mergedEmail_df['DATE COMPLETED'] = np.NaN
mergedEmail_df['Notes'] = np.NaN

mergedEmail_df = mergedEmail_df[['EID_M', 'EID_AM',
                                 'WDID_M','WDID_AM', 'WDID_WD',
                                 'FirstName_M', 'FirstName_AM', 'FirstName_BE', 'FirstName_WD', 'FirstName_EOC',
                                 'LastName_M', 'LastName_AM', 'LastName_BE', 'LastName_WD', 'LastName_EOC',
                                 'MiddleName_BE', 'MiddleName_WD', 'MiddleName_EOC',
                                 'Phone_M', 'Phone_AM', 'Phone_BE', 'Phone_WD', 'Phone_EOC',
                                 'Email_M', 'Email_AM', 'Email_BE', 'Email_WD', 'Email_EOC',
                                 'Class_M', 'Class_AM', 'Class_BE', 'Class_EOC',
                                 'Specialty_M', 'Specialty_AM', 'Specialty_BE',
                                 'DOB_M', 'DOB_BE', 'DOB_WD', 'DOB_EOC',
                                 'Gender_AM', 'Gender_BE', 'Gender_EOC',
                                 'Address_M', 'Address_BE', 'Address_WD',
                                 'City_M', 'City_AM', 'City_BE', 'City_WD',
                                 'State_M', 'State_AM', 'State_BE', 'State_WD',
                                 'Zip_M', 'Zip_AM', 'Zip_BE', 'Zip_WD',
                                 'LicenseState_AM', 'LicenseState_BE',
                                 'LicenseNumber_BE', 'LicenseNumber_EOC',
                                 'SS#_BE', 'SS#_WD',
                                 'AlertMedia Updated', 'Mobilize Updated', 'Backend Updated', 'WebEOC Updated',
                                 'Workday Updated', 'Completed By', 'DATE COMPLETED', 'Notes', 'EffectiveDate_WD', 'Address Line 2', 'ProfileActive_M']]

if DEBUG:
    print("Trimmed\n", mergedEmail_df.info(verbose=True))

# Generate File
mergedEmail_df.to_csv('../MasterTracking_Data/Master Tracking Trimmed.csv')
print('Master Tracking Trimmed generated')
