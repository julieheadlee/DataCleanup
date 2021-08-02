import pandas as pd
import numpy as np
import os
import sys

# Get list of files to process - Master rosters
path = 'C:/DataCleanup/Data'
master_path = '/BCFS_Masters'
backend_path = '/Backend'
carrizo_path = '/Carrizo_masters'
masterfiles = os.listdir(path + master_path)
backendfiles = os.listdir(path + backend_path)
carrizofiles = os.listdir(path + carrizo_path )

# Create empty dataframes to hold all the data
backend_df = pd.DataFrame(columns=['MobilizeEID','LastName', 'FirstName', 'Class', 'ClinicalSpecialty', 'Phone', 'Email',
                                  'Address1', 'Address2', 'City', 'State', 'Zip', 'Gender', 'DOB', 'Facility', 'Deployment',
                                  'Status', 'Demob_date', 'Activator', 'Hotel', 'MedLicenseName', "LicenseState", 'LicenseNum'])
master_df = pd.DataFrame(columns=['LastName', 'FirstName', 'Class', 'Clinical Specialty', 'Hotel', 'Phone', 'Email',
                                  'Facility', 'Date'])
carrizo_df = pd.DataFrame(columns=['LastName', 'FirstName', 'Class', 'Hotel', 'Phone', 'Email', 'Facility', 'Date'])

# Create file of all Texas Master Rosters
my_dir = os.getcwd()

os.chdir(path + master_path)

for f in masterfiles:
    # read the file to a dataframe, select the first sheet automatically
    
    try:
        file_df = pd.read_excel(f, sheet_name='Master Roster')
    except: 
        try:
            file_df = pd.read_excel(f, sheet_name='Sheet1')
        except:
            try:
                file_df = pd.read_excel(f, sheet_name='Live Roster')
            except:
                file_df = pd.read_excel(f)
    
    # get the date
    date = f[:10]
    year = date[6:10]
    month = date[:2]
    day = date[3:5]
    
    final_date = year + "/" + month + "/" + day
    
    # rename the hospital and class columns if not standard
    try:
        file_df.rename(columns= {'Hospital':'Facility'}, inplace=True)
    except:
        continue
    
    try:
        file_df.rename(columns= {'AS':'Facility'}, inplace=True)
    except:
        continue
    
    try:
        file_df.rename(columns= {'Facility ':'Facility'}, inplace=True)
    except:
        continue
    
    try:
        file_df.rename(columns= {'Hospital Assignment':'Facility'}, inplace=True)
    except:
        continue
    try:
        file_df.rename(columns= {'HospitalAssignment':'Facility'}, inplace=True)
    except:
        continue   
        
    try:
        file_df.rename(columns={'Class Working As':'Class'}, inplace=True)
    except:
        continue

    try:
        file_df.rename(columns={'Class Working As ':'Class'}, inplace=True)
    except:
        continue
        
    try:
        file_df.rename(columns={'Class Working as':'Class'}, inplace=True)
    except:
        continue
    
    try:
        file_df.rename(columns={'Last Name': 'LastName', 'First Name':'FirstName'}, inplace=True)
    except:
        continue
        
    try:
        file_df.rename(columns={'Phone Number':'Phone'}, inplace=True)
    except:
        continue
    try:
        file_df.rename(columns={'Phone Number ':'Phone'}, inplace=True)
    except:
        continue

    try:
        file_df.rename(columns={'PhoneNumber':'Phone'}, inplace=True)
    except:
        continue
        
    try:
        file_df.rename(columns={'Specialty':'Clinical Specialty'}, inplace=True)
    except:
        continue
    file_df['Date'] = final_date

    print(f)
    holding_df = file_df[['LastName', 'FirstName', 'Class', 'Clinical Specialty', 'Hotel','Phone', 'Email', 
                                  'Facility',  'Date']].copy()
    
    # append temp dataframe to master
    master_df = master_df.append(holding_df, ignore_index=True)

# rename columns 
master_df.rename(columns={'Clinical Specialty':'ClinicalSpecialty'}, 
                inplace=True)

# Save to file for quick exam -- there are too many rows to use for processing
os.chdir(path)
master_df.to_csv("full_master_roster_TX.csv")

# Create master roster of Carrizo 

os.chdir(path + carrizo_path)

for f in carrizofiles:
    # read the file to a dataframe, select the first sheet automatically
    
    try:
        file_df = pd.read_excel(f, sheet_name='Master Roster')
    except: 
        try:
            file_df = pd.read_excel(f, sheet_name='Sheet1')
        except:
            try:
                file_df = pd.read_excel(f, sheet_name='Live Roster')
            except:
                file_df = pd.read_excel(f)
    
    # get the date
    date = f[:10]
    year = date[6:10]
    month = date[:2]
    day = date[3:5]
    
    final_date = year + "/" + month + "/" + day
    
    # rename the hospital and class columns if not standard
    try:
        file_df.rename(columns= {'Hospital':'Facility'}, inplace=True)
    except:
        continue
    
    try:
        file_df.rename(columns= {'AS':'Facility'}, inplace=True)
    except:
        continue
    try:
        file_df.rename(columns= {'Assignment':'Facility'}, inplace=True)
    except:
        continue
    
    try:
        file_df.rename(columns= {'Facility ':'Facility'}, inplace=True)
    except:
        continue
    
    try:
        file_df.rename(columns= {'Facility Assignment':'Facility'}, inplace=True)
    except:
        continue
    
    try:
        file_df.rename(columns={'Class Working As':'Class'}, inplace=True)
    except:
        continue
    
    try:
        file_df.rename(columns={'Class Working as':'Class'}, inplace=True)
    except:
        continue
    
    try:
        file_df.rename(columns={'Last Name': 'LastName', 'First Name':'FirstName'}, inplace=True)
    except:
        continue

    try:
        file_df.rename(columns={'PhoneNumber': 'Phone'}, inplace=True)
    except:
        continue
        
    try:
        file_df.rename(columns={'Phone Number':'Phone'}, inplace=True)
    except:
        continue
    try:
        file_df.rename(columns={'Phone Number ':'Phone'}, inplace=True)
    except:
        continue

    print(f)    
    file_df['Date'] = final_date
    # create temp dataframe with all necessary columns
    carrizo_holding_df = file_df[['LastName', 'FirstName', 'Class', 'Hotel','Phone', 'Email',
                                  'Facility',  'Date']].copy()
        
    # append temp dataframe to master
    carrizo_df = carrizo_df.append(carrizo_holding_df, ignore_index=True)

# rename columns 
#carrizo_df.rename(columns={'Phone Number':'Phone'}, 
#                inplace=True)

# Save to file for quick exam -- there are too many rows to use for processing
os.chdir(path)
carrizo_df.to_csv("full_carrizo_master_roster_TX.csv")