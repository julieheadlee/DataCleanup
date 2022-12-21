import pandas as pd
import numpy as np

# 4.5 Creates Import for Alert Media

dfAM = pd.read_csv('../MasterTracking_Data/3Catagories/Incorrect.csv', dtype=str, low_memory=False)

dfAM = dfAM[dfAM['Profile Exists_AM'] == 'True']

BEE = dfAM['Profile Exists_BE'].astype(bool)
WDE = dfAM['Profile Exists_WD'].astype(bool)
EOCE = dfAM['Profile Exists_EOC'].astype(bool)

# IMPORTANT! Columns must be named from the list of column names in an AM import template
dfImport = pd.DataFrame(columns=['first_name','last_name','email','mobile_phone','city','state','zipcode','gender','workday_id','employee_id','license_state'])

dfImport['employee_id'] = np.where(dfAM['EID_AM'].isnull(), dfAM['EID_M'], dfAM['EID_AM'])
dfImport['workday_id'] = np.where(dfAM['WDID_AM'].isnull() & (dfAM['WDID_M'] == dfAM['WDID_WD']), dfAM['WDID_M'], dfAM['WDID_AM'])

First1 = np.where((dfAM['FirstName_M'] == dfAM['FirstName_BE']) | ~BEE, True, False)
First2 = np.where((dfAM['FirstName_M'] == dfAM['FirstName_WD']) | ~WDE, True, False)
First3 = np.where((dfAM['FirstName_M'] == dfAM['FirstName_EOC']) | ~EOCE, True, False)
dfImport['first_name'] = np.where(First1 & First2 & First3 & dfAM['FirstName_AM'].isnull() & (BEE | WDE | EOCE), dfAM['FirstName_M'], dfAM['FirstName_AM'])

Last1 = np.where((dfAM['LastName_M'] == dfAM['LastName_BE']) | ~BEE, True, False)
Last2 = np.where((dfAM['LastName_M'] == dfAM['LastName_WD']) | ~WDE, True, False)
Last3 = np.where((dfAM['LastName_M'] == dfAM['LastName_EOC']) | ~EOCE, True, False)
dfImport['last_name'] = np.where(Last1 & Last2 & Last3 & dfAM['LastName_AM'].isnull() & (BEE | WDE | EOCE), dfAM['LastName_M'], dfAM['LastName_AM'])

Phone1 = np.where((dfAM['Phone_M'] == dfAM['Phone_BE']) | ~BEE, True, False)
Phone2 = np.where((dfAM['Phone_M'] == dfAM['Phone_WD']) | ~WDE, True, False)
Phone3 = np.where((dfAM['Phone_M'] == dfAM['Phone_EOC']) | ~EOCE, True, False)
dfImport['mobile_phone'] = np.where(Phone1 & Phone2 & Phone3 & dfAM['Phone_AM'].isnull() & (BEE | WDE | EOCE), dfAM['Phone_M'], dfAM['Phone_AM'])

Email1 = np.where((dfAM['Email_M'] == dfAM['Email_BE']) | ~BEE, True, False)
Email2 = np.where((dfAM['Email_M'] == dfAM['Email_WD']) | ~WDE, True, False)
Email3 = np.where((dfAM['Email_M'] == dfAM['Email_EOC']) | ~EOCE, True, False)
dfImport['email'] = np.where(Email1 & Email2 & Email3 & dfAM['Email_AM'].isnull() & (BEE | WDE | EOCE), dfAM['Email_M'], dfAM['Email_AM'])

dfImport['gender'] = np.where(dfAM['Gender_AM'].isnull() & (dfAM['Gender_BE'] == dfAM['Gender_EOC']), dfAM['Gender_BE'], dfAM['Gender_AM'])

City1 = np.where((dfAM['City_M'] == dfAM['City_BE']) | ~BEE, True, False)
City2 = np.where((dfAM['City_M'] == dfAM['City_WD']) | ~WDE, True, False)
dfImport['city'] = np.where(City1 & City2 & (BEE | WDE), dfAM['City_M'], dfAM['City_AM']) # & dfAM['City_AM'].isnull() Normally include this, this time however we are not

State1 = np.where((dfAM['State_M'] == dfAM['State_BE']) | ~BEE, True, False)
State2 = np.where((dfAM['State_M'] == dfAM['State_WD']) | ~WDE, True, False)
dfImport['state'] = np.where(State1 & State2 & dfAM['State_AM'].isnull() & (BEE | WDE), dfAM['State_M'], dfAM['State_AM'])

Zip1 = np.where((dfAM['Zip_M'] == dfAM['Zip_BE']) | ~BEE, True, False)
Zip2 = np.where((dfAM['Zip_M'] == dfAM['Zip_WD']) | ~WDE, True, False)
dfImport['zipcode'] = np.where(Zip1 & Zip2 & dfAM['Zip_AM'].isnull() & (BEE | WDE), dfAM['Zip_M'], dfAM['Zip_AM'])

dfImport['license_state'] = np.where(dfAM['LicenseState_AM'].isnull(), dfAM['LicenseState_BE'], dfAM['LicenseState_AM'])

dfImport.to_csv('../MasterTracking_Data/AMBulkImport.csv', index=False)
print('AM bulk import generated')
