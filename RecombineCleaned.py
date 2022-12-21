import pandas as pd
import numpy as np
import os
import sys
#install XlsxWriter

# 8 Metrics

from datetime import datetime, timedelta

from sympy import difference_delta

path = '../CleanUpMetrics/'
os.chdir(path)

ACTIVE = True
INACTIVE = True
DELETE = True

DATE_OVERRIDE = False
if DATE_OVERRIDE:
    date = '2022.03.27'
else:
    date = f'{datetime.now().strftime("%Y.%m.%d")}'

if ACTIVE:
    dfActive = pd.DataFrame(columns=['MOBILIZE ID FINAL', 'WORKDAY ID FINAL', 'FIRST NAME FINAL', 'LAST NAME FINAL',
                                    'MIDDLE NAME FINAL', 'PHONE FINAL', 'EMAIL FINAL', 'CLASS FINAL', 'SPECIALTY FINAL',
                                    'DOB FINAL', 'GENDER FINAL', 'ADDRESS FINAL', 'CITY FINAL', 'STATE FINAL', 'ZIP FINAL',
                                    'LICENSE STATE FINAL', 'LICENSE NUMBER FINAL', 'SSN FINAL', 'AlertMedia Updated', 'Mobilize Updated',
                                    'Backend Updated', 'WebEOC Updated', 'Workday Updated', 'Completed By', 'DATE COMPLETED', 'Notes'])

if INACTIVE:
    dfInactive = pd.DataFrame(columns=['Email', 'EID_M', 'EID_AM', 'Profile Exists_BE', 'Profile Exists_WD',
                                        'In Mobilize under another ID?', 'In Alert Media under name and/or email?',
                                        'In backend and/or Workday?', 'Need to reactivate?', 'Completed Date', 'Completed by',
                                        'FirstName_M', 'LastName_M', 'Phone_M', 'Class_M', 'SSN FINAL', 'Is Profile Active?'])

if DELETE:
    dfDelete = pd.DataFrame(columns=['First Name', 'Last Name', 'Phone', 'Email', 'Profile ID', 'WorkdayID', 'Created Date', 'Modified Date',
                                    'Delete?', 'Completed By', 'Completed Date', 'Notes'])

if ACTIVE:
    active_path = f'Active {date}'
if INACTIVE:
    inactive_path = f'Inactive {date}'
if DELETE:
    delete_path = f'Delete {date}'

if ACTIVE:
    activechunks = os.listdir(active_path)
if INACTIVE:
    inactivechunks = os.listdir(inactive_path)
if DELETE:
    deletechunks = os.listdir(delete_path)

if  ACTIVE:
    active_df = pd.DataFrame(columns=['MOBILIZE ID FINAL', 'WORKDAY ID FINAL', 'FIRST NAME FINAL', 'LAST NAME FINAL',
                                    'MIDDLE NAME FINAL', 'PHONE FINAL', 'EMAIL FINAL', 'CLASS FINAL', 'SPECIALTY FINAL',
                                    'DOB FINAL', 'GENDER FINAL', 'ADDRESS FINAL', 'CITY FINAL', 'STATE FINAL', 'ZIP FINAL',
                                    'LICENSE STATE FINAL', 'LICENSE NUMBER FINAL', 'SSN FINAL', 'AlertMedia Updated', 'Mobilize Updated',
                                    'Backend Updated', 'WebEOC Updated', 'Workday Updated', 'Completed By', 'DATE COMPLETED', 'Notes'])

if INACTIVE:
    inactive_df = pd.DataFrame(columns=['Email', 'EID_M', 'EID_AM', 'Profile Exists_BE', 'Profile Exists_WD',
                                        'In Mobilize under another ID?', 'In Alert Media under name and/or email?',
                                        'In backend and/or Workday?', 'Need to reactivate?', 'Completed Date', 'Completed by',
                                        'FirstName_M', 'LastName_M', 'Phone_M', 'Class_M', 'SSN FINAL', 'Is Profile Active?'])

if DELETE:
    delete_df = pd.DataFrame(columns=['First Name', 'Last Name', 'Phone', 'Email', 'Profile ID', 'WorkdayID', 'Created Date', 'Modified Date',
                                    'Delete?', 'Completed By', 'Completed Date', 'Notes'])

