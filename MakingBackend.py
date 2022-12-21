import pandas as pd
import numpy as np

# 1 Combines Backend Sharepoint Lists into one file.

dfCarrizo = pd.read_csv('../MasterTracking_Data/Backend 1215/Carrizo.csv', low_memory=False)
dfBCFS2 = pd.read_csv('../MasterTracking_Data/Backend 1215/BCFS2.csv', low_memory=False)
dfInactive = pd.read_csv('../MasterTracking_Data/Backend 1215/Inactive.csv',low_memory=False)
dfNYC = pd.read_csv('../MasterTracking_Data/Backend 1215/NYC.csv', low_memory=False)

NaN = np.nan
dfNYC['Class working as'] = NaN
dfInactive['Activation Date'] = NaN
dfNYC['Star Number'] = NaN
dfInactive['Star Number'] = NaN
dfInactive['Vaccination Status'] = NaN
dfBCFS2['Activation Time'] = NaN
dfInactive['Activation Time'] = NaN
dfCarrizo['Status Notes'] = NaN
dfInactive['Status Notes'] = NaN
dfNYC['Status Notes'] = NaN
dfNYC['Spanish Fluent?'] = NaN
dfInactive['Spanish Fluent?'] = NaN
dfBCFS2['Drivers License Number'] = NaN
dfNYC['Drivers License Number'] = NaN
dfCarrizo['Demob Date'] = NaN
dfNYC['Demob Date'] = NaN
dfBCFS2['Demob Date'] = NaN
dfBCFS2['Drivers License State'] = NaN
dfNYC['Drivers License State'] = NaN
dfBCFS2['Drivers Licenses Expiration'] = NaN
dfNYC['Drivers Licenses Expiration'] = NaN
dfNYC['Shirt Size'] = NaN
dfCarrizo['Drivers Licenses Active'] = NaN
dfNYC['Drivers Licenses Active'] = NaN
dfInactive['Drivers Licenses Active'] = NaN

column_names = ['Deployment', 'Activation Date' ,'Star Number','Status', 'First Name_be', 'Middle Name_be', 'Last Name_be', 'Email Address_be', 'Phone Number_be', 'Gender_be', \
                'Date of Birth_be','SS#_be', 'Class_be', 'Clinical Area of Specialty_be','Class Working As_be', 'Assignment/Facility', 'Hotel',\
                'Address_be', 'City of Residency_be', 'State of Residency_be', 'Zip Code_be', 'Name EXACTLY as it Appears on Medical License_be', \
                'State(s) Medical License is Valid In_be', 'Professional License Number_be', 'Expected Date of Arrival', 'Emergency Contact #_be',\
                'Vaccination Status', 'Activator Name', 'Activation Time', 'Notes', 'Status Notes', 'Spanish Fluent?', 'Drivers License Number', \
                'Drivers License State', 'Drivers Licenses Active','Drivers Licenses Expiration', 'Demob Date', 'Shirt Size']

dfCombined = pd.DataFrame(columns = column_names)

print(dfCombined)

