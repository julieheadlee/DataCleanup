from logging import logMultiprocessing
import pandas as pd
import numpy as np

# 6 Creates Chunks Uncomment portions of code corresponsing to chunks you want to make, and comment the rest.

BLOCK_SIZE = 100 # Sets how large the chunks are.

# Note, need to create file "Chunks" in the correct location, or else it will throw an error

# for incorrect
# dfMaster = pd.read_csv('../MasterTracking_Data/3Catagories/Incorrect.csv', dtype=str, low_memory=False)

# for inactive falses
# dfMaster = pd.read_csv('../MasterTracking_Data/3Catagories/MobilizeFalse.csv', dtype=str, low_memory=False)

# for mobilize to delete chunks
# dfMaster = pd.read_csv('../MasterTracking_Data/MobilizeToDelete/Mobilize_Never_Interacted.csv', dtype=str, low_memory=False)
# dfMaster['Delete?'] = np.NaN
# dfMaster['Completed By'] = np.NaN
# dfMaster['Completed Date'] = np.NaN
# dfMaster['Notes'] = np.NaN
# dfMaster['Phone'] = dfMaster['Phone'].str[:3] + '-' + dfMaster['Phone'].str[3:6] + '-' + dfMaster['Phone'].str[6:]

# for historical
dfMaster = pd.read_csv('../Data/Historical_Combined/Historical_Combined 2022.03.03.csv', dtype=str, low_memory=False)

# for incorrect and inactive falses
# dfMaster = dfMaster.drop(columns=['Unnamed: 0'])

num_of_files = dfMaster.shape[0] // BLOCK_SIZE + 1
print(num_of_files)

for i in range(num_of_files):
    # for incorrect
    # chunk_name = '../MasterTracking_Data/3Catagories/Chunks/' + str(i+1).zfill(len(str(num_of_files))) + '_DataChunk_NAMEHERE.xlsx'

    # for inactive falses
    # chunk_name = '../MasterTracking_Data/3Catagories/Chunks/Inactives/' + str(i + 1).zfill(len(str(num_of_files))) + '_DataChunk_NAMEHERE.xlsx'

    # for mobilize to delete chunks
    # chunk_name = '../MasterTracking_Data/MobilizeToDelete/Delete Chunks/' + str(i + 1).zfill(len(str(num_of_files))) + '_DataChunk_NAMEHERE.xlsx'

    # for historical
    chunk_name = '../Data/Historical_Combined/Historical Chunks/' + str(i + 1).zfill(len(str(num_of_files))) + '_Historical.xlsx'

    chunk = dfMaster.loc[i * BLOCK_SIZE:i * BLOCK_SIZE + BLOCK_SIZE - 1]
    chunk.to_excel(chunk_name)
    print(i + 1, "/", num_of_files) # For visibility if you want to see progress in console. Will flood your console, and slow down the process significantly, do not recommend.

print(f'{num_of_files} files have been generated')