holding_active = pd.DataFrame()
holding_inactive = pd.DataFrame()
holding_delete = pd.DataFrame()

if ACTIVE:
    os.chdir(active_path)

    for f in activechunks:
        holding_active = pd.read_excel(f)
        #append all the columns
        active_df = holding_active[['MOBILIZE ID FINAL', 'WORKDAY ID FINAL', 'FIRST NAME FINAL', 'LAST NAME FINAL',
                        'MIDDLE NAME FINAL', 'PHONE FINAL', 'EMAIL FINAL', 'CLASS FINAL', 'SPECIALTY FINAL',
                        'DOB FINAL', 'GENDER FINAL', 'ADDRESS FINAL', 'CITY FINAL', 'STATE FINAL', 'ZIP FINAL',
                        'LICENSE STATE FINAL', 'LICENSE NUMBER FINAL', 'SSN FINAL', 'AlertMedia Updated', 'Mobilize Updated',
                        'Backend Updated', 'WebEOC Updated', 'Workday Updated', 'Completed By', 'DATE COMPLETED', 'Notes']].copy()

        dfActive = dfActive.append(active_df, ignore_index=True)
        print(f)
    
    os.chdir('..')

if INACTIVE:
    os.chdir(inactive_path)

    for f in inactivechunks:
        holding_inactive = pd.read_excel(f)
        inactive_df = holding_inactive[['Email', 'EID_M', 'EID_AM', 'Profile Exists_BE', 'Profile Exists_WD',
                                        'In Mobilize under another ID?', 'In Alert Media under name and/or email?',
                            'In backend and/or Workday?', 'Need to reactivate?', 'Completed Date', 'Completed by',
                            'FirstName_M', 'LastName_M', 'Phone_M', 'Class_M', 'SSN FINAL', 'Is Profile Active?']].copy()

        dfInactive = dfInactive.append(inactive_df, ignore_index=True)
        print(f)

    os.chdir('..')

if DELETE:
    os.chdir(delete_path)

    for f in deletechunks:
        holding_delete = pd.read_excel(f)
        delete_df = holding_delete[['First Name', 'Last Name', 'Phone', 'Email', 'Profile ID', 'WorkdayID', 'Created Date', 'Modified Date',
                                    'Delete?', 'Completed By', 'Completed Date', 'Notes']].copy()

        dfDelete = dfDelete.append(delete_df, ignore_index=True)
        print(f)

    os.chdir('..')

def format_Dates(series):
    date_parts = series.str.split('/', expand=True)
    return date_parts[0].str.zfill(4) + '/' + date_parts[1].str.zfill(2) + '/' + date_parts[2].str.zfill(2)

if ACTIVE:
    dfActive['DATE COMPLETED'] = dfActive['DATE COMPLETED'].astype(str)
    dfActive['DATE COMPLETED'] = dfActive['DATE COMPLETED'].str.replace(' 00:00:00', '', regex=True)
    dfActive['DATE COMPLETED'] = dfActive['DATE COMPLETED'].str.replace('-', '/', regex=True)
    dfActive['DATE COMPLETED'] = format_Dates(dfActive['DATE COMPLETED'])

if INACTIVE:
    dfInactive['Completed Date'] = dfInactive['Completed Date'].astype(str)
    dfInactive['Completed Date'] = dfInactive['Completed Date'].str.replace(' 00:00:00', '', regex=True)
    dfInactive['Completed Date'] = dfInactive['Completed Date'].str.replace('-', '/', regex=True)
    dfInactive['Completed Date'] = format_Dates(dfInactive['Completed Date'])

if DELETE:
    dfDelete['Completed Date'] = dfDelete['Completed Date'].astype(str)
    dfDelete['Completed Date'] = dfDelete['Completed Date'].str.replace(' 00:00:00', '', regex=True)
    dfDelete['Completed Date'] = dfDelete['Completed Date'].str.replace('-', '/', regex=True)
    dfDelete['Completed Date'] = format_Dates(dfDelete['Completed Date'])

# if ACTIVE:
#     #taking first 5 characters from the year
#     dfTemp = dfActive['DATE COMPLETED'].str[:5]
#     #getting rid of the rest
#     dfActive['DATE COMPLETED'] = dfActive['DATE COMPLETED'].str[5:]
#     dfTemp = dfTemp.str.replace('/', '', regex=True)
#     dfTemp2 = dfActive['DATE COMPLETED'] + '/' + dfTemp
#     dfActive['DATE COMPLETED'] = dfTemp2