dfCombined['Deployment'] = pd.concat([dfCarrizo['Deployment'], dfBCFS2['Deployment'], dfNYC['Deployment Name'], dfInactive['Deployment']])
dfCombined['Activation Date'] = pd.concat([dfCarrizo['Activation Date'], dfBCFS2['Activation Date'], dfNYC['Activation Date'], dfInactive['Activation Date']])
dfCombined['Star Number'] = pd.concat([dfCarrizo['STAR Number'], dfBCFS2['Star Number'], dfNYC['Star Number'], dfInactive['Star Number']])
dfCombined['Status'] = pd.concat([dfCarrizo['Status'], dfBCFS2['Status'], dfNYC['Status'], dfInactive['Status']])
dfCombined['First Name_be'] = pd.concat([dfCarrizo['First name'], dfBCFS2['First Name'], dfNYC['First Name'], dfInactive['First Name']])
dfCombined['Middle Name_be'] = pd.concat([dfCarrizo['Middle Name'], dfBCFS2['Middle Name'], dfNYC['Middle Name'], dfInactive['Middle Name']])
dfCombined['Last Name_be'] = pd.concat([dfCarrizo['Last Name'], dfBCFS2['Last Name'], dfNYC['Last Name'], dfInactive['Last Name']])
dfCombined['Email Address_be'] = pd.concat([dfCarrizo['Email Address'], dfBCFS2['E-mail Address'], dfNYC['E-mail Address'], dfInactive['E-mail Address']])
dfCombined['Phone Number_be'] = pd.concat([dfCarrizo['Phone Number'], dfBCFS2['Phone Number'], dfNYC['Phone Number'], dfInactive['Phone Number']])
dfCombined['Gender_be'] = pd.concat([dfCarrizo['Gender'], dfBCFS2['Gender'], dfNYC['Gender'], dfInactive['Gender']])
dfCombined['Date of Birth_be'] = pd.concat([dfCarrizo['Date of Birth'], dfBCFS2['Date of Birth'], dfNYC['DOB'], dfInactive['Date of Birth']])
dfCombined['SS#_be'] = pd.concat([dfCarrizo['SSN'], dfBCFS2['SS#'], dfNYC['SS#'], dfInactive['SS#']])
dfCombined['Class_be'] = pd.concat([dfCarrizo['Class'], dfBCFS2['Class'], dfNYC['Class'], dfInactive['Class']])
dfCombined['Clinical Area of Specialty_be'] = pd.concat([dfCarrizo['Clinical Area of Speciality'], dfBCFS2['Clinical Area of Specialty'], dfNYC['Clinical Area of Specialty'], dfInactive['Clinical Area of Specialty']])
dfCombined['Class Working As_be'] = pd.concat([dfCarrizo['Class working as'], dfBCFS2['Class working as'], dfNYC['Class working as'], dfInactive['Class working as']])
dfCombined['Assignment/Facility'] = pd.concat([dfCarrizo['Assignment'], dfBCFS2['Name of Facility/Hospital'], dfNYC['Name of Facility/Hospital'], dfInactive['Name of Facility/Hospital']])
dfCombined['Hotel'] = pd.concat([dfCarrizo['Name of Shelter/Hotel'], dfBCFS2['Hotel'], dfNYC['Hotel'], dfInactive['Hotel']])
dfCombined['Address_be'] = pd.concat([dfCarrizo['Address'], dfBCFS2['Address1'], dfNYC['Address 1'], dfInactive['Address1']])
dfCombined['City of Residency_be'] = pd.concat([dfCarrizo['City of Residency'], dfBCFS2['City of Residency'], dfNYC['City of Residency'], dfInactive['City of Residency']])
dfCombined['State of Residency_be'] = pd.concat([dfCarrizo['State of Residency'], dfBCFS2['State of Residency'], dfNYC['State of Residency'], dfInactive['State of Residency']])
dfCombined['Zip Code_be'] = pd.concat([dfCarrizo['Zip Code'], dfBCFS2['Zip Code'], dfNYC['Zip Code'], dfInactive['Zip Code']])
dfCombined['Name EXACTLY as it Appears on Medical License_be'] = pd.concat([dfCarrizo['Name on Prof License'], dfBCFS2['Name EXACTLY as it Appears on Medical License'], dfNYC['Name EXACTLY as it Appears on Medical License'], dfInactive['Name EXACTLY as it Appears on Medical License']])
dfCombined['State(s) Medical License is Valid In_be'] = pd.concat([dfCarrizo['Prof License Issuing State'], dfBCFS2['State(s) Medical License is Valid In'], dfNYC['State(s) Medical License is Valid In'], dfInactive['State(s) Medical License is Valid In']])
dfCombined['Professional License Number_be'] = pd.concat([dfCarrizo['Prof License Number'], dfBCFS2['Medical/Nursing License Number'], dfNYC['Medical/Nursing License Number'], dfInactive['Medical/Nursing License Number']])
dfCombined['Expected Date of Arrival'] = pd.concat([dfCarrizo['Expected Date of Arrival'], dfBCFS2['Expected Date of Arrival'], dfNYC['Expected Date of Arrival'], dfInactive['Expected Date of Arrival']])
dfCombined['Emergency Contact #_be'] = pd.concat([dfCarrizo['Emergency Contact #'], dfBCFS2['Emergency Contact #'], dfNYC['Emergency Contact #'], dfInactive['Emergency Contact #']])
dfCombined['Vaccination Status'] = pd.concat([dfCarrizo['Vaccination response'], dfBCFS2['Fully Vaccinated?'], dfNYC['COVID Vaccine?'], dfInactive['Vaccination Status']])
dfCombined['Activator Name'] = pd.concat([dfCarrizo['Activator Name'], dfBCFS2['ActivatorName'], dfNYC['ActivatorName'], dfInactive['ActivatorName']])
dfCombined['Activation Time'] = pd.concat([dfCarrizo['Activation Time'], dfBCFS2['Activation Time'], dfNYC['ActivationTime'], dfInactive['Activation Time']])
dfCombined['Notes'] = pd.concat([dfCarrizo['Notes'], dfBCFS2['Notes'], dfNYC['Notes'], dfInactive['Notes']])
dfCombined['Status Notes'] = pd.concat([dfCarrizo['Status Notes'], dfBCFS2['Status Notes'], dfNYC['Status Notes'], dfInactive['Status Notes']])
dfCombined['Spanish Fluent?'] = pd.concat([dfCarrizo['Spanish Fluent?'], dfBCFS2['Fluent in Spanish and English? (Yes or No)'], dfNYC['Spanish Fluent?'], dfInactive['Spanish Fluent?']])
dfCombined['Drivers License Number'] = pd.concat([dfCarrizo['Drivers License Number'], dfBCFS2['Drivers License Number'], dfNYC['Drivers License Number'], dfInactive['License Number']])
dfCombined['Drivers License State'] = pd.concat([dfCarrizo['DL Issuing State'], dfBCFS2['Drivers License State'], dfNYC['Drivers License State'], dfInactive['License State']])
dfCombined['Drivers Licenses Active'] = pd.concat([dfCarrizo['Drivers Licenses Active'], dfBCFS2['DL Active?'], dfNYC['Drivers Licenses Active'], dfInactive['Drivers Licenses Active']])
dfCombined['Drivers Licenses Expiration'] = pd.concat([dfCarrizo['DL Expiration Date'], dfBCFS2['Drivers Licenses Expiration'], dfNYC['Drivers Licenses Expiration'], dfInactive['License Expiration Date']])
dfCombined['Demob Date'] = pd.concat([dfCarrizo['Demob Date'], dfBCFS2['Demob Date'], dfNYC['Demob Date'], dfInactive['Demob Date']])
dfCombined['Shirt Size'] = pd.concat([dfCarrizo['Shirt Size'], dfBCFS2['Shirt Size'], dfNYC['Shirt Size'], dfInactive['Shirt Size']])


dfCombined.reset_index(drop=True, inplace=True)
dfCombined.to_csv('../MasterTracking_Data/Backend_Combined.csv')