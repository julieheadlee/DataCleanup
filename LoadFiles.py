import pandas as pd
import numpy as np
import os

# Get list of files to process
path = 'C:/master_rosters'

files = os.listdir(path)

# Create empty dataframe
roster_df = 
# for each file append data to Dataframe
for f in files:
    # read the file to a dataframe
    file_df = pd.read_excel(f, sheet_name="Sheet1")

    # rename the hospitl column if it is not standard
    try:
        file_df.rename(columns= {'Hospital':'Hospital Assignment'})
    except:
        continue

    try:
        file_df.rename(columns= {'AS':'Hospital Assignment'})
    except:
        continue

    try:
        file_df.rename(columns= {'Facility':'Hospital Assignment'})
    except:
        continue  

    