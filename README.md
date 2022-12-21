# KrucialStaffing
 
Data Cleanup, 
Historial Data, 
WebEOC/Field Data


For dataclean- run the code in this file order \
1) Generating Backend\
Master Combined- Puts all files together in this order Mobilize-Alert Media - Backend- Workday - EOC\
FormattingFile - formats various aspect from the sources to help matches\
MasterComparison - compares everything/adds some columns and reorganizes them - first name from all sources marks if needs to be fixed or correct- etc\
MobilizeInactive - merges in the inactive bump and breaks down the files into 3 catagories- Inactive, row correct, everything else\
AMImportMaker - creates a file to import info we can assume as correct into AM, import file into AM, export all Users, rename that export as AM Download, and rerun code up to this point then go to ChunkMaker instead.\
ChunkMaker - breaks the Incorrect file into bite-sized chunks of X rows, and puts them into a folder called Chunks\
ChunkFormatter - Formats the chunks to look how we want them to be

UPDATED 9/9/2022 - we will no longer be working with WebEOC.  We may remove Workday, but I am leaving it in for now.

1. MasterCombined_simplified - puts all files together in this order: Mobilize, Alert Media, KOPA (backend), Workday.  WebEOC references removed from original
2. FormattingFile_simplified - formats various aspects from the sources to help matches.  WebEOC references removed from original
3. MasterComparison_simplified - compares everything, adds some columns and reorganizes them. WebEOC references need to be removed from original
4. 
