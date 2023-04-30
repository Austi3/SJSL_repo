from tourneyExtractorWriter import *
from plotFunctions import *
from Calculations import *

 
docName = "2023 SJ Smash Sheet"
sheetName = "2023 Q2 Tourneys"
clusterSheetName = '2023Q2 Player Clusters'
 
""" Run this to update the spreadsheet """
# updateTourneyDataSheet(docName, sheetName)

tourneyObjDict = getTourneyObjDict(docName, sheetName)

playerLvlsObj = getPlayerLevels(docName, clusterSheetName)

for tourney in tourneyObjDict:
    getTourneyScores(tourneyObjDict[tourney], playerLvlsObj)

tourneyDF = pd.DataFrame.from_records([tourneyObjDict[tournName].to_dict() for tournName in tourneyObjDict])
plotTourneyDataFrame(tourneyDF, 'stackedScore', "Stacked Points", 'SJ Tourney Stacked Points (2023 Q1 Season)')
plotTourneyDataFrame(tourneyDF, 'Total Entrants', "Entrant Count",  'SJ Tourney Attendance (2023 Q1 Season)')
plotTourneyDataFrame(tourneyDF, 'totalScore', "Tourney Point Value (TPV)", 'SJ Tourneys by Tourney Point Value (2023 Q1 Season)')
plotTourneyDataFrame(tourneyDF, 'stackedRatio', "Stacked Player Index (SPI)", 'SJ Tourneys by Stacked Player Index (2023 Q1 Season)')



#     makeTourneyPlacementDict(tourneyObjDict[tourney])
#     

#     updateAllPlayerScores(tourneyObjDict[tourney], playerObjDict
                              
# # tourneyDF = pd.DataFrame.from_records([tourneyObjDict[tournName].to_dict() for tournName in tourneyObjDict])


# plotTourneyDataFrame(tourneyDF, 'stackedScore', "Stacked Points", 'SJ Tourney Stacked Points (2023 Q1 Season)')
# plotTourneyDataFrame(tourneyDF, 'Total Entrants', "Entrant Count", 'SJ Tourney Attendance (2023 Q1 Season)')
# plotTourneyDataFrame(tourneyDF, 'totalScore', "Tourney Point Value (TPV)", 'SJ Tourneys by Tourney Point Value (2023 Q1 Season)')
# plotTourneyDataFrame(tourneyDF, 'stackedRatio', "Stacked Player Index (SPI)", 'SJ Tourneys by Stacked Player Index (2023 Q1 Season)')


# playerDF = getPlacementPercentileAverages(tourneyDF)

# getPlayerSkillLevels(playerDF, sheetName, clusterSheetName)