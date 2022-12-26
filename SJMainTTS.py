import pandas as pd
   
from Tourney import *
from Calculations import *

class playerLvls():
    def __init__(self, lvl3s, lvl4s, lvl5s):
        self.lvl3s = lvl3s
        self.lvl4s = lvl4s
        self.lvl5s = lvl5s

def Main():
    masterExcelFile = "SJ Fall 2022 (Oct3- Dec23) Tournaments.xlsx"
    rankedLvlPlayersDF = pd.read_excel(masterExcelFile, sheet_name = 2)

    lvl3s = rankedLvlPlayersDF['LEVEL3'].dropna()
    lvl4s = rankedLvlPlayersDF['LEVEL4'].dropna()
    lvl5s = rankedLvlPlayersDF['LEVEL5'].dropna()

    playerLvlsObj = playerLvls(lvl3s, lvl4s, lvl5s)

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
        tourneyObj = Tourney(data['Hyperlink'],    data['SGGName'],     data['TName'],   data['TSeries'],   data['Color'],  data['TotalEntrants'],  data['ResultsString'])
        name = str(data['SGGName'])  
        tourneyObjDict[name] = tourneyObj

    for tourney in tourneyObjDict:
        makeTourneyPlacementDict(tourneyObjDict[tourney])
        getTourneyScores(tourneyObjDict[tourney], playerLvlsObj)
        # updateAllPlayerScores(fullTourneyObjDict[tourney])







Main()