# if INACTIVE:
# #taking first 5 characters from the year
#     dfTemp = dfInactive['Completed Date'].str[:5]
#     #getting rid of the rest
#     dfInactive['Completed Date'] = dfInactive['Completed Date'].str[5:]
#     dfTemp = dfTemp.str.replace('/', '', regex=True)
#     dfTemp2 = dfInactive['Completed Date'] + '/' + dfTemp
#     dfInactive['Completed Date'] = dfTemp2

if ACTIVE:
    dfActive['Completed By'] = dfActive['Completed By'].str.title().str.strip()
if INACTIVE:
    dfInactive['Completed by'] = dfInactive['Completed by'].str.title().str.strip()
if DELETE:
    dfDelete['Completed by'] = dfDelete['Completed By'].str.title().str.strip()
    dfDelete['Delete?'] = dfDelete['Delete?'].str.title().str.strip()

if ACTIVE:
    ActivePivot = pd.DataFrame()
    ActivePivot2 = pd.DataFrame()
if INACTIVE:
    InactivePivot = pd.DataFrame()
    InactivePivot2 = pd.DataFrame()
if DELETE:
    DeletePivot = pd.DataFrame()
    DeletePivot2 = pd.DataFrame()
    DeletePivot3 = pd.DataFrame()
    DeletePivot4 = pd.DataFrame()
    DeletePivot5 = pd.DataFrame()
    DeletePivot6 = pd.DataFrame()
    DeletePivot7 = pd.DataFrame()

if ACTIVE:
    ActivePivot['Completed Date'] = dfActive['DATE COMPLETED']
    ActivePivot['Completed By'] = dfActive['Completed By']
    ActivePivot['ActiveCount'] = np.NaN
    ActivePivot2['Completed Date'] = dfActive['DATE COMPLETED']
    ActivePivot2['Completed By'] = dfActive['Completed By']
    ActivePivot2['ActiveCount'] = np.NaN

if INACTIVE:
    InactivePivot['Completed Date'] = dfInactive['Completed Date']
    InactivePivot['Completed By'] = dfInactive['Completed by']
    InactivePivot['InactiveCount'] = np.NaN
    InactivePivot2['Completed Date'] = dfInactive['Completed Date']
    InactivePivot2['Completed By'] = dfInactive['Completed by']
    InactivePivot2['InactiveCount'] = np.NaN

if DELETE:
    DeletePivot['Completed Date'] = dfDelete['Completed Date']
    DeletePivot['Completed By'] = dfDelete['Completed By']
    DeletePivot['Delete?'] = dfDelete['Delete?']
    DeletePivot['DeleteCount'] = np.NaN
    DeletePivot2['Completed Date'] = dfDelete['Completed Date']
    DeletePivot2['Completed By'] = dfDelete['Completed By']
    DeletePivot2['Delete?'] = dfDelete['Delete?']
    DeletePivot2['DeleteCount'] = np.NaN
    DeletePivot3['Completed Date'] = dfDelete['Completed Date']
    DeletePivot3['Completed By'] = dfDelete['Completed By']
    DeletePivot3['Delete?'] = dfDelete['Delete?']
    DeletePivot3['DeleteCount'] = np.NaN
    DeletePivot4['Completed Date'] = dfDelete['Completed Date']
    DeletePivot4['Completed By'] = dfDelete['Completed By']
    DeletePivot4['Delete?'] = dfDelete['Delete?']
    DeletePivot4['DeleteCount'] = np.NaN
    DeletePivot5['Completed Date'] = dfDelete['Completed Date']
    DeletePivot5['Completed By'] = dfDelete['Completed By']
    DeletePivot5['Delete?'] = dfDelete['Delete?']
    DeletePivot5['DeleteCount'] = np.NaN
    DeletePivot6['Completed Date'] = dfDelete['Completed Date']
    DeletePivot6['Completed By'] = dfDelete['Completed By']
    DeletePivot6['Delete?'] = dfDelete['Delete?']
    DeletePivot6['DeleteCount'] = np.NaN
    DeletePivot7['Completed Date'] = dfDelete.loc[lambda x: x['Completed Date'].notna()].apply(lambda x: datetime.strftime(datetime.strptime(x['Completed Date'],'%Y/%m/%d') - 
                                                    timedelta(days=((datetime.strptime(x['Completed Date'],'%Y/%m/%d').weekday() + 1) % 7)), '%Y/%m/%d'), axis=1)
    DeletePivot7['Completed By'] = dfDelete['Completed By']
    DeletePivot7['DeleteCount'] = np.NaN

