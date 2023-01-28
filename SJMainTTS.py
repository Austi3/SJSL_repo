import pandas as pd
   
from Tourney import *
from Calculations import *
from plotFunctions import *

class playerLvls():
    def __init__(self, lvl2s, lvl3s, lvl4s, lvl5s):
        self.lvl2s = lvl2s
        self.lvl3s = lvl3s
        self.lvl4s = lvl4s
        self.lvl5s = lvl5s

def Main():
    masterExcelFile = "SJ Fall 2022 (Oct3- Dec23) Tournaments.xlsx"
    rankedLvlPlayersDF = pd.read_excel(masterExcelFile, sheet_name = 2)

    lvl2s = rankedLvlPlayersDF['LEVEL2'].str.lower().dropna().to_list()
    lvl3s = rankedLvlPlayersDF['LEVEL3'].str.lower().dropna().to_list()
    lvl4s = rankedLvlPlayersDF['LEVEL4'].str.lower().dropna().to_list()
    lvl5s = rankedLvlPlayersDF['LEVEL5'].str.lower().dropna().to_list()

    playerLvlsObj = playerLvls(lvl2s, lvl3s, lvl4s, lvl5s)

    tourneyExcelDF = pd.read_excel(masterExcelFile, sheet_name = 1)

    # important dictionaries that store all tournament and player objects

    tourneyObjDict = {}
    # key is tourney name, value is the actual tourney object

    playerObjDict = {}
    # key is player name, value is the actual player object

    # populate tourney object dictionary
    for row in tourneyExcelDF.iterrows():
        # row[0] is the index, row[1] is the dataframe 
        data = row[1]
        #tourney            Hyperlink              SGGName              TName,           TSeries,           Color,          TotalEntrants,          ResultsString)
        tourneyObj = Tourney(data['Hyperlink'],    data['SGGName'],     data['TName'],   data['TSeries'],   data['Color'],  data['Total Entrants'],  data['ResultsString'])
        name = str(data['SGGName'])  
        if "hyperspace" not in name:
            tourneyObjDict[name] = tourneyObj

    for tourney in tourneyObjDict:
        makeTourneyPlacementDict(tourneyObjDict[tourney])
        getTourneyScores(tourneyObjDict[tourney], playerLvlsObj)
    
        updateAllPlayerScores(tourneyObjDict[tourney], playerObjDict)        
    
    # covert the dict of tourneys into a dataframe for plotting
    tourneyDF = pd.DataFrame.from_records([tourneyObjDict[tournName].to_dict() for tournName in tourneyObjDict])

    # # Plotting Tourney Info
    # plotDataFrame(tourneyDF, 'stackedScore', 'SJ Tourneys by Stacked Score')
    # plotDataFrame(tourneyDF, 'Total Entrants', 'SJ Tourney Attendance')
    # plotDataFrame(tourneyDF, 'totalScore', 'SJ Tourneys by Total Score')
    # plotDataFrame(tourneyDF, 'stackedRatio', 'SJ Tourneys by Stacked Player Ratio')

    """
    TODO  i want to have an option to plot each individual's placement at a tourney and their pt ratio gathered from that
    that would be soemthing good to have user input and lookup on. would require a nested structure of sorts

    for playerTag in playerObjDict:
        plotPlayerPerformance(playerTag, playerObjDict, tourneyObjDict)
        break
    """
    playerDF = pd.DataFrame.from_records([playerObjDict[playerTag].to_dict() for playerTag in playerObjDict])

    # getPlayerTopResults(playerObjDict)

    # plotPlayerDataFrame(playerDF, playerObjDict, 'weightedPercentileAvg', 'Players Ranked by Weighted Percentile Ratio')
    # plotPlayerDataFrame(playerDF, playerObjDict, 'avgPercentile', 'Players Ranked by Average Placement Percentile')

    # plotPlayerDataFrame(playerDF, playerObjDict, 'earnedTourneyPts', 'Earned Tourney Pts of Each Player')
    # plotPlayerDataFrame(playerDF, playerObjDict, 'totalPossibleTourneyPts', 'Max Possible Pts for Each Player')

    # plotPlayerDataFrame(playerDF, playerObjDict, 'tourneyPtRatio', ' Tourney Pt Ratio (Temp Best Alg)')

    return tourneyObjDict, playerObjDict
    


"""
TODO i want a look up and print function that searches for a player or tournament and outputs the info i want i need to be able to search
this database of mine
"""

Main()
