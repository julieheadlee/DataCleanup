import pandas as pd
import numpy as np

# 5 Separates file based on what needs to be done with them.

dfMaster = pd.read_csv('../MasterTracking_Data/PostFormatting-Comparison.csv', dtype=str, low_memory=False, )
#dfInactive = pd.read_csv('../MasterTracking_Data/Inactive Bump.csv', dtype={'ProfileID':str}, low_memory=False)

dfMaster.drop('Unnamed: 0', axis=1, inplace=True)

#adding in 'Is Profile Active?' column to master sheet
print(dfMaster.info(verbose=True))
print(dfMaster['ProfileActive_M'].dtype)

m = dfMaster['ProfileActive_M'] != 'FALSE'
ATrue, BFalse = dfMaster[m], dfMaster[~m]

print(ATrue)
print(BFalse)

BFalse.to_csv('../MasterTracking_Data/3Catagories/False.csv')
#ATrue.to_csv('../MasterTracking_Data/3Catagories/True.csv')

# Adding code to reformat False.csv for chunking, and add needed check columns
inactives_db = BFalse[['Email', 'EID_M', 'EID_AM', 'Profile Exists_BE', 'Profile Exists_WD', 'FirstName_M', 'LastName_M', 'Phone_M', 'Class_M', 'SSN FINAL', 'ProfileActive_M']]
inactives_db.insert(loc=5, column="In Mobilize under another ID?", value="")
inactives_db.insert(loc=6, column="In Alert Media under name and/or email?", value="")
inactives_db.insert(loc=7, column="In backend and/or Workday?", value="")
inactives_db.insert(loc=8, column="Need to reactivate?", value="")
inactives_db.insert(loc=9, column="Completed Date", value="")
inactives_db.insert(loc=10, column="Completed by", value="")

inactives_db.to_csv('../MasterTracking_Data/3Catagories/MobilizeFalse.csv')

n = ATrue['RowCorrect?'] == 'RowCorrect'
cCorrect, dIncorrect = ATrue[n], ATrue[~n]
cCorrect.to_csv('../MasterTracking_Data/3Catagories/RowCorrect.csv')
dIncorrect.to_csv('../MasterTracking_Data/3Catagories/Incorrect.csv')
print('Files Generated')
