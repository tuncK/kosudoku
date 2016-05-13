#!/sw/bin/python3.4


# ----------------------------------------------------------------------------------------------- #
# PoolPresenceTableSolve.py
# Created by Buz Barstow 2015-6-14
# Last updated by Buz Barstow 2015-8-26

# All code necessary to build pool presence table from Sudoku reads, except for code that performs
# summary of himar section of reads, and summarizes index reads. 
# Now uses sudokuutils version 7.
# ----------------------------------------------------------------------------------------------- #


from sudokuutils13.input import get_input

from sudokuutils13.utils import ensure_dir

from sudokuutils13.grid import ImportSudokuGridLayout, WriteSudokuGridSummaryTable, \
AnnotateSudokuGridWithFeautureNames, FlattenSudokuGridLookupDict

from sudokuutils13.pool import ImportPoolPresenceTable, SolvePoolPresenceTable

from sudokuutils13.xml import ExportSudokuGridToXML, ImportSudokuGridFromXML

from sudokuutils13.feature import ImportFeatureArrayFromGenBank, UpdateFeatureArrayWithSudokuWells, \
CalculateFeatureArrayTaxonomy


import sys
import pdb
import os

# ----------------------------------------------------------------------------------------------- #
# Import the input parameter file

argv = sys.argv

inputParameters = [\
'rowPools', 'colPools', 'controlPools', 'poolPresenceTableFileName', \
'sudokuGridLayout', 'outputLog', 'maxGapForCoordGrouping', \
'readCountThreshold', 'voigtScoreThreshold', 'maxTotalCoords', 'maxSinglePoolCoordNumber', \
'sudokuGridXMLFile', 'sudokuGridSummaryFileName', 'shewyGenomeGenBankFileName']

# inputParameterValues = get_input2(argv, inputParameters)
inputParameterValues = get_input(['',\
'/Users/buz/Dropbox (BarstowLab)/BarstowLab Shared Folder/Analysis/' \
+ '2015-05-10 - Sudoku Sequencing of Shewanella Sudoku Library/Input Files/Version 13/' \
+ 'SudokuAnalyze13_PoolPresenceSolve.inp'], \
inputParameters)

# ----------------------------------------------------------------------------------------------- #


# ----------------------------------------------------------------------------------------------- #
# Parse the input data
rowPools = inputParameterValues['rowPools'].split(',')
colPools = inputParameterValues['colPools'].split(',')
controlPools = inputParameterValues['controlPools'].split(',')
poolPresenceTableFileName = inputParameterValues['poolPresenceTableFileName']

outputLog = inputParameterValues['outputLog']
sudokuGridLayout = inputParameterValues['sudokuGridLayout']
maxGapForCoordGrouping = int(inputParameterValues['maxGapForCoordGrouping'])
readCountThreshold = int(inputParameterValues['readCountThreshold'])
voigtScoreThreshold = float(inputParameterValues['voigtScoreThreshold'])
maxTotalCoords = int(inputParameterValues['maxTotalCoords'])
maxSinglePoolCoordNumber = int(inputParameterValues['maxSinglePoolCoordNumber'])
sudokuGridXMLFile = inputParameterValues['sudokuGridXMLFile']
sudokuGridSummaryFileName = inputParameterValues['sudokuGridSummaryFileName']
shewyGenomeGenBankFileName = inputParameterValues['shewyGenomeGenBankFileName']
# ----------------------------------------------------------------------------------------------- #



# ------------------------------------------------------------------------------------------------ #
# Import the pool presence table

[sudokuGridLookupDict, prPools, pcPools] = ImportSudokuGridLayout(sudokuGridLayout, rowPools, colPools)

sudokuPoolColumns = ['readAlignmentCoord'] + rowPools + colPools + prPools + pcPools + controlPools

poolPresenceTable = ImportPoolPresenceTable(poolPresenceTableFileName, sudokuPoolColumns)
# ------------------------------------------------------------------------------------------------ #


# ------------------------------------------------------------------------------------------------ #
logReadNumberRatioHistogramFitDict = {\
'nr2nc': array([  4.40167575e+03,  -6.14416490e-01,   2.31441504e-01, 6.10917305e-01]), \
'npr2npc': array([  4.37639039e+03,  -1.93463028e-01,   2.49560416e-01, 5.69134210e-01]), \
'nc2npc': array([  4.26554263e+03,  -1.28866329e+00,   1.02679161e-01, 8.49570121e-01]), \
'nr2npr': array([  4.29226485e+03,  -1.77483793e+00,   1.67029253e-01, 8.50852254e-01]), \
'nc2npr': array([  4.33491451e+03,  -9.78105660e-01,   2.26399445e-01, 7.66314686e-01]), \
'nr2npc': array([  4.24814935e+03,  -2.11653643e+00,   7.17920853e-02, 9.20773485e-01]) }
          

logReadNumberRatioHistogramIntegralDict = {\
'nr2nc': 4335.5755955204122, 'npr2npc': 4305.8760588073219, 'nc2npc': 4236.5746634922598, \
'nr2npr': 4244.0194718705397, 'nc2npr': 4270.6449466057529, 'nr2npc': 4227.2659786258046 }
# ------------------------------------------------------------------------------------------------ #


# ------------------------------------------------------------------------------------------------ #
# Initialize the output files
outputLogDir = os.path.dirname(outputLog)
sudokuGridXMLFileDir = os.path.dirname(sudokuGridXMLFile)
sudokuGridSummaryFileDir = os.path.dirname(sudokuGridSummaryFileName)
	
ensure_dir(outputLogDir + '/')
ensure_dir(sudokuGridXMLFileDir + '/')
ensure_dir(sudokuGridSummaryFileDir + '/')
# ------------------------------------------------------------------------------------------------ #


# ------------------------------------------------------------------------------------------------ #
sudokuGridTaxonomyDict = SolvePoolPresenceTable(sudokuGridLookupDict, poolPresenceTable, \
rowPools, colPools, prPools, pcPools, controlPools, logReadNumberRatioHistogramFitDict, \
logReadNumberRatioHistogramIntegralDict, \
readCountThreshold, voigtScoreThreshold, maxSinglePoolCoordNumber, maxTotalCoords, \
maxGapForCoordGrouping)


featureArray = ImportFeatureArrayFromGenBank(shewyGenomeGenBankFileName)

geneFeatureArray = []
for feature in featureArray:
	if feature.featureType == 'gene':
		geneFeatureArray.append(feature)

flattenedSudokuGrid = FlattenSudokuGridLookupDict(sudokuGridLookupDict, prPools, pcPools, rowPools,\
colPools)

UpdateFeatureArrayWithSudokuWells(geneFeatureArray, flattenedSudokuGrid)

AnnotateSudokuGridWithFeautureNames(sudokuGridLookupDict, geneFeatureArray, prPools, pcPools, \
rowPools, colPools)

featureArrayTaxonomyDict = CalculateFeatureArrayTaxonomy(geneFeatureArray)

ExportSudokuGridToXML(sudokuGridLookupDict, prPools, pcPools, rowPools, colPools, sudokuGridXMLFile)

WriteSudokuGridSummaryTable(sudokuGridSummaryFileName, sudokuGridLookupDict, prPools, pcPools, \
rowPools, colPools)

# ------------------------------------------------------------------------------------------------ #
