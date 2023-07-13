from sheetsReadWriteFunctions import *
from plotFunctions import *
from Calculations import *
from SJSL_Excel_ReadWriter import *
 
docName = "MY SJSL Data Sheet"

seasonName = "SJSL"

tourneySheetName = "%s Tourneys" % seasonName
clusterSheetName = '%s Player Clusters'  % seasonName
playerDFSheet =  "%s Player Data" % seasonName
tourneyDFSheet = "%s Tourney Data" % seasonName

 
def MAIN():
    WriteUpdateTourneyDataSheet(docName, tourneySheetName, "SJSL Official Data", "Tourney URL List")

    tourneyObjDict = getTourneyObjDict(docName, tourneySheetName)

    overwritePlayerClusters = False
    numClusters = 4
    ppaCutoff = 50

    if overwritePlayerClusters:
        writePlayerLevelClustersPPA(docName, tourneySheetName, clusterSheetName, ppaCutoff, numClusters)
    
    ptValueIncrement = 1.5
    playerLvlDict = getPlayerLevels(docName, clusterSheetName ,ptValueIncrement)


    playerObjDict = {}
    maxPlacementBonusPoints = 50
    for tourney in tourneyObjDict:
        getTourneyScores(tourneyObjDict[tourney], playerLvlDict)
        updateAllPlayerData(tourneyObjDict[tourney], playerObjDict, maxPlacementBonusPoints)

    """ LEAGUE ONLY!!!"""
    getWriteLeagueLeaderboard(playerObjDict)

    tourneyDF = pd.DataFrame.from_records([tourneyObjDict[tournName].to_dict() for tournName in tourneyObjDict])
    playerDF = pd.DataFrame.from_records([playerObjDict[playerTag].to_dict() for playerTag in playerObjDict])
    
    """TODO make this dynamic"""
    
    dropColumnsList = ['Tourneys Attended Object List', 'tourneyResultsDict']
    writeDataFrame(docName, playerDFSheet, playerDF, dropColumnsList)
 
    writeDataFrame(docName, tourneyDFSheet, tourneyDF)


    # user_choice, choiceIdx = get_user_choice()
    # showPlot = True
    # numPlayers = 30
    # savePlot = False
    # for plotItem in user_choice:

    #     if plotItem in ["Total League Points", "Max Points Possible", "Number of Tourneys Entered"]:
    #         minTourneys = 0
    #     else: 
    #         minTourneys = 5

    customPlotName = "SJSL Points Leaderboard"
    showPlot = True
    numPlayers = 30
    minTourneys = 0
    plotPlayerData(playerDF, "Total League Points", seasonName, minTourneys, numPlayers, showPlot, customPlotName)

    plotPlayerData(playerDF, "Avg Points Per Tourney", seasonName, minTourneys, numPlayers, showPlot)


    plotTourneyDataFrame(tourneyDF, 'totalScore', "Tourney Point Value (TPV)", 'SJ Tourneys by Tourney Point Value (%s Season)' % seasonName, seasonName)

    # plotTourneyDataFrame(tourneyDF, 'stackedScore', "Stacked Points", 'SJ Tourney Stacked Points (%s Season)' % seasonName, seasonStr)
    # plotTourneyDataFrame(tourneyDF, 'Total Entrants', "Entrant Count",  'SJ Tourney Attendance (%s Season)' % seasonName, seasonStr)
    # plotTourneyDataFrame(tourneyDF, 'stackedRatio', "Stacked Player Index (SPI)", 'SJ Tourneys by Stacked Player Index (%s Season)' % seasonName, seasonStr)



MAIN()