if ACTIVE:
    ActivePivot = pd.pivot_table(ActivePivot, index=['Completed Date', 'Completed By'],
                                values=['Completed By'], aggfunc={'ActiveCount': 'size'})

    ActivePivot2 = pd.pivot_table(ActivePivot2, index=['Completed By', 'Completed Date'],
                                values=['ActiveCount'], aggfunc={'ActiveCount': 'size'})

if INACTIVE:
    InactivePivot = pd.pivot_table(InactivePivot, index=['Completed Date', 'Completed By'],
                                values=['Completed By'], aggfunc={'InactiveCount': 'size'})

    InactivePivot2 = pd.pivot_table(InactivePivot2, index=['Completed By', 'Completed Date'],
                                values=['InactiveCount'], aggfunc={'InactiveCount': 'size'})

if DELETE:
    DeletePivot = pd.pivot_table(DeletePivot, index=['Completed Date', 'Completed By', 'Delete?'],
                                values=['DeleteCount'], aggfunc={'DeleteCount': 'size'})
    DeletePivot2 = pd.pivot_table(DeletePivot2, index=['Completed Date', 'Delete?', 'Completed By'],
                                values=['DeleteCount'], aggfunc={'DeleteCount': 'size'})
    DeletePivot3 = pd.pivot_table(DeletePivot3, index=['Completed By', 'Completed Date', 'Delete?'],
                                values=['DeleteCount'], aggfunc={'DeleteCount': 'size'})
    DeletePivot4 = pd.pivot_table(DeletePivot4, index=['Completed By', 'Delete?', 'Completed Date'],
                                values=['DeleteCount'], aggfunc={'DeleteCount': 'size'})
    DeletePivot5 = pd.pivot_table(DeletePivot5, index=['Delete?', 'Completed Date', 'Completed By'],
                                values=['DeleteCount'], aggfunc={'DeleteCount': 'size'})
    DeletePivot6 = pd.pivot_table(DeletePivot6, index=['Delete?', 'Completed By', 'Completed Date', ],
                                values=['DeleteCount'], aggfunc={'DeleteCount': 'size'})
    DeletePivot7 = pd.pivot_table(DeletePivot7, index=['Completed Date', 'Completed By'],
                                values=['DeleteCount'], aggfunc={'DeleteCount': 'size'})

writer = pd.ExcelWriter(f'{date} metrics.xlsx', engine='xlsxwriter')

if ACTIVE:
    ActivePivot.to_excel(writer, sheet_name='Metrics')
    ActivePivot2.to_excel(writer, sheet_name='Metrics', startcol=4)
if INACTIVE:
    InactivePivot.to_excel(writer, sheet_name='Metrics', startcol=8)
    InactivePivot2.to_excel(writer, sheet_name='Metrics', startcol=12)
if DELETE:
    DeletePivot7.to_excel(writer, sheet_name='Metrics', startcol=16)
    DeletePivot.to_excel(writer, sheet_name='Metrics', startcol=20)
    DeletePivot2.to_excel(writer, sheet_name='Metrics', startcol=25)
    DeletePivot3.to_excel(writer, sheet_name='Metrics', startcol=30)
    DeletePivot4.to_excel(writer, sheet_name='Metrics', startcol=35)
    DeletePivot5.to_excel(writer, sheet_name='Metrics', startcol=40)
    DeletePivot6.to_excel(writer, sheet_name='Metrics', startcol=45)
if ACTIVE:
    dfActive.to_excel(writer, sheet_name='Active')
if INACTIVE:
    dfInactive.to_excel(writer, sheet_name='Inactive')
if DELETE:
    dfDelete.to_excel(writer, sheet_name='Delete')

writer.sheets['Metrics'].set_column(0, 48, 15)
writer.save()



