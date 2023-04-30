from tourneyExtractorWriter import *
from plotFunctions import *
from Calculations import *

 
docName = "2023 SJ Smash Sheet"
sheetName = "2023 Q2 Tourneys"
clusterSheetName = '2023Q2 Player Clusters'
 
""" Run this to update the spreadsheet """
updateTourneyDataSheet(docName, sheetName)

tourneyObjDict = getTourneyObjDict(docName, sheetName)

playerLvlsObj = getPlayerLevels(docName, clusterSheetName)


playerObjDict = {}

for tourney in tourneyObjDict:
    getTourneyScores(tourneyObjDict[tourney], playerLvlsObj)
    updateAllPlayerScores(tourneyObjDict[tourney], playerObjDict) 

playerDF = pd.DataFrame.from_records([playerObjDict[playerTag].to_dict() for playerTag in playerObjDict])

# plotPlayerDataFrame(playerDF, playerObjDict, 'weightedPercentileAvg', 'Weighted Placement Percentile Average (%)', 'Top 30 Weighted Placement Percentile Averages (WPPA)')
# plotPlayerDataFrame(playerDF, playerObjDict, 'avgPercentile', "Placement Percentile Average (%)", 'Top 30 Placement Percentile Averages (PPA)')

# plotPlayerDataFrame(playerDF, playerObjDict, 'earnedTourneyPts', 'Earned Tourney Points', 'Top 30 Earned Tourney Points (ETP)', False, 1)
# plotPlayerDataFrame(playerDF, playerObjDict, 'totalPossibleTourneyPts', 'Max Tourney Points Possible', '30 Players With Highest Max Tourney Points Possible (MTPP)', False)

# plotPlayerDataFrame(playerDF, playerObjDict, 'tourneyPtRatio', 'Earned Point Ratio %) ', 'Top 30 Earned Point Ratios (EPR)')



tourneyDF = pd.DataFrame.from_records([tourneyObjDict[tournName].to_dict() for tournName in tourneyObjDict])
plotTourneyDataFrame(tourneyDF, 'stackedScore', "Stacked Points", 'SJ Tourney Stacked Points (2023 Q1 Season)')
plotTourneyDataFrame(tourneyDF, 'Total Entrants', "Entrant Count",  'SJ Tourney Attendance (2023 Q1 Season)')
plotTourneyDataFrame(tourneyDF, 'totalScore', "Tourney Point Value (TPV)", 'SJ Tourneys by Tourney Point Value (2023 Q1 Season)')
plotTourneyDataFrame(tourneyDF, 'stackedRatio', "Stacked Player Index (SPI)", 'SJ Tourneys by Stacked Player Index (2023 Q1 Season)')



