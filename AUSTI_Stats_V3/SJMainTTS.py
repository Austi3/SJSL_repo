from sheetsReadWriteFunctions import *
from plotFunctions import *
from Calculations import *

 
docName = "2023 SJ Smash Sheet"

seasonName = "2023 Q1"

tourneySheetName = "%s Tourneys" % seasonName
clusterSheetName = '%s Player Clusters'  % seasonName


 
def MAIN():
    WriteUpdateTourneyDataSheet(docName, tourneySheetName)

    tourneyObjDict = getTourneyObjDict(docName, tourneySheetName)

    
    numClusters = 4
    ppaCutoff = 50

    writePlayerLevelClustersPPA(docName, tourneySheetName, clusterSheetName, ppaCutoff, numClusters)
    
    ptValueIncrement = 1.5
    playerLvlDict = getPlayerLevels(docName, clusterSheetName ,ptValueIncrement)



    playerObjDict = {}

    for tourney in tourneyObjDict:
        getTourneyScores(tourneyObjDict[tourney], playerLvlDict)
        updateAllPlayerScores(tourneyObjDict[tourney], playerObjDict) 

    tourneyDF = pd.DataFrame.from_records([tourneyObjDict[tournName].to_dict() for tournName in tourneyObjDict])
    playerDF = pd.DataFrame.from_records([playerObjDict[playerTag].to_dict() for playerTag in playerObjDict])

    seasonStr = seasonName + "/"
    plotTourneyDataFrame(tourneyDF, 'stackedScore', "Stacked Points", 'SJ Tourney Stacked Points (%s Season)' % seasonName, seasonStr)
    plotTourneyDataFrame(tourneyDF, 'Total Entrants', "Entrant Count",  'SJ Tourney Attendance (%s Season)' % seasonName, seasonStr)
    plotTourneyDataFrame(tourneyDF, 'totalScore', "Tourney Point Value (TPV)", 'SJ Tourneys by Tourney Point Value (%s Season)' % seasonName, seasonStr)
    plotTourneyDataFrame(tourneyDF, 'stackedRatio', "Stacked Player Index (SPI)", 'SJ Tourneys by Stacked Player Index (%s Season)' % seasonName, seasonStr)


    plotPlayerDataFrame(playerDF, playerObjDict, 'weightedPercentileAvg', 'Weighted Placement Percentile Average (%)', 'Top 30 Weighted Placement Percentile Averages (WPPA)', seasonStr)
    plotPlayerDataFrame(playerDF, playerObjDict, 'avgPercentile', "Placement Percentile Average (%)", 'Top 30 Placement Percentile Averages (PPA)', seasonStr)

    plotPlayerDataFrame(playerDF, playerObjDict, 'earnedTourneyPts', 'Earned Tourney Points', 'Top 30 Earned Tourney Points (ETP)', seasonStr, False, 1)
    plotPlayerDataFrame(playerDF, playerObjDict, 'totalPossibleTourneyPts', 'Max Tourney Points Possible', '30 Players With Highest Max Tourney Points Possible (MTPP)', seasonStr, False)

    plotPlayerDataFrame(playerDF, playerObjDict, 'tourneyPtRatio', 'Earned Point Ratio %) ', 'Top 30 Earned Point Ratios (EPR)', seasonStr)






MAIN()


