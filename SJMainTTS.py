import pandas as pd
   
from Tourney import *
from Calculations import *
from plotFunctions import *

import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Path to the credential JSON file
CREDENTIALS_FILE = r'C:\Users\acmaa\DocumentsACM\Local Projects\ImportantCoding\core-synthesis-384200-4101747176bd.json'

# Define the scope that you need to access the API
SCOPE = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']

# Authenticate with the Google Sheets API using the JSON file
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPE)
client = gspread.authorize(creds)

class playerLvls():
    def __init__(self, lvl2s, lvl3s, lvl4s, lvl5s):
        self.lvl2s = lvl2s
        self.lvl3s = lvl3s
        self.lvl4s = lvl4s
        self.lvl5s = lvl5s

def Main(pleasePlot):
    # masterExcelFile = "SJ Spring 2023 Tournaments.xlsx"
    #"SJ Q3 2022 Tournaments.xlsx"
    #"SJ Fall 2022 (Oct3- Dec23) Tournaments.xlsx"
    

    SPREADSHEET_NAME = "2023 SJ Smash Sheet"
    PLAYER_SHEET_NAME = "2023Q1 Players"
    TOURNEY_SHEET_NAME = "2023Q1 Tourneys"

    # # Open the specified sheet
    playersheet = client.open(SPREADSHEET_NAME).worksheet(PLAYER_SHEET_NAME)

    # get all values from the sheet
    playervalues = playersheet.get_all_values()

    # create pandas dataframe from values
    rankedLvlPlayersDF = pd.DataFrame(playervalues[1:], columns=playervalues[0])

    lvl2s = rankedLvlPlayersDF['LEVEL2'].str.lower().dropna().to_list()
    # lvl2s = []
    # """TODO im testing this"""

    lvl3s = rankedLvlPlayersDF['LEVEL3'].str.lower().dropna().to_list()
    lvl4s = rankedLvlPlayersDF['LEVEL4'].str.lower().dropna().to_list()
    lvl5s = rankedLvlPlayersDF['LEVEL5'].str.lower().dropna().to_list()

    playerLvlsObj = playerLvls(lvl2s, lvl3s, lvl4s, lvl5s)


    # # Open the specified sheet
    tourneysheet = client.open(SPREADSHEET_NAME).worksheet(TOURNEY_SHEET_NAME)

    # get all values from the sheet
    tourneyvals = tourneysheet.get_all_values()

    # create pandas dataframe from values
    tourneyExcelDF = pd.DataFrame(tourneyvals[1:], columns=tourneyvals[0])
    tourneyExcelDF['Total Entrants'] = tourneyExcelDF['Total Entrants'].astype(int)


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
        if "hyperspace" not in name and int(data['Total Entrants'])>=8:
            tourneyObjDict[name] = tourneyObj

    for tourney in tourneyObjDict:
        makeTourneyPlacementDict(tourneyObjDict[tourney])
        getTourneyScores(tourneyObjDict[tourney], playerLvlsObj)
    
        updateAllPlayerScores(tourneyObjDict[tourney], playerObjDict)        
    
    # covert the dict of tourneys into a dataframe for plotting
    tourneyDF = pd.DataFrame.from_records([tourneyObjDict[tournName].to_dict() for tournName in tourneyObjDict])


    # # Plotting Tourney Info
    # plotTourneyDataFrame(tourneyDF, 'stackedScore', "Stacked Points", 'SJ Tourney Stacked Points (2023 Q1 Season)')
    # plotTourneyDataFrame(tourneyDF, 'Total Entrants', "Entrant Count", 'SJ Tourney Attendance (2023 Q1 Season)')
    # plotTourneyDataFrame(tourneyDF, 'totalScore', "Tourney Point Value (TPV)", 'SJ Tourneys by Tourney Point Value (2023 Q1 Season)')
    # plotTourneyDataFrame(tourneyDF, 'stackedRatio', "Stacked Player Index (SPI)", 'SJ Tourneys by Stacked Player Index (2023 Q1 Season)')

    """
    TODO  i want to have an option to plot each individual's placement at a tourney and their pt ratio gathered from that
    that would be soemthing good to have user input and lookup on. would require a nested structure of sorts

    for playerTag in playerObjDict:
        plotPlayerPerformance(playerTag, playerObjDict, tourneyObjDict)
        break
    """

# TODO THIS SORTA DOES WORK IDK WHY ITS NTO FOR PLITTNG BUT IT DOES REMOVE THE 20% its so close wow
    # for playerTag in playerObjDict:
    #     playerObjDict[playerTag].tourneyResultsDict= playerObjDict[playerTag].remove_bottom_20_percent(playerObjDict[playerTag].tourneyResultsDict, 'percentilePtsEarned')
        

    playerDF = pd.DataFrame.from_records([playerObjDict[playerTag].to_dict() for playerTag in playerObjDict])

    if not pleasePlot:
        return tourneyObjDict, playerObjDict

    # # getPlayerTopResults(playerObjDict)

    plotPlayerDataFrame(playerDF, playerObjDict, 'weightedPercentileAvg', 'Weighted Placement Percentile Average (%)', 'Top 30 Weighted Placement Percentile Averages (WPPA)')
    plotPlayerDataFrame(playerDF, playerObjDict, 'avgPercentile', "Placement Percentile Average (%)", 'Top 30 Placement Percentile Averages (PPA)')

    plotPlayerDataFrame(playerDF, playerObjDict, 'earnedTourneyPts', 'Earned Tourney Points', 'Top 30 Earned Tourney Points (ETP)', False, 1)
    plotPlayerDataFrame(playerDF, playerObjDict, 'totalPossibleTourneyPts', 'Max Tourney Points Possible', '30 Players With Highest Max Tourney Points Possible (MTPP)', False)

    plotPlayerDataFrame(playerDF, playerObjDict, 'tourneyPtRatio', 'Earned Point Ratio %) ', 'Top 30 Earned Point Ratios (EPR)')

    

Main(True)
"""
TODO i want a look up and print function that searches for a player or tournament and outputs the info i want i need to be able to search
this database of mine
"""

